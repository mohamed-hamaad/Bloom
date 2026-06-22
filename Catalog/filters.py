import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter
from .models import *

import django_filters
from django_filters import CharFilter, NumberFilter
from .models import Product

class ProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains', label='Product Name')
    category = CharFilter(field_name='category', lookup_expr='icontains', label='Category')
    min_price = NumberFilter(field_name='price', lookup_expr='gte', label='Min Price')
    max_price = NumberFilter(field_name='price', lookup_expr='lte', label='Max Price')

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        # الحل السحري: بنلف على الـ fields اللي جوه الـ form الداخلي للمكتبة
        for field_name, field in self.form.fields.items():
            field.widget.attrs.update({
                'class': 'rounded-xl w-full px-4 py-2 border border-gray-300 focus:outline-none focus:border-dark text-sm tracking-wide bg-cream'
            })

    class Meta:
        model = Product
        fields = []