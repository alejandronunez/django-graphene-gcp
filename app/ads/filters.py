""""FilterSet of ads app"""
import django_filters
from ads.models import Ad


class AdFilter(django_filters.FilterSet):
    """Ad Filter"""

    class Meta:
        model = Ad
        fields = ['title', 'description', 'subcategory', 'price', 'name', 'email', 'phone']
