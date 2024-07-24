from django.db import models
# from ..account.models.account import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
import json

User = get_user_model()
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    

class RealEstate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'real_user')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name = 'real_cat')
    title =models.CharField(max_length=250,blank=True,null=True)
    description =models.TextField(blank=True,null=True)

    def get_real_estate_images(self):
            domain_url = settings.DOMAIN_URL
            images_url = []
            for profile_image in self.real_estate_image.all():
                images_url.append( {'image':domain_url+profile_image.image.url})
            return json.dumps(images_url)

    class PropertyType(models.TextChoices):
     # Actual value ↓      # ↓ Displayed on Django Admin 
         
        APARTMENT = 'Apartment', 'apartment'
        HOUSE = 'House', 'house'
        VILLA = 'Villa', 'villa'
        STUDIO = 'Studio', 'studio'
        PENTHOUSE = 'Penthouse', 'penthouse'
        RESIDENCE = 'Residence', 'residence'
        UNDERCONSTRUCTIONBUILDING = 'Under Construction Building', 'under construction building'
        LAND = 'Land', 'land'
        COMMERCIALPROPERTY = 'Commercial Property', 'commercial property'
        WAREHOUSE = 'Warehouse', 'warehouse'

    Propertytype = models.CharField(
        max_length=150,
        choices=PropertyType.choices,
        default=PropertyType.APARTMENT
    )
    class TitleDeedType(models.TextChoices):
     
        TURKISHTITLEDEED = 'Turkish Title Deed', 'turkish title deed'
        EQUIVALENTTITLEDEED = 'Equivalent Title Deed', 'equivalent title deed'
        FOREIGNTITLEDEED = 'Foreign Title Deed', 'foreign title deed'
        STATESOCIALHOUSING = 'State Social Housing', 'state social housing'
        MARTYRCHILD = 'Martyr Child ', 'martyr child'
        ALLOCATION = 'Allocation', 'allocation'
        VETERANPOINTS = 'Veteran Points', 'veteran points'
        LEASEHOLD = 'Leasehold', 'leasehold'
      

    TitleDeedType = models.CharField(
        max_length=150,
        choices=TitleDeedType.choices,
        default=TitleDeedType.TURKISHTITLEDEED
    )
 
    Price = models.DecimalField(max_digits=150,decimal_places=2,default=0)

    Size = models.DecimalField(max_digits=150,decimal_places=2,default=0)

    class NumberOfBedrooms(models.TextChoices):
     
        STUDIO = 'Studio', 'studio'
        ONEBEDROOM = '1 Bedroom', '1 bedroom'
        TWOBEDROOM = '2 Bedrooms', '2 bedrooms'
        THREEBEDROOM = '3 Bedrooms', '3 bedrooms'
        FOURBEDROOM = '4 Bedrooms', '4 bedrooms'
        FIVEPLUSBEDROOM = '5+ Bedrooms', '5+ bedrooms'
      

    NumberOfBedrooms = models.CharField(
        max_length=150,
        choices=NumberOfBedrooms.choices,
        default=NumberOfBedrooms.ONEBEDROOM
    )

    class FurnishingStatus(models.TextChoices):
     
        UNFURNISHED = 'Unfurnished', 'unfurnished'
        PARTIALLYFURNISHED = 'Partially Furnished', 'partially furnished'
        FURNISHED = 'Furnished', 'furnished'
        ONLYWHITEGOODS = 'Only White Goods', 'only white goods'
      
      

    FurnishingStatus = models.CharField(
        max_length=150,
        choices=FurnishingStatus.choices,
        default=FurnishingStatus.UNFURNISHED
    )
    class Status(models.TextChoices):
        UNUSED = 'Unused', 'unused'
        USED = 'Used', 'used'
    

    Status = models.CharField(
        max_length=150,
        choices=Status.choices,
        default=Status.UNUSED
    )
    City =models.CharField(max_length=300,blank=True,null=True)
    Visit_count =models.IntegerField(default=0)
    Is_show = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    admin_message = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.title + self.user.email)






class Car(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'car_user')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name = 'car_cat')
    title =models.CharField(max_length=250,blank=True,null=True)
    description =models.TextField(blank=True,null=True)

    def get_car_images(self):
        domain_url = settings.DOMAIN_URL
        images_url = []
        for profile_image in self.car_image.all():
            images_url.append( { "image" :domain_url+profile_image.image.url})
        return json.dumps(images_url)

    class BodyType(models.TextChoices):
     
        CABRIOLET = 'cabriolet', 'cabriolet'
        COUPE = 'coupe', 'coupe'
        HATCHBACK5DOOR = 'hatchback-5-Door', 'hatchback 5 door'
        HATCHBACK3DOOR = 'Hatchback-3-Door', 'hatchback 3 door'
        SEDAN = 'sedan', 'sedan'
        STATIONWAGON = 'stationwagon', 'stationwagon'
        SUV = 'suv', 'suv'
    
    
    
    BodyType = models.CharField(
        max_length=150,
        choices=BodyType.choices,
        default=BodyType.CABRIOLET
    )

    Mileage = models.DecimalField(max_digits=150,decimal_places=2,default=0)


    class FuelType(models.TextChoices):
     
        PETROL = 'Petrol', 'petrol'
        DIESEL = 'Diesel', 'diesel'
        ELECTRIC = 'Electric', 'electric'
        HYBRID = 'Hybrid', 'hybrid'
        
    
    
    
    FuelType = models.CharField(
        max_length=150,
        choices=FuelType.choices,
        default=FuelType.PETROL
    )


    class TransmissionType(models.TextChoices):
     
        MANUAL = 'Manual', 'manual'
        AUTOMATIC = 'Automatic', 'automatic'
        SEMIAUTOMATIC = 'Semi-Automatic', 'semi-automatic'
      
    
    
    TransmissionType = models.CharField(
        max_length=150,
        choices=TransmissionType.choices,
        default=TransmissionType.MANUAL
    )
    class Status(models.TextChoices):
        UNUSED = 'Unused', 'unused'
        USED = 'Used', 'used'
    

    Status = models.CharField(
        max_length=150,
        choices=Status.choices,
        default=Status.UNUSED
    )
    Price = models.DecimalField(max_digits=150,decimal_places=2,default=0)
    City =models.CharField(max_length=300,blank=True,null=True)
    Visit_count =models.IntegerField(default=0)
    Is_show = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    admin_message = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.title + self.user.email)


