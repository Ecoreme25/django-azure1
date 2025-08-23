from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from sales_record.models import Sales
from django.core.cache import cache


@receiver([post_save, post_delete], sender=Sales)
def invalidate_product_cache(sender, instance, **kwargs):
    """
    Invalidate product list caches when a product is created, updated, deleted
    """
    print("Clearing product cache")

    # Clear  sales list caches
    cache.delete_pattern('*sales_list*') # You need to install django-redis package for this bcos it's not available in the django native redis backend
                                         # Use wildcard before and after "sales_list" => "*sales_list*" to remove all values with key_prefix "sales_list" from the redis db
    