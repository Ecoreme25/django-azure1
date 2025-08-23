from django.contrib import admin
from .models import User
from .models import OneTimePassword
# Register your models here.


admin.site.register(User)
admin.site.register(OneTimePassword)


# Super admin: admin1@gmail.com/Password321
