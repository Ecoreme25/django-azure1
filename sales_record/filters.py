import django_filters
from .models import Sales
from django_filters import FilterSet, NumberFilter
from rest_framework import filters

class PendSalesPayFilterBackend(filters.BaseFilterBackend):
     def filter_queryset(self, request, queryset, view):
        return queryset.filter(amount__gt=0) # filter || exclude => status='Pending'
        #return queryset.filter(owner=request.user)
     

class SalesFilter(django_filters.FilterSet):

    # # Exact match (default behavior)
    # amount = NumberFilter(field_name='amount')

    # # Greater than
    # amount__gt = NumberFilter(field_name='amount', lookup_expr='gt')

    # # Less than
    # amount__lt = NumberFilter(field_name='amount', lookup_expr='lt')

    # # Range (between two values)
    # amount__range = NumberFilter(field_name='amount', lookup_expr='range')


    class Meta:
        model = Sales
        #fields = ('product_name', 'customer_name', 'quantity', 'amount', created_at')
        #fields = ['amount','amount__gt', 'amount__lt', 'amount__range']
        fields = {
            'product_name': ['iexact', 'icontains'],
            'customer_name': ['iexact', 'icontains'],
            'quantity': ['iexact', 'icontains'],
            'amount': ['iexact', 'icontains', 'lt', 'gt','range'],
            'created_at': ['iexact', 'year__gt'],
        }

        