from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from django.contrib.auth import get_user_model
from django.conf import settings
import re
from rest_framework.response import Response

User = get_user_model()



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

     class Meta:
        model = User
        fields =('verification_code',)

        



         
    
    

    
class UserLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        user = User.objects.get(username=attrs.get('username'))
        if not user:
            raise serializers.ValidationError({"detail": "No active account found with the given credentials"})

        try:
            data = super().validate(attrs)
        except:
            raise serializers.ValidationError({"detail": "Invalid password"})
        data['username'] = self.user.username
        data['access_exp'] = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        data['refresh_exp'] = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']
        return data




class UserLogoutSerializer(TokenBlacklistSerializer):
    def validate(self, attrs):
        data = super(UserLogoutSerializer, self).validate(attrs)

        data['detail'] = "successfully logged out"

        return data









# from ..models.account import YourModel

# class YourModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = YourModel
#         fields = ['id', 'name', 'data']