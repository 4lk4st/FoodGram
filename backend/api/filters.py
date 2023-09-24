from django_filters import rest_framework as filters


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')
