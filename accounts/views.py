from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .utils import send_code_to_user
from .serializers import UserRegisterSerializer, LoginSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer, LogoutUserSerializer, VerifyEmailSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import OneTimePassword, User
from rest_framework.permissions import IsAuthenticated
from django.utils.http import urlsafe_base64_decode 
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# Create your views here.

class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer

    def post(self, request):
        user_data=request.data
        print("Touched view 1")
        serializer=self.serializer_class(data=user_data)
        print("Touched view 2a")
        if serializer.is_valid(raise_exception=True):   # Calls the validate function inside the serializers class. If serializer.is_valid() hasn't been called before serializer.save(), a RuntimeError is raised:
            print("Touched view 2b")
            serializer.save() # In DRF, the serializer.save() method is used to save the validated data of a serializer instance into the database. See more below.
            print("Touched view 3")
            user=serializer.data
            send_code_to_user(user['email']) # In production, you can send the email with celery to avoid delay
            #send email function user['email']
            #print(user)
            user_fname = user['first_name']
            print("Touched view 4")
            return Response({
                'data':user,
                'message':f'hi {user_fname} thanks for signing up. A passcode has been sent to the email provided'
            }, status=status.HTTP_201_CREATED)            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserEmail(GenericAPIView):
    serializer_class=VerifyEmailSerializer
    
    def post(self, request):
        otpcode=request.data.get('otp')
        try:
            user_code_obj=OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    'message':'Account email verified successfully'
                }, status=status.HTTP_200_OK)
            return Response({
                'message':'Code is invalid, user already verified'
            }, status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({'message':'Passcode not provided'}, status=status.HTTP_404_NOT_FOUND)
        

class LoginUserView(GenericAPIView):
    serializer_class=LoginSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request}) # context={'request': request}: Adds the request object to the serializer's context. The context dictionary allows you to pass additional information to the serializer that might be needed during its operation (e.g., custom validation, dynamic fields).
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class TestAuthenticationView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        data={
            'msg':'It works'
        }
        return Response(data, status=status.HTTP_200_OK)


class PasswordResetRequestView(GenericAPIView):
    serializer_class=PasswordResetRequestSerializer
    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response({
            'message':"A link has been sent to your email to reset your password.",          
        }, status=status.HTTP_200_OK)
    

class PasswordResetConfirm(GenericAPIView):  # Users will be directed here when they click the reset password link
    def get(self, request, uidb64, token): # Valid the uidb64 and token, get the user id from them then query for the user object
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token): # Check if the user is the owner of the token and it has not expired
                return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)
            return Response({'success':True, 'message':'Credential is valid', 'uidb64':uidb64,'token':token}, status=status.HTTP_200_OK)            

        except DjangoUnicodeDecodeError:
            return Response({'message':'token is invalid or has expired'},status=status.HTTP_401_UNAUTHORIZED)


class SetNewPassword(GenericAPIView):
    serializer_class=SetNewPasswordSerializer
    def patch(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message':'Password reset successful'}, status=status.HTTP_200_OK)
    
class LogoutUserView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes=[IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)



# The behavior of serializer.save() depends on whether the serializer is creating a new instance or updating an existing one.
# a. Creating a New Object
# If the serializer is working with new data (serializer.data), it calls the create() method of the serializer.
# Example:
# def create(self, validated_data):
#     return MyModel.objects.create(**validated_data)
# The create() method must be defined in the serializer or inherited from a parent serializer.
# b. Updating an Existing Object
# If the serializer is bound to an existing instance (e.g., passed via serializer = MySerializer(instance=existing_obj, data=new_data)), it calls the update() method of the serializer.
# Example:
# def update(self, instance, validated_data):
#     instance.field = validated_data.get('field', instance.field)
#     instance.save()
#     return instance
# >>>You must define the update() method if the default behavior is insufficient.