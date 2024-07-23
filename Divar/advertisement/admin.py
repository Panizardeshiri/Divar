from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(RealEstate)
admin.site.register(Car)
admin.site.register(OthersAds)
admin.site.register(CarImage)
admin.site.register(RealEstateImage)
admin.site.register(OtherImage)
