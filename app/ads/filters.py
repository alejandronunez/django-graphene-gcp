""""FilterSet of ads app"""
import django_filters
from ads.indices import AdDocument
from ads.models import Ad
from graphene_django.elasticsearch.filter import filters
from graphene_django.elasticsearch.filter.filterset import FilterSetES


class AdFilter(django_filters.FilterSet):
    """Ad Filter"""

    class Meta:
        model = Ad
        fields = ['title', 'description', 'subcategory', 'price', 'name', 'email', 'phone']


class AdFilterESAuto(FilterSetES):
    """ES filter for Ad"""

    class Meta(object):
        """Metaclass data"""
        index = AdDocument
        includes = ['title', 'description', 'subcategory', 'price', 'name', 'email', 'phone']
        order_by = ['id', 'price']


class AdFilterES(FilterSetES):
    """ES filter for Ad"""

    class Meta(object):
        """Metaclass data"""
        index = AdDocument
        order_by = ['id', 'price']
        includes = {
            'title': {},
            'description': {},
            'price': {
                'lookup_expressions': ['lte', 'gte', 'term']
            },
            'subcategory': {
                'id': {
                    'field_name': 'subcategory'
                },
                'name': {
                    'field_name': 'subcategory_name',
                    'lookup_expressions': ['term'],
                    'default_processor': 'term'
                },
                'parent_category_name': {
                    'field_name': 'category_name',
                    'lookup_expressions': ['term'],
                    'default_processor': 'term'
                },
                'parent_category_id': {
                    'field_name': 'category'
                },
            }
        }

    user_name = filters.StringFilterES(field_name='user_name', field_name_es="name", lookup_expressions=['contains'])
    email = filters.StringFilterES(field_name='email', lookup_expressions=['term', 'contains', 'regex', 'prefix'])
    phone = filters.StringFilterES(field_name='phone', lookup_expressions=['term', 'contains', 'regex', 'prefix'])
