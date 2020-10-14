from django.conf.urls import url

from . import views

app_name = "search"

urlpatterns = [
	url(
		r"^keyword_search/$",
		views.search_videos,
		name="search_videos",
	),
]