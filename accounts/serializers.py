from rest_framework import serializers
from .models import User,OneTimePassword
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.urls import reverse
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, Token, TokenError

#Enter a valid email and Email used are checked with the Built-in EmailField and unique=True resp in the model
#Then the Passwords match check function below is used


class UserRegisterSerializer(serializers.ModelSerializer): # The ModelSerializer helps us to create a serializer and tie it to a model
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2=serializers.CharField(max_length=68, min_length=6, write_only=True)
    print("Touched Serializer 1")
    class Meta:
        print("Touched Serializer 2")
        model=User
        print("Touched Serializer 3")
        fields=['email', 'first_name', 'last_name', 'role', 'password', 'password2']
        # Add constraints here (check below)

    def validate(self, attrs):                                  # attrs is a dictionary containing the data being validated
        print("Touched Serializer 4")
        password=attrs.get('password', '')                      # ttrs.get('password', '') retrieves the value of the 'password' field from the dictionary. If the 'password' key is not found, it returns an empty string.
        password2=attrs.get('password2', '')                    
        if password != password2:
            print("Touched Serializer 5")
            raise serializers.ValidationError("Passwords do not match") #This is used.
        print("Touched Serializer 6")
        return attrs                                            # If the password validation passes, the method returns the attrs dictionary, allowing the serialization or deserialization process to continue.        
    
    def create(self, validated_data):
        print("Touched Serializer 7")
        user=User.objects.create_user(                          # Calls the create_user method inside the UserManager class inside managers.py
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            role=validated_data.get('role'),
            password=validated_data.get('password'),
        )
        print("Touched Serializer 8")
        return user
    

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=6)
    password=serializers.CharField(max_length=68, write_only=True)
    full_name=serializers.CharField(max_length=255, read_only=True)
    role=serializers.CharField(max_length=255, read_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model=User
        fields=['email', 'password', 'full_name', 'role', 'access_token', 'refresh_token']
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        user_tokens=user.tokens() # Calls the tokens function in the models.py file

        user = User.objects.get(email=email)
        role = user.role

        return {
            'email':user.email,
            'full_name':user.get_full_name,
            'role':role,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh'))
        }


class PasswordResetRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=255)

    class Meta:
        fields=['email']

    def validate(self, attrs):
        email=attrs.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email) # Get the user object where the email is equal the email provided
            uidb64=urlsafe_base64_encode(smart_bytes(user.id)) # Embed the userid into the code. Encode a bytestring to a base64 string for use in URLs. Strip any trailing equal signs.
            token=PasswordResetTokenGenerator().make_token(user) # Generate the final reset token. Return a token that can be used once to do a password reset for the given use.
            request=self.context.get('request') #  This line of code retrieves the HTTP request object from a context object. This request object contains valuable information about the incoming HTTP request, such as the HTTP method, URL path, headers, and request body.
            site_domain=get_current_site(request).domain # Domain of the frontend to receive the link
            relative_link=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token}) # This line of code is constructing a relative URL for a Django password reset confirmation view using Django's reverse() function
            abslink=f"http://{site_domain}{relative_link}"
            email_body=f"Hi, use the link below to reset your password \n {abslink}"
            data={
                'email_body':email_body,
                'email_subject':"Reset Your Password",
                'to_email':user.email
            }
            send_normal_email(data)
            
        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(write_only=True)
    token=serializers.CharField(write_only=True)

    class Meta:
        fields = ["password", "confirm_password", "uidb64", "token"]

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Reset link is invalid or has expired", 401)
            if password != confirm_password:
                raise AuthenticationFailed("Password do not match")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("Link is invalid or has expired")
        

class LogoutUserSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_messages={
        'bad_token':('Token is invalid or has expired')
    }

    def validate(self, attrs):
        self.token=attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')



class VerifyEmailSerializer(serializers.Serializer):
    otp = serializers.CharField()

    def validate_otp(self, value):
        try:
            otp_obj = OneTimePassword.objects.get(code=value)
        except OneTimePassword.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired OTP code.")

        user = otp_obj.user
        if user.is_verified:
            raise serializers.ValidationError("User is already verified.")

        # Attach user to serializer instance for use in the view
        self.user = user
        return value



# >>> User.objects.create_user():
# - This line uses the create_user() method of the User model to create a new user instance.
# - create_user() is a convenient method provided by Django's built-in AbstractUser or BaseUser classes. It usually handles password hashing securely.




# >>> relative_link=reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token':token})
# This line of code is constructing a relative URL for a Django password reset confirmation view using Django's reverse() function. Let's break it down:

# Explanation:
# relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
# reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

# reverse() is a Django function that generates a URL from a named URL pattern.
# 'password-reset-confirm' is the name of the URL pattern defined in urls.py.
# kwargs={'uidb64': uidb64, 'token': token} passes the necessary keyword arguments (UID and token) to build the URL.
# Arguments in kwargs

# uidb64: This is the base64-encoded user ID, which identifies the user requesting the password reset.
# token: This is a password reset token, typically generated by Django to ensure the request is valid.




# Example URL Generated:
# Assume uidb64 = "MTIz" (Base64 for "123") and token = "abcd1234xyz", the reverse() function will generate something like:

# /password-reset-confirm/MTIz/abcd1234xyz/
# How This Is Used
# This is typically used in Django's password reset workflow:

# A user requests a password reset.
# Django generates a password reset link containing uidb64 and token.
# The user clicks the link and is taken to a password reset form.

