from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from mail_templated import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenBlacklistView)
from .utils import (EmailThreading, get_tokens_for_user, create_verification_code )
import json

class UserRegistrationAPIView(APIView):
    serializer_class = UserRegistrationSerializer

    def post(self,request, *args, **kwargs):
        # print('----------*********************-----------', json.dumps(request.data))
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # send email to created user
        user = User.objects.get(username=serializer.validated_data['username'])
        code = create_verification_code()
        user.verification_code = code
        user.save()
        refresh_token , access_token = get_tokens_for_user(user, code)
        # print('-------------', user, "--------", code)


        verification_email = EmailMessage('email/email_varification.html', 
                                    {'token':code}, 
                                    'djdivarr@gmail.com', 
                                    [user.email],
                                    )
        
        EmailThreading(verification_email).start()
        return Response({ "detail":{
            'message':"sign up successfully",
            'refresh_token' : refresh_token,
            'access_token' : access_token,
            "user_id": user.id
            }
        },status=status.HTTP_201_CREATED)
    

class UserVerificationAPIView(APIView):
    serializer_class = UserVerificationSerializer

    def post(self,request):
        serializer =self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user =request.user
        if (not user.is_verified and user.verification_code  == serializer.validated_data['verification_code']):
            user.is_verified =True
            user.save()
            return Response({'detail':
                             {'message':"User is successfully verified."}})
        else:
            return Response({'detail':{'message':'User is verified before Or Please Enter the Correct Code'}})

class UserLoginView(TokenObtainPairView):

    serializer_class = UserLoginSerializer


class UserLogoutView(TokenBlacklistView):
   
    serializer_class = UserLogoutSerializer











# class YourModelView(APIView):
#     serializer_class = YourModelSerializer

#     def post(self, request):
#         serializer= self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         # send email to created user

#         return Response({
#             'message':"sign up successfully",
#         },status=status.HTTP_201_CREATED)       