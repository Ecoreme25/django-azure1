from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, SaleItemViewSet, SaleViewSet, PaymentViewSet, InventoryLogViewSet  # CustomerViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
#router.register(r'customers', CustomerViewSet)
router.register(r'sale-item', SaleItemViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'inventory-logs', InventoryLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]