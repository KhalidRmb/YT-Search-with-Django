import logging

from django.conf import settings
from django.db.models import Q

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
	search_term = request.data.get("search_term")

	logger.info("Incoming query for {}".format(search_term))

	if not SearchResult.objects.last():
			response_data = {"error": "Sorry, No video stored in the DB yet"}
			return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

	words = search_term.strip().split()
	
	# Ability to partial match the search query with the title & description
	query = Q()
	for word in words:
		query = query & (Q(title__icontains=word) | Q(description__icontains=word))
	logger.info(query)
	results = SearchResult.objects.filter(query).order_by("-publish_time")
	logger.info(results)
	
	# Paginating the response
	paginator, result_page = paginated_queryset(results, request)
	serializer = SearchResultSerializer(
		result_page, many=True, context={"request": request}
	)
	response_data = serializer.data
	return paginator.get_paginated_response(response_data)

