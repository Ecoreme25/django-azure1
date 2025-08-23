from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


from rest_framework import generics
from accounts.models import User
from .models import Sales
from .serializers import SalesSerializer
from .filters import SalesFilter, PendSalesPayFilterBackend
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsEmployee, IsCustomer

from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class SalesListCreateView(generics.ListCreateAPIView):
    queryset = Sales.objects.order_by('pk')
    serializer_class = SalesSerializer
    #permission_classes = [IsAuthenticated] # With the get_queryset below, you can use the if statement to specify custom actions for each user role
    #permission_classes = [IsAuthenticated, IsAdmin] 
    

    # View formating
    filterset_class = SalesFilter
    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
        PendSalesPayFilterBackend
    ]
    search_fields = ['=product_name', 'customer_name'] # Perform case-insensitive partial matches simultaneously for all the specified fields. It's drf built-in, thus you don't need to install Django filter before using this
    #filterset_fields = ('product_name', 'customer_name', 'quantity', 'amount')
    ordering_fields = ['product_name', 'customer_name', 'amount']
    
    #####pagination_class = LimitOffsetPagination
    # pagination_class = PageNumberPagination # None
    # pagination_class.page_size = 3
    # pagination_class.page_query_param = 'SalesListNum'
    # pagination_class.page_size_query_param = 'size' # Set the page size manually
    # pagination_class.max_page_size = 8

    # cache
    # @method_decorator(cache_page(60 * 15, key_prefix='sales_list'))   # Check if there's a cached response, then return it (don't go here: def get_queryset(self) at all), else go get it from the db
    # @method_decorator(vary_on_headers("Authorization"))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)


    def get_queryset(self):
        import time
        #time.sleep(2) # Remove for production
        return super().get_queryset()


    # def get_queryset(self):
    #     import time
    #     time.sleep(2) # Remove for production
    #     qs = super().get_queryset()
    #     if self.request.user.role == 'admin':
    #         qs = qs.filter(amount = 60000)
    #     if self.request.user.role == 'customer':
    #         qs = qs.filter(amount = 12000)
    #     return qs


class SalesRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sales.objects.all()
    serializer_class = SalesSerializer



# class SalesListCreateView(generics.ListCreateAPIView):
#     queryset = Sales.objects.order_by('pk')
#     serializer_class = SalesSerializer


    
# class SalesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer


# from django.core.cache import cache
# from rest_framework.views import APIView
# from rest_framework.response import Response

# class ProductListView(APIView):
#     def get(self, request):
#         cache_key = 'product_list'
#         data = cache.get(cache_key)
#         if not data:
#             data = list(Product.objects.values('name', 'price'))
#             cache.set(cache_key, data, timeout=60 * 15)  # Cache for 15 minutes
#         return Response(data)







#===========================================================================
# class SalesListCreateView(generics.ListCreateAPIView):
#     queryset = Sales.objects.order_by('pk')
#     serializer_class = SalesSerializer
#     permission_classes = [IsAuthenticated] # With the get_queryset below, you can use the if statement to specify custom actions for each user role
#     #permission_classes = [IsAuthenticated, IsAdmin] # With the get_queryset below, you can use the if statement to specify custom actions for each user role


#     # View formatiing
#     filterset_class = SalesFilter
#     filter_backends = [
#         DjangoFilterBackend, 
#         SearchFilter,
#         OrderingFilter,
#         PendSalesPayFilterBackend
#     ]
#     search_fields = ['=product_name', 'customer_name'] # Perform case-insensitive partial matches simultaneously for all the specified fields. It's drf built-in, thus you don't need to install Django filter before using this
#     #filterset_fields = ('product_name', 'customer_name', 'quantity', 'amount')
#     ordering_fields = ['product_name', 'customer_name', 'amount']
    
#     #####pagination_class = LimitOffsetPagination
#     # pagination_class = PageNumberPagination # None
#     # pagination_class.page_size = 3
#     # pagination_class.page_query_param = 'SalesListNum'
#     # pagination_class.page_size_query_param = 'size' # Set the page size manually
#     # pagination_class.max_page_size = 8


#     def get_queryset(self):
#         qs = super().get_queryset()
#         if self.request.user.role == 'admin':
#             qs = qs.filter(amount = 60000)
#         if self.request.user.role == 'customer':
#             qs = qs.filter(amount = 12000)
#         return qs


# class SalesRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Sales.objects.all()
#     serializer_class = SalesSerializer



# @method_decorator(cache_page(60 * 60 * 2))
