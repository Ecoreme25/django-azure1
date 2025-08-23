from google.auth.transport import requests
from google.oauth2 import id_token # We will use this to verify the token
from accounts.models import User
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed


class Google():
    @staticmethod
    def validate(access_token):
        try:
            id_info=id_token.verify_oauth2_token(access_token, requests.Request()) # id_info: This is the result of the verification process. It typically contains the decoded claims from the token, such as the user's ID, email, and other information.
            if "accounts.google.com" in id_info['iss']: # Checking if the key contains accounts.google.com meaning it's coming from google https://accounts.google.com. Check below.
                return id_info
        except Exception as e:
            return "token is invalid or has expired"
        

    def login_social_user(email, password):
        user=authenticate(email=email, password=password)
        user_tokens=user.tokens()
        return{
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh'))
        }

    def register_social_user(provider, email, first_name, last_name):
        user=User.objects.filter(email=email)
        # Log in the user if the user exists and using Google as the provider
        if user.exists():
            if provider == user[0].auth_provider:  # Checking if provider is Google since the variable "provider" is already set to "google" inside the serializer
                Google.login_social_user(email, settings.SOCIAL_AUTH_PASSWORD)     
            else:
                raise AuthenticationFailed(
                    detail=f"Please continue your login with {user[0].auth_provider}" # Telling the user to continue the login with their correct provider
                )
        
         # If the user does not exist, register and log in the user (Note: Set is_verified to True as the email has been auto verified)
        else:
            new_user={
                'email':email,
                'first_name':first_name,
                'last_name':last_name,
                'password':settings.SOCIAL_AUTH_PASSWORD
            }
            register_user=User.objects.create_user(**new_user)
            register_user.auth_provider=provider
            register_user.is_verified=True
            register_user.save() # Save and log in the user
            Google.login_social_user(email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD)





# if "accounts.google.com" in id_info['iss']
# The code snippet if "accounts.google.com" in id_info['iss']: is checking whether the string "accounts.google.com" is present within the value associated with the key 'iss' in the id_info dictionary.

# Explanation:
# id_info is assumed to be a dictionary.

# id_info['iss'] retrieves the value associated with the key 'iss' (which typically stands for "issuer" in contexts like JWT tokens).

# "accounts.google.com" in id_info['iss'] checks if the string "accounts.google.com" is a substring of the value stored in id_info['iss'].

# Common Use Case:
# This kind of check is often used in authentication flows, particularly when verifying the issuer of an ID token (e.g., in OAuth or OpenID Connect). For example, if you're working with Google Sign-In or Google OAuth, the issuer (iss) of the token should be "accounts.google.com" or "https://accounts.google.com".

# For example
# id_info = {
#     'iss': 'https://accounts.google.com',
#     'sub': '1234567890',
#     'email': 'user@example.com'
# }






# KEEP
                # user=authenticate(email=email, password=settings.SOCIAL_AUTH_PASSWORD)
                # user_tokens=user.tokens()
                # return{
                #     'email':user.email,
                #     'full_name':user.get_full_name,
                #     'access_token':str(user_tokens.get('access')),
                #     'refresh_token':str(user_tokens.get('refresh'))
                # }






            # user=authenticate(email=register_user.email, password=settings.SOCIAL_AUTH_PASSWORD)
            # user_tokens=user.tokens()
            # return{
            #     'email':user.email,
            #     'full_name':user.get_full_name,
            #     'access_token':str(user_tokens.get('access')),
            #     'refresh_token':str(user_tokens.get('refresh'))
            # }