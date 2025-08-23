from rest_framework.viewsets import ModelViewSet
from .models import Product, Sale, SaleItem, Payment, InventoryLog # Customer
from .serializers import ProductSerializer, SaleItemSerializer, SaleSerializer, PaymentSerializer, InventoryLogSerializer  # CustomerSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class CustomerViewSet(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     serializer_class = CustomerSerializer

class SaleItemViewSet(ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer

class SaleViewSet(ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class InventoryLogViewSet(ModelViewSet):
    queryset = InventoryLog.objects.all()
    serializer_class = InventoryLogSerializer