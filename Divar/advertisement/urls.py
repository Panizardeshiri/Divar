from django.contrib import admin
from django.urls import path, include
from .views import *


app_name = "advertisement"
urlpatterns = [
    path('Home/',HomeView.as_view(),name='Home'),
    path('category/',CategoryView.as_view(),name='category'),
    path('real-estate/',RealEstateView.as_view(),name='realstate'),
    path('car/',CarView.as_view(),name='car'),
    path('otherAds/',OtherAdsView.as_view(),name='otherAds'), 
    path('category/<str:category_name>/<str:sub_name>', SearchByCategoryView.as_view(), name='search-by-category'),
    path('saved-ads/', SaveAdsView.as_view(), name='saved_ads' ),
    path('ads-detail/<str:category_name>/<int:id>', AdsDetailView.as_view(), name='ads_detail'),
    path('search-ads/', SearchAdsView.as_view(), name='search_ads' ),
    path('carconversation-list/',ConversationListView.as_view(),name='carconversation_list'),
    path('messages-list/<int:user_id>/<str:category_name>/<int:ad_id>',MessagesListView.as_view(),name='messages_list'),
    # path('conversations/', ConverstationsView.as_view(), name='conversations'  ),
    # path('conversations/<str:username>/', ConversationMessageView.as_view(), name='conversation_messages'  ),
    # path('message-to-ad/<int:id>', MessageToAdView.as_view(), name='message_to_ad' ),



]