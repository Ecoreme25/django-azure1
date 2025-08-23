import uuid
from django.db import models

# Create your models here.


class Sales(models.Model):
    # id = models.AutoField(primary_key=True)
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #import uuid
    
    product_name = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100, db_index=True)
    quantity =  models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #description = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Sold {self.product_name} to {self.customer_name} for {self.amount} at {self.created_at} with the status {self.status}"
    



# class Order(models.Model):
#     user = models.ForeignKey("auth.User", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['user', 'created_at']),  # Composite index
#         ]
