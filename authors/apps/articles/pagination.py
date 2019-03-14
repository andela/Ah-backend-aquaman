from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from collections import OrderedDict

class ArticlesLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 6
    max_limit = 50

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('articleCount', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('articles', data),
        ]))
