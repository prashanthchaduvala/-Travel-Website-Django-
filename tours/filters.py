import django_filters
from .models import Tour

class TourFilter(django_filters.FilterSet):
    price = django_filters.OrderingFilter(
        fields=(('price', 'price'),),
        label='Sort by Price',
        field_labels={'price': 'Price'},
    )

    class Meta:
        model = Tour
        fields = ['country', 'days', 'food_types']
