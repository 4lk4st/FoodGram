from rest_framework.pagination import PageNumberPagination


class FoodPageLimitPaginator(PageNumberPagination):

    page_size_query_param = 'limit'
