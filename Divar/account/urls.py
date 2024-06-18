from django.contrib import admin
from django.urls import path, include


app_name = "account"
urlpatterns = [
    path('api-vi/',include('account.api_vi.urls', namespace='account_api') )
]