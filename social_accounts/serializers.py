from rest_framework import serializers
from .utils import Google
from .github import Github
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed, ValidationError


class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)

    def validate_access_token(self, access_token):
        google_user_data=Google.validate(access_token)
        try:
            userid=google_user_data["sub"] #Retrieve the userId from Google if the token is validated   
        except:
            raise serializers.ValidationError("This token is invalid or has expired.")
        
        if google_user_data['aud'] != settings.GOOGLE_CLIENT_ID: # The "aud"="audience" also contains the GOOGLE_CLIENT_ID
            raise AuthenticationFailed(detail="Could not verify user")
        # If everything is fine, we will retrieve the necessary information for the user from Google using the respective keys
        email=google_user_data['email']
        first_name=google_user_data['given_name']
        last_name=google_user_data['family_name']
        provider="google"
        return Google.register_social_user(provider, email, first_name, last_name)


class GithubOauthSerializer(serializers.Serializer):
    code = serializers.CharField(min_length=2)

    def validate_code(self, code):
        access_token=Github.exchange_code_for_token(code)
        if access_token:
            user=Github.retrieve_github_user(access_token)
            full_name=user['name']
            email=user['email']
            names=full_name.split(" ")
            firstName=names[1]
            lastName=names[0]
            provider="github"
            return Google.register_social_user(provider, email, firstName, lastName)        
        else:
            raise ValidationError("Token is invalid or has expired")

# Note:
# The value of "aud" in the ID token is equal to one of your app's client IDs. This check is necessary to prevent ID tokens issued to a malicious app being used to access data about the same user on your app's backend server.
# The value of "iss" in the ID token is equal to accounts.google.com or https://accounts.google.com.