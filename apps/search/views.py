import logging

from django.conf import settings
from django.contrib.postgres.search import SearchVector, SearchQuery

from rest_framework import status
from rest_framework.decorators import (
	api_view,
)
from rest_framework.response import Response

from .models import (
	SearchResult,
)

from .serializers import (
	SearchResultSerializer
)

from .tasks import fetch_search_results

from .utils import paginated_queryset

logger = logging.getLogger(__name__)


@api_view(["GET"])
def search_videos(request):
	search_term = request.data.get("search_term").strip()

	logger.info("Incoming query for {}".format(search_term))

	if not SearchResult.objects.last():
			response_data = {"error": "Sorry, No video stored in the DB yet"}
			return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

	if not search_term:
		response_data = {"error": "Sorry, Please send a valid search term"}
		return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

	# Ability to partial match the search query with the title & description, 
	# and also matches closely related words (ex: 'interested' & 'interesting')
	results = SearchResult.objects.annotate(search=SearchVector('title', 'description')).filter(search=search_term).order_by("-publish_time")
	
	# Paginating the response
	paginator, result_page = paginated_queryset(results, request)
	serializer = SearchResultSerializer(
		result_page, many=True, context={"request": request}
	)
	response_data = serializer.data
	return paginator.get_paginated_response(response_data)

