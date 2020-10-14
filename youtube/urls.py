from django.contrib import admin
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r"^admin/", admin.site.urls),
	url( r"^api/search/", include("search.urls", namespace="search")),
]

if settings.DEBUG:
	urlpatterns += [
		url(r"^dbschema/", include("django_spaghetti.urls")),
		url(
			r"^api/admin-auth/",
			include("rest_framework.urls", namespace="rest_framework"),
		),
		url(r"^silk/", include("silk.urls", namespace="silk")),
	] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)