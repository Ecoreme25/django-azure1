from django.contrib import admin
from .models import Sale, SaleItem, Product, Payment, InventoryLog

# Register your models here.
admin.site.register(SaleItem)
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(InventoryLog)