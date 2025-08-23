from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def email_validator(self, email):
        print("Touched manager 1")
        try:
            validate_email(email)
            print("Touched manager 2")
        except ValidationError:
            print("Touched manager 3")
            raise ValueError(_("Please enter a valid email address"))
        
    def create_user(self, email, first_name, last_name, role, password, **extra_fields):
        print("Touched manager 4")
        if email:
            email=self.normalize_email(email) # Normalize the email address and validate it
            self.email_validator(email)
            print("Touched manager 5")
        else:
            raise ValueError(_("An email address is required"))
        if not first_name:
            raise ValueError(_("First name is required"))
        if not last_name:
            raise ValueError(_("Last name is required"))
        print("Touched manager 6")
        user=self.model(email=email, first_name=first_name, last_name=last_name, role=role, **extra_fields)
        user.set_password(password) # Uses the set_password method to securely hash the password before saving the whole user object.
        user.save(using=self._db) # See below _db
        print("Touched manager 7")
        return user
    
    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        print("Touched manager 8")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_verified", True)
        print("Touched manager 9")

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Is staff must be true for admin user"))
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Is superuser must be true for admin user"))
        
        role='admin'

        print("Touched manager 10")
        user=self.create_user(
            email, first_name, last_name, role, password, **extra_fields
        )
        print("Touched manager 11")
        user.save(using=self._db) # Why do we need this line again since create_user has taken care of it
        print("Touched manager 12")
        return user
    



# Explanation of self._db:

# The underscore (_) in self._db is a common convention in Python for denoting private or protected attributes within a class. These attributes are typically meant for internal use by the class and its methods, and their access from outside the class might be restricted.
# In this case, self._db likely holds a database connection object that has been configured in your Django project's settings or within the UserManager class itself. This ensures that the user object is saved to the correct database connection, especially if you're working with multiple databases in your project.



        


        
        