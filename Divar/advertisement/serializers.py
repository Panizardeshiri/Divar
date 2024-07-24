from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class RealEstateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = serializers.CharField(source="get_real_estate_images")
    class Meta:
        model = RealEstate
        fields = '__all__'





class OtherAdsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = serializers.CharField(source="get_other_images")

    class Meta:
        model = OthersAds
        fields = '__all__'





class CarSerializer(serializers.ModelSerializer):
    category        = CategorySerializer()
    user            = UserSerializer()
    images = serializers.CharField(source="get_car_images")
    # car_ad_message = MessageToAdSerializer(many=True,read_only = True)
    admin_message = serializers.CharField()
    class Meta:
        model = Car
        # fields = ('id','images','category','user','car_ad_message')
        fields = '__all__'
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if not instance.is_published:
    #         representation['admin_message'] = (instance.admin_message, many=True).data
    #     else:
    #         representation.pop('admin_message',None)
    #     return representation



class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =CarImage
        fields = '__all__'


class CarImagesSerializer(serializers.ModelSerializer):

    car_image = CarImageSerializer(many = True, read_only = True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True)
        )
    class Meta:
        model = Car
        fields = ('user','category','title','car_image','uploaded_images','description','BodyType','Mileage','FuelType','TransmissionType','Status','Price','City')
        
    def create(self,validated_data):
        uploaded_images = validated_data.pop('uploaded_images')
        car = Car.objects.create(**validated_data)
        
        
        for image in uploaded_images:
            CarImage.objects.create(car=car, image = image)
        
        return car
    

class RealestateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =RealEstateImage
        fields = '__all__'


class RealestateImagesSerializer(serializers.ModelSerializer):

    real_estate_image = RealestateImageSerializer(many = True, read_only = True)
    real_estate_uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True)
        )
    class Meta:
        model = RealEstate
        fields = ('user', 'category','title','real_estate_image','real_estate_uploaded_images','Status','Price',
                  'City','Visit_count','Is_show','description','Propertytype','TitleDeedType','Size','NumberOfBedrooms','FurnishingStatus')
    
    def create(self,validated_data):
        real_estate_uploaded_images = validated_data.pop('real_estate_uploaded_images')
        real_estate = RealEstate.objects.create(**validated_data)
        
        
        for image in real_estate_uploaded_images:
            RealEstateImage.objects.create(real_estate=real_estate, image = image)
        
        return real_estate
    
class OtherImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherImage
        fields = '__all__'


class OtherImagesSerializer(serializers.ModelSerializer):

    other_image = OtherImageSerializer(many = True, read_only = True)
    other_uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True)
        )
    class Meta:
        model = OthersAds
        fields = ('user', 'category','title','Propertytype','other_image','other_uploaded_images','Status','Price','City','Visit_count','Is_show','description')
        
    def create(self,validated_data):
        other_uploaded_images = validated_data.pop('other_uploaded_images')
        other = OthersAds.objects.create(**validated_data)
        
        
        for image in other_uploaded_images:
            OtherImage.objects.create(other=other, image = image)
        
        return other
        




    












# class AdvertisementImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AdvertisementImage
#         fields = '__all__'


# class AdvertiseSerializer(serializers.ModelSerializer):
#     ad_image = AdvertisementImageSerializer(many = True, read_only = True)
#     uploaded_images = serializers.ListField(
#         child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True)
#         )
    
#     class Meta:
#         model = Advertisement
#         fields = ('name','category','user','uploaded_images','ad_image')

    
#     def create(self,validated_data):
#         uploaded_images = validated_data.pop('uploaded_images')
#         advertisement = Advertisement.objects.create(**validated_data)
        
        
#         for image in uploaded_images:
#             AdvertisementImage.objects.create(advertisement=advertisement, image = image)
        
#         return advertisement




