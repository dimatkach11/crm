import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

class OrederFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte') # month/day/year ex. 08/22/2020
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')

    note = CharFilter(field_name='note', lookup_expr='icontains')
    
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']