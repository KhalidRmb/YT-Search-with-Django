import logging

from django.contrib.postgres.fields import ArrayField, JSONField
from django.db import models

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex



logger = logging.getLogger(__name__)


class TimeStampedModel(models.Model):
	"""
	An abstract base class model that provides self-managed `created_at` and
	`modified_at` fields.
	"""
	created_at = models.DateTimeField(auto_now_add=True)
	modified_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		app_label = "base"


class SearchResult(TimeStampedModel):
	"""
	Model representing a search result from the Youtube API
	"""
	title = models.CharField(max_length=100)
	description = models.TextField(null=True, blank=True)
	publish_time = models.DateTimeField(
		null=True, blank=True, verbose_name="Video Pulish time (UTC)"
	)
	thumbnail_url = models.URLField(blank=True, null=True)  # Default thumbnail url
	video_id = models.CharField(unique=True, max_length=100)

	class Meta:
		app_label = "search"
		db_table = "search_result"
		indexes = [
            GinIndex(fields=['title', 'description']),
        ]


class APIKey(TimeStampedModel):
	"""
	Model representing a Youtube API Developer's key
	"""
	key = models.TextField(null=True, blank=True)
	is_active = models.BooleanField(default=True, db_index=True)

	class Meta:
		app_label = "search"
		db_table = "api_key"

