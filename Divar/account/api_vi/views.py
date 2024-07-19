from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from mail_templated import EmailMessage
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenBlacklistView)
from .utils import (EmailThreading, get_tokens_for_user, create_verification_code ,hash_user_code)
import json
from rest_framework.permissions import IsAuthenticated
from advertisement.models import *
from advertisement.serializers import *

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

class ForgetPassAPIView(APIView):
    serializer_class = ForgetPassSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:    
            user = User.objects.get(username = serializer.validated_data['username'])
            code = create_verification_code()
            user.forget_code = code
            user.save()
            hash_code = hash_user_code(code)
            forget_email = EmailMessage('email/email_forget.html', 
                                    {'token':code}, 
                                    'djdivarr@gmail.com', 
                                    [user.email],
                                    )
        
            EmailThreading(forget_email).start()
            return Response({'detail':{'message':'A forget code is sent to your email address.',
                                       'hash_code':hash_code}})
        
            
        except: 
             return Response({'detail':{'message':'User does not exist, Please Sign-in first.'}}
                                 ,status=status.HTTP_404_NOT_FOUND)     
            

class ResetPassAPIView(APIView):
    serializer_class = ResetPassSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if user.forget_code == serializer.validated_data['forget_code']:
            user.set_password(serializer.validated_data['new_password'])
            return Response({'detail':{'message':'You successfully reset your password.'}})
        else:
            return Response({'detail':{'message':'Please enter your right code.'}})


class ProfileView(APIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated] 

    def get(self,request):
        user=request.user
        cars = Car.objects.filter(user=user, Is_show=True)
        real_states = RealEstate.objects.filter(user=user, Is_show=True)
        other_ads= OthersAds.objects.filter(user=user, Is_show=True)
        all_data = []
        if cars.exists():
            car_serializer = CarSerializer(cars,many=True)
            for data in car_serializer.data:
                all_data.append(data)
        
        if real_states.exists():
            realstate_serializer = RealEstateSerializer(real_states, many=True)
            for data in realstate_serializer.data:
                all_data.append(data) 
        

        if other_ads.exists():
            otherAds_serializer = OtherAdsSerializer(other_ads,many =True)
            for data in otherAds_serializer.data:
                all_data.append(data)

        sorted_data = sorted(all_data, key=lambda x: x['created_date'], reverse=True)
        profile = Profile.objects.get(user= request.user)
        profile.MyAds =sorted_data 


        profile.save()
        serializer= self.serializer_class(profile) 
        
        return Response(serializer.data)          










