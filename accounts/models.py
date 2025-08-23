from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.


AUTH_PROVIDERS={'email':'email', 'google':'google', 'github':'github', 'facebook':'facebook'}
ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('customer', 'Customer'),
    ]


class User(AbstractBaseUser, PermissionsMixin):
    print("Touched Model 1")
    email=models.EmailField(max_length=255, unique=True, verbose_name=_("Email Address"))
    first_name=models.CharField(max_length=100, verbose_name=_("First Name")) # The translation of "First Name" is deferred until the model is used (check below).
    last_name=models.CharField(max_length=100, verbose_name=_("Last Name"))

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    auth_provider = models.CharField(max_length=50, default=AUTH_PROVIDERS.get("email"))

    USERNAME_FIELD="email" # is used when customizing the user authentication system to use the email address as the unique identifier for authentication instead of the default username field. This is common in projects where email-based login is preferred.
    print("Touched Model 2")
    REQUIRED_FIELDS=["first_name", "last_name"]

    objects= UserManager()
    print("Touched Model 3")

    def __str__(self): 
        return f"{self.email} - {self.first_name} {self.last_name} - {self.role}"

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def tokens(self):
        refresh=RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

    print("Touched Model 4")



class OneTimePassword(models.Model):
    print("Touched Model 5")
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    code=models.CharField(max_length=6, unique=True)

    def __str__(self):
        print("Touched Model 6")
        return f"{self.user.first_name}-passcode"
    



# Key Benefits:
# Performance: Improves performance by delaying translation until necessary.
# Maintainability: Makes your code more organized and easier to maintain for internationalization.
# Flexibility: Allows you to easily change translations without modifying other parts of your code.

# Create a custom model property to be used by e.g. the LoginSerializer class