from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','id')

class RealEstateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = serializers.CharField(source="get_real_estate_images")
    class Meta:
        model = RealEstate
        fields = '__all__'

class RealestateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =RealEstateImage
        fields = '__all__'


class RealEstateDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = RealestateImageSerializer(many = True, read_only = True)
    

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


class OtherImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherImage
        fields = '__all__'


class OtherAdsDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    user = UserSerializer()
    images = OtherImageSerializer(many = True, read_only = True)
    

    class Meta:
        model = OthersAds
        fields = '__all__'


class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model =CarImage
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    category        = CategorySerializer()
    user            = UserSerializer()
    images = serializers.CharField(source="get_car_images")
    
    class Meta:
        model = Car
        fields = '__all__'
    
class CarDetailSerializer(serializers.ModelSerializer):
    category        = CategorySerializer()
    user            = UserSerializer()
    images = CarImageSerializer(many = True, read_only = True)
   
    class Meta:
        model = Car
        fields = '__all__'

    


class CarImagesSerializer(serializers.ModelSerializer):

    car_image = CarImageSerializer(many = True, read_only = True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True),
        allow_empty=True,
        required=False 
        )
    
    delete_images = serializers.ListField(
        child=serializers.IntegerField(),  # Assuming IDs are integers
        allow_empty=True,
        required=False
    )
    class Meta:
        model = Car
        fields = ('user','category','title','car_image','uploaded_images','description','BodyType','Mileage','FuelType','TransmissionType','Status','Price','City','delete_images')
        
    def create(self,validated_data):

        if validated_data.get('uploaded_images'):
            uploaded_images = validated_data.pop('uploaded_images')
            print('***&&&',uploaded_images)
            car = Car.objects.create(**validated_data)
        
            for image in uploaded_images:
                CarImage.objects.create(car=car, image = image)
        
        else:
            car = Car.objects.create(**validated_data)
        return car
    
    def update(self, instance, validated_data):
        uploaded_images = validated_data.pop('uploaded_images', [])
        delete_images = validated_data.pop('delete_images', [])

        # Update the fields of the Car instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete images specified in delete_images list
        if delete_images:
            CarImage.objects.filter(id__in=delete_images).delete()

        # Add new images
        if uploaded_images:
            for image in uploaded_images:
                CarImage.objects.create(car=instance, image=image)

        return instance
        

    # def update(self, instance, validated_data):
    #     uploaded_images = validated_data.pop('uploaded_images', [])

    #     # Update the fields of the Car instance
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()

    #     # Handle existing images (if needed, e.g., delete old images, or do nothing)
    #     # Here, we simply keep existing images and add new ones
    #     if uploaded_images:
    #         for image in uploaded_images:
    #             CarImage.objects.create(car=instance, image=image)

    #     return instance
    




class RealestateImagesSerializer(serializers.ModelSerializer):

    real_estate_image = RealestateImageSerializer(many = True, read_only = True)
    real_estate_uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000, allow_empty_file =True, use_url = False, write_only = True),
        allow_empty=True,  # This allows empty lists
        required=False 
        )
    
    delete_images = serializers.ListField(
        child=serializers.IntegerField(),  # Assuming IDs are integers
        allow_empty=True,
        required=False
    )
    class Meta:
        model = RealEstate
        fields = ('user', 'category','title','real_estate_image','real_estate_uploaded_images','Status','Price',
                  'City','description','Propertytype','TitleDeedType','Size','NumberOfBedrooms','FurnishingStatus','delete_images')
    
    def create(self,validated_data):

        if validated_data.get('real_estate_uploaded_images'):
            real_estate_uploaded_images = validated_data.pop('real_estate_uploaded_images')
            real_estate = RealEstate.objects.create(**validated_data)
            
            for image in real_estate_uploaded_images:
                RealEstateImage.objects.create(real_estate=real_estate, image = image)
        else:
            print('----------------------------------------77777777', validated_data)
            real_estate = RealEstate.objects.create(**validated_data)
        
        return real_estate
    

    def update(self, instance, validated_data):
        real_estate_uploaded_images = validated_data.pop('real_estate_uploaded_images', [])
        delete_images = validated_data.pop('delete_images', [])

        # Update the fields of the Car instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete images specified in delete_images list
        if delete_images:
            RealEstateImage.objects.filter(id__in=delete_images).delete()

        # Add new images
        if real_estate_uploaded_images:
            for image in real_estate_uploaded_images:
                RealEstateImage.objects.create(real_estate=instance, image=image)

        return instance
    
class OtherImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherImage
        fields = '__all__'


class OtherImagesSerializer(serializers.ModelSerializer):

    other_image = OtherImageSerializer(many = True, read_only = True)
    other_uploaded_images = serializers.ListField(
        child=serializers.ImageField(max_length =1000000,allow_empty_file =False, use_url = False, write_only = True),
        allow_empty=True,
        required=False 
        )
    
    delete_images = serializers.ListField(
        child=serializers.IntegerField(),  # Assuming IDs are integers
        allow_empty=True,
        required=False
    )
    class Meta:
        model = OthersAds
        fields = ('user', 'category','title','Propertytype','other_image','other_uploaded_images','Status','Price','City','description','delete_images')
        
    def create(self,validated_data):

        if validated_data.get('other_uploaded_images'):
            other_uploaded_images = validated_data.pop('other_uploaded_images')
            other = OthersAds.objects.create(**validated_data)
            
            
            for image in other_uploaded_images:
                OtherImage.objects.create(other=other, image = image)
        else:
            other = OthersAds.objects.create(**validated_data)
        return other
    

    def update(self, instance, validated_data):
        other_uploaded_images = validated_data.pop('other_uploaded_images', [])
        delete_images = validated_data.pop('delete_images', [])

        # Update the fields of the Car instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete images specified in delete_images list
        if delete_images:
            OtherImage.objects.filter(id__in=delete_images).delete()

        # Add new images
        if other_uploaded_images:
            for image in other_uploaded_images:
                OtherImage.objects.create(other=instance, image=image)

        return instance
        



class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()
    class Meta:
        model = Message
        fields = [ 'sender','context', 'created_at']


class CarConvSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = serializers.CharField(source="get_car_images")
    class Meta:
        model=Car
        fields ='__all__'

class CarConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many =True)
    ad = CarConvSerializer()
    class Meta:
        model = CarConversation
        fields  = ['id', 'ad', 'messages', 'starter', 'updated_at']


class RealestateConvSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = serializers.CharField(source="get_real_estate_images")
    class Meta:
        model=RealEstate
        fields = '__all__'

class RealestateConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many =True)
    ad = RealestateConvSerializer()
    class Meta:
        model = RealEstateConversation
        fields  = ['id', 'ad', 'starter', 'messages', 'updated_at']


class OtherConvSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = serializers.CharField(source="get_other_images")
    class Meta:
        model=OthersAds
        fields = "__all__"

class OtherConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many =True)
    ad = OtherConvSerializer()
    class Meta:
        model = OtherConversation
        fields  = ['id', 'ad', 'messages', 'starter', 'updated_at']





    














