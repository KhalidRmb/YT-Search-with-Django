from django.conf import settings

from rest_framework.pagination import PageNumberPagination


def paginated_queryset(
	queryset, request, pagination_class=PageNumberPagination()
):
	"""
		Return a paginated result for a queryset
	"""
	paginator = pagination_class
	paginator.page_size = settings.REST_FRAMEWORK["PAGE_SIZE"]
	result_page = paginator.paginate_queryset(queryset, request)
	return (paginator, result_page)
