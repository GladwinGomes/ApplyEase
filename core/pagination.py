"""
Custom pagination classes for ApplyEase.
"""

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination: 20 items per page, client can override up to 100.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
