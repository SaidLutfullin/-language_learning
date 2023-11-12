from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from loguru import logger


class ExerciseAPIListPagination(PageNumberPagination):
    page_query_param = 'page'
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 10000


    def get_paginated_response(self, data):
        total_pages = self.page.paginator.num_pages
        page_range = list(self.page.paginator.page_range)

        return Response({
            'current_page_number': self.page.number,
            'last_page_number': total_pages,
            'results': data
        })
