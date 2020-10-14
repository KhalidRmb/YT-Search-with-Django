from django import forms
from django.contrib import admin, messages

from django.contrib.admin.helpers import ActionForm

from .models import (
	SearchResult,
	APIKey
)


@admin.register(SearchResult)
class SearchResultAdmin(admin.ModelAdmin):
	exclude = ("created_at", "modified_at")
	readonly_fields = ("created_at",)
	list_display = (
		"title",
		"description",
		"publish_time",
		"thumbnail_url",
		"video_id",
	)
	search_fields = (
		"title",
		"description",
	)

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
	exclude = ("created_at", "modified_at")
	readonly_fields = ("created_at",)
	list_display = ("key", "is_active")
	search_fields = ("is_active", )
