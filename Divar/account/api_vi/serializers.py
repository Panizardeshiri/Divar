from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
import re
from rest_framework.response import Response
from ..models.profile import *
from advertisement.serializers import *
from django.contrib.auth import authenticate




User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        
class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)
    class Meta:
        model = User
        fields =[ 'username', 'password', 'password1']
    from decimal import Decimal
    def validate_username(self, attr):
            email_regex = '^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$'
            is_email    =  re.search(email_regex, attr)
            
            if not is_email:
                error_message = 'Enter valid Email!'
                raise serializers.ValidationError({ 'detail' : error_message })        
   
            return attr

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({'detail':'Password does not match'})
        try:
            validators.validate_password(password=attrs.get('password'))
        
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({ "detail": list(e.messages)})
        
        return super(UserRegistrationSerializer, self).validate(attrs)
    
    def create(self, validated_data):
       
        user = User.objects.create( 
                    username=validated_data['username'],            
                    email = validated_data['username']
                )
        

        user.set_password(validated_data['password'])
        user.save()
        return user
    

class UserVerificationSerializer(serializers.Serializer):
     verification_code = serializers.CharField(max_length=6)


    
class UserLoginSerializer(TokenObtainPairSerializer):
      def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Check if the user exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"detail": "Invalid password"})

        # Call the parent class's validate method to get tokens
        data = super().validate(attrs)

        # Add additional user details to the response
        data['username'] = user.username
        data['user_id'] = user.id
        data['access_exp'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data['refresh_exp'] = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        return data

    

class UserLogoutSerializer(TokenBlacklistSerializer):
    def validate(self, attrs):
        data = super(UserLogoutSerializer, self).validate(attrs)
        data['detail'] = "successfully logged out"

        return data



class ForgetPassSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=255)


class ResetPassSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=60)
    forget_code = serializers.CharField(max_length=6)
    new_password = serializers.CharField(max_length=250)
    new_password_confirm = serializers.CharField(max_length=250)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'detail':'Password does not match'})
        try:
            validators.validate_password(password=attrs.get('new_password'))
        
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({ "detail": list(e.messages)})
        
        return super(ResetPassSerializer, self).validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    Saved_Ads = serializers.SerializerMethodField()
    # My_Ads = serializers.SerializerMethodField()

    class Meta:
        model = Profile 
        fields = '__all__'


    def get_Saved_Ads(self, obj):
        saved_ads = obj.Saved_Ads.all()
        saved_data = []
        for ad in saved_ads:            
            if ad.category_name == 'car':
                cars = Car.objects.filter(id=ad.ads_id)
                if cars.exists():
                    print('((((((((((((((((()))))))))))))))))', cars[0])
                    serializer = CarSerializer(cars)
                    saved_data.append(serializer.data[0])
            
            if ad.category_name == 'real_estate':
                real_state = RealEstate.objects.filter(id=ad.ads_id)
                if real_state.exists():
                    serializer = RealEstateSerializer(real_state)
                    saved_data.append(serializer.data)

            if ad.category_name == 'other':
                other_ads = OthersAds.objects.filter(id=ad.ads_id)
                serializer = OtherAdsSerializer(other_ads)
                saved_data.append(serializer.data)
            
        # sorted_saved_data = sorted(saved_data, key=lambda x: x['created_date'], reverse=True)
        return saved_data
    
    # def get_My_Ads(self, obj):

    










