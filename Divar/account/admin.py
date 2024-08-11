from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.account import *
from .models.profile import *
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff','is_active',"is_verified")
    list_filter = ('email','is_staff','is_active', 'is_verified')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
       ('Authentication',{
           "fields":(
              'username', 'email','password' ,'verification_code','forget_code'
           ),
       }),
       ('permissions', {
           "fields": (
               'is_staff', 'is_active','is_superuser','is_verified', 'stars',

           ),
       }),
   )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser', 'stars', 'is_verified')}
         ),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(SavedAds)
