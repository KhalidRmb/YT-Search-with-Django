from rest_framework import serializers

from .models import (
	SearchResult,
)


class SearchResultSerializer(serializers.ModelSerializer):
	def __init__(self, *args, **kwargs):
		super(SearchResultSerializer, self).__init__(*args, **kwargs)

	class Meta:
		model = SearchResult
		fields = (
			"title",
			"description",
			"publish_time",
			"thumbnail_url",
			"video_id",
		)