class OthersAds(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='otherad_user')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name = 'otherad_cat')
    title =models.CharField(max_length=250,blank=True,null=True)
    description =models.TextField(blank=True,null=True)
    def get_other_images(self):
            domain_url = settings.DOMAIN_URL
            images_url = []
            for profile_image in self.other_image.all():
                images_url.append( {'image':domain_url+profile_image.image.url})
            return json.dumps(images_url)
    
    class PropertyType(models.TextChoices):
        DIGITALGOODS = 'Digital Goods', 'digital goods'
        KITCHEN = 'Kitchen', 'kitchen'
        INTERTAINMENT = 'Intertainment', 'intertainment'
        PERSONALITEMS = 'Personal Items', 'personal items'
        

    Propertytype = models.CharField(
        max_length=150,
        choices=PropertyType.choices,
        default=PropertyType.DIGITALGOODS
    )
    Price = models.DecimalField(max_digits=150,decimal_places=2,default=0)
    class Status(models.TextChoices):
        UNUSED = 'Unused', 'unused'
        USED = 'Used', 'used'
    

    Status = models.CharField(
        max_length=150,
        choices=Status.choices,
        default=Status.UNUSED
    )
    City =models.CharField(max_length=300,blank=True,null=True)
    Visit_count =models.IntegerField(default=0)
    Is_show = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    admin_message = models.TextField(blank=True,null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.title + self.user.email)



import os
def image_upload_to_car(instance, filename):
    file_dir = instance.car.user.email.split('@')[0]
    print('-----------------------------------', os.getcwd())
    return f"advertisements/cars/{file_dir}/{filename}"

class CarImage(models.Model):
    car = models.ForeignKey(Car,on_delete=models.CASCADE,related_name='car_image')
    image = models.ImageField(upload_to=image_upload_to_car, blank=True, null=True)

    def __str__(self):
        return str(self.car.title)
    


import os

def image_upload_to_real_estate(instance, filename):
    file_dir = instance.real_estate.user.email.split('@')[0]
    print('-----------------------------------', os.getcwd())
    return f"advertisements/real_estate/{file_dir}/{filename}"

class RealEstateImage(models.Model):
    real_estate = models.ForeignKey(RealEstate,on_delete=models.CASCADE,related_name='real_estate_image')
    image = models.ImageField(upload_to=image_upload_to_real_estate, blank=True, null=True)

    def __str__(self):
        return str(self.real_estate.title)
    

def image_upload_to_other(instance, filename):
    file_dir = instance.other.user.email.split('@')[0]
    print('-----------------------------------', os.getcwd())
    return f"advertisements/other/{file_dir}/{filename}"

class OtherImage(models.Model):
    other = models.ForeignKey(OthersAds,on_delete=models.CASCADE,related_name='other_image')
    image = models.ImageField(upload_to=image_upload_to_other, blank=True, null=True)

    def __str__(self):
        return str(self.other.title)


class Message(models.Model):
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='message_sender')
    context = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.context)

class CarConversation(models.Model):
    car_ad = models.ForeignKey(Car,on_delete=models.CASCADE,related_name='car_conversation')
    starter =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='car_starter_conv')
    messages = models.ManyToManyField(Message)

class RealEstateConversation(models.Model):
    realestate_ad = models.ForeignKey(RealEstate,on_delete=models.CASCADE,related_name='realestate_conversation')
    starter =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='realestate_starter_conv')
    messages = models.ManyToManyField(Message)

class OtherConversation(models.Model):
    other_ad = models.ForeignKey(OthersAds,on_delete=models.CASCADE,related_name='other_conversation')
    starter =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='other_starter_conv')
    messages = models.ManyToManyField(Message)


# from django_resized import ResizedImageField

# User = get_user_model()

# class Conversation(models.Model):
#     starter = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
#     )
#     receiver = models.ForeignKey(
#         User, on_delete=models.SET_NULL, null=True, related_name="convo_receiver"
#     )
#     start_time = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return f"{self.starter.username}"


# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL,
#                               null=True, related_name='message_sender')
#     text = models.CharField(max_length=200, blank=True)
#     attachment = ResizedImageField(force_format='WEBP', size=None,scale=0.5, quality=75, upload_to='chats/images/', blank=True, null=True)
#     conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message_conversation")
#     timestamp = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         ordering = ('-timestamp',)

#     def __str__(self) -> str:
#         return f"{self.conversation}_{self.sender}"