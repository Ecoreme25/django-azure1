from django.urls import path
from .views import SalesListCreateView, SalesRetrieveUpdateDestroyView

urlpatterns = [
    path('sales/', SalesListCreateView.as_view(), name='sales-list-create'),
    path('sales/<int:pk>/', SalesRetrieveUpdateDestroyView.as_view(), name='sales-retrieve-update-destroy'),
]

