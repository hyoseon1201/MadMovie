from django_filters import rest_framework as filters, BaseInFilter, NumberFilter
from rest_framework.filters import SearchFilter

from movies.models import Movie

class NumberInFilter(BaseInFilter, NumberFilter):
    pass

class MovieFilter(filters.FilterSet):
    genres = NumberInFilter(field_name='genres__id')

    class Meta:
        model = Movie
        fields = ['genres']

class CustomSearchFilter(SearchFilter):
    def get_search_terms(self, request):
        params = super().get_search_terms(request)
        terms = [param.replace(' ', '') for param in params]
        return terms
