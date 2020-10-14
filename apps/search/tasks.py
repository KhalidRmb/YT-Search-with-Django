import json
import logging
import os
import requests

from datetime import datetime, timedelta 

from django.conf import settings

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from youtube.celery import app
from celery import shared_task

from .models import APIKey, SearchResult
from .serializers import SearchResultSerializer

logger = logging.getLogger(__name__)

SEARCH_TERM = settings.SEARCH_TERM
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

@shared_task(name="fetch_search_results_task")
def fetch_search_results():
	DEVELOPER_KEY = APIKey.objects.filter(is_active=True)

	if not DEVELOPER_KEY:
		logger.warning("There are no active API keys present!")
		return
	else:
		DEVELOPER_KEY = DEVELOPER_KEY[0]

	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY.key)

	result = SearchResult.objects.last()
	if not result:
		delta = timedelta(hours=6)
		d = datetime.utcnow() - delta
		d = d.isoformat("T") + "Z"
	else:
		latest = SearchResult.objects.latest('publish_time')
		d = latest.publish_time
		d = d.isoformat("T")
		if not d.endswith("+00:00"):
			d += "+00:00"

	nextToken = None

	while True:
		try:
			if nextToken:
				response = youtube.search().list(q=SEARCH_TERM, part='snippet', publishedAfter=d, order='date', type='video', pageToken=nextToken).execute()
			else:
				response = youtube.search().list(q=SEARCH_TERM, part='snippet', publishedAfter=d, order='date', type='video').execute()
		except Exception as e:
			logger.exception(e)
			if json.loads(e.content)['error']['code'] == 403:
				DEVELOPER_KEY.is_active = False
				DEVELOPER_KEY.save()
			return

		items = response.get('items')
		for item in items:
			search_result = {
				'title': item['snippet']['title'],
				'description': item['snippet']['description'],
				'thumbnail_url': item['snippet']['thumbnails']['default']['url'],
				'publish_time': item['snippet']['publishedAt'],
				"video_id": item['id']['videoId']
			}
			serializer = SearchResultSerializer(data=search_result)
			if serializer.is_valid():
				serializer.save()
			else:
				logger.warning("Serializer is invalid for video {}: {}".format(item['snippet']['title'], serializer.errors))

		if len(items) < 5:
			break

		nextToken = response.get('nextPageToken')

