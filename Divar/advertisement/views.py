from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status,permissions
from rest_framework.response import Response
from .models import  RealEstate, Car
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from account.models import Profile, SavedAds
from django.db.models import Q
from .utils import io
# Create your views here.
class CategoryView(APIView):
    serializer_class = CategorySerializer

    def get(self,request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories,many= True)
        return Response(serializer.data)

class RealEstateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        realestate = RealEstate.objects.all()
        serializer = RealEstateSerializer(realestate,many=True)
        return Response(serializer.data)

    def post(self,request):
        print('---------------------------', request.data)
        user = request.user
        if user == User.objects.get(id = request.data['user']):

            serializer = RealestateImagesSerializer( data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            return Response('ok')
        return Response('User is not allowed.')
    

class CarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request): 
        cars = Car.objects.filter(Q(Is_show=True) & Q(is_published = True) )
        serializer = CarSerializer(cars,many=True)
        return Response(serializer.data)

    def post(self,request):
        user = request.user
        print(user.id)
        if user == User.objects.get(id = request.data['user']):

            serializer = CarImagesSerializer( data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            return Response('ok')
        return Response('User is not allowed.')
    




class OtherAdsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        otherAds= OthersAds.objects.all()
        serializer = OtherAdsSerializer(otherAds,many=True)
        return Response(serializer.data)

    def post(self,request):
        user = request.user
        if user == User.objects.get(id = request.data['user']):

            serializer = OtherImagesSerializer( data= request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        
            return Response('ok')
        return Response('User is not allowed.')





class HomeView(APIView):

    def get(self,request):
        Cars = Car.objects.filter(Q(Is_show=True) & Q(is_published = True))
        RealStates = RealEstate.objects.filter(Q(Is_show=True) & Q(is_published = True))
        otherAds= OthersAds.objects.filter(Q(Is_show=True) & Q(is_published = True))
        car_serializer = CarSerializer(Cars,many=True)
        realstate_serializer = RealEstateSerializer(RealStates,many=True)
        otherAds_serializer = OtherAdsSerializer(otherAds,many =True)

        data = car_serializer.data + realstate_serializer.data + otherAds_serializer.data
        sorted_data = sorted(data, key=lambda x: x['created_date'], reverse=True)
        

        return Response({'All_ads':sorted_data})


class AdsDetailView(APIView):

    def get(self,request,category_name,id):

        if category_name =='car':
            add = Car.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = CarDetailSerializer(add)
            return Response(serializer.data)
        
        elif category_name =='realestate':
            add = RealEstate.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = RealEstateDetailSerializer(add)
            return Response(serializer.data)
        
        elif category_name =='other':
            add = OthersAds.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = OtherAdsDetailSerializer(add)
            return Response(serializer.data)
            
    
    def delete(self,request,category_name,id):

        if category_name =='car':
            add = Car.objects.get(id =id)
            user = request.user
            if add.user == user:
                add.Is_show = False
            add.save()
            return Response('add is deleted')
        
        elif category_name =='realestate':
            add = RealEstate.objects.get(id =id)
            user = request.user
            if add.user == user:
                add.Is_show = False
            add.save()
            return Response('add is deleted')
        
        elif category_name =='other':
            add = OthersAds.objects.get(id =id)
            user = request.user
            if add.user == user:
                add.Is_show = False
            add.save()
            return Response('add is deleted')
    

    def patch(self, request, category_name, id):
        if category_name == 'car':
            ad = Car.objects.get(id=id)
            if ad.user != request.user:
                return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer = CarImagesSerializer(ad, data=request.data, partial=True)
        
        elif category_name == 'realestate':
            ad = RealEstate.objects.get(id=id)
            if ad.user != request.user:
                return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer = RealestateImagesSerializer(ad, data=request.data, partial=True)
        
        elif category_name == 'other':
            ad = OthersAds.objects.get(id=id)
            if ad.user != request.user:
                return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            serializer = OtherImagesSerializer(ad, data=request.data, partial=True)
        
        else:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    


class SaveAdsView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self,request):
        user = request.user
        profile = Profile.objects.get(user=user)
        saved_ads = profile.Saved_Ads.all()
        saved_data = []
        for ad in saved_ads:
            
            if ad.category_name == 'car':
                serializer = CarSerializer(Car.objects.get(id=ad.ads_id))
                saved_data.append(serializer.data)
            
            if ad.category_name == 'realestate':
                serializer = RealEstateSerializer(RealEstate.objects.get(id=ad.ads_id))
                saved_data.append(serializer.data)

            if ad.category_name == 'other':
                serializer = OtherAdsSerializer(OthersAds.objects.get(id=ad.ads_id))
                saved_data.append(serializer.data)
        

        return Response({
                         'Saved_ads':saved_data})

   
            
    def post(self, request):
        profile = Profile.objects.get(user=request.user)
        if request.data['status']=='save':
            saved_ads = SavedAds.objects.create(user=request.user,category_name=request.data['category_name'], ads_id=request.data['ads_id'])
            profile.Saved_Ads.add(saved_ads)
            profile.save()
        if request.data['status'] == 'delete':
            
            print('----------------------------------------------------------', request.user)
            saved_ads = SavedAds.objects.filter(user=request.user, category_name=request.data['category_name'], ads_id=request.data['ads_id'])
            print('----------------------------------------------------------', saved_ads)

            if saved_ads.exists():
                profile.Saved_Ads.remove(saved_ads[0].id)
                profile.save()

        return Response('ok')



class SearchByCategoryView(APIView):
    
    
    def get(self, request, category_name, sub_name, *args, **kwargs):

        print('(((((())))))', category_name, sub_name)

        if category_name.lower() == 'car':
            adds = Car.objects.filter(Q(Is_show=True) & Q(is_published = True) & Q(BodyType=sub_name)).order_by('-id')
            serializer =CarSerializer(adds,many=True)
            

        elif category_name.lower() == 'realestate':
            print('pppppppppppppppppp', sub_name)
            real_state = RealEstate.objects.filter(Q(Is_show=True) & Q(is_published = True) & Q(Propertytype=sub_name)).order_by('-id')
            serializer = RealEstateSerializer(real_state,many=True)
            print('pppppppppppppppppp', real_state)

        
        elif category_name.lower() == 'other':
            other = OthersAds.objects.filter(Q(Is_show=True) & Q(is_published = True) & Q(Propertytype=sub_name)).order_by('-id')
            serializer = OtherAdsSerializer(other,many=True)

        
        if serializer.data:
            return Response(serializer.data)
        else:
            return Response('not_found')



class SearchAdsView(APIView):
    
    def post(self,request):
        title = request.data['title']
        city = request.data['city']
        sorted_data = get_data_by_search(title, city)
        


        return Response({'All_ads':sorted_data})


def get_data_by_search(title_name, city_name ):
    all_data = []
    car_ads = Car.objects.filter(Q(Is_show=True) & Q(is_published = True) &

        (Q(title__icontains=title_name)|Q(description__icontains=title_name) | Q(category__name__icontains=title_name) ) & (  Q(City= city_name) ) |
        (     Q( title__icontains=city_name) | Q( description__icontains=city_name)   )
        # |(Q(City=city_name) )
)


    car_ads_serializer = CarSerializer(car_ads,many = True)
    for data in car_ads_serializer.data:
        all_data.append(data)
    

    real_estate_ads = RealEstate.objects.filter(Q(Is_show=True) & Q(is_published = True) &

        (Q(title__icontains=title_name)|Q(description__icontains=title_name) | Q(category__name__icontains=title_name) ) & (  Q(City= city_name) ) |
        (     Q( title__icontains=city_name) | Q( description__icontains=city_name)   )

    )
    real_estate_ads_serializer = RealEstateSerializer(real_estate_ads,many = True)
    for data in real_estate_ads_serializer.data:
        all_data.append(data)
    


    other_ads = OthersAds.objects.filter(Q(Is_show=True) & Q(is_published = True) &

        (Q(title__icontains=title_name)|Q(description__icontains=title_name) | Q(category__name__icontains=title_name) ) & (  Q(City= city_name) ) |
        (     Q( title__icontains=city_name) | Q( description__icontains=city_name)   )

    )
    other_ads_serializer = OtherAdsSerializer(other_ads,many = True)
    for data in other_ads_serializer.data:
        all_data.append(data)

    sorted_data = sorted(all_data, key=lambda x: x['created_date'], reverse=True)
    print(sorted_data,'******&&&&&&&&%^$%')

    return sorted_data

class ConversationListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        user= request.user
         
        cars = Car.objects.filter(user=user)
        car_serializer = CarSerializer(cars,many=True)
        realestate = RealEstate.objects.filter(user=user)
        realestate_serializer = RealEstateSerializer(realestate,many = True)
        others = OthersAds.objects.filter(user=user)
        other_serializer = OtherAdsSerializer(others,many=True)
        admin_message_data = car_serializer.data + realestate_serializer.data + other_serializer.data
        sorted_messages_data = sorted(admin_message_data, key=lambda x: x['created_date'], reverse=True)


        data = []
        car_convs = CarConversation.objects.filter(Q(starter =user)| Q(ad__user=user))
        if car_convs:
            car_convs_serializer =CarConversationSerializer(car_convs,many=True)
            for car_conv in car_convs_serializer.data:
                data.append(car_conv)

        realestate_convs = RealEstateConversation.objects.filter(Q(starter =user)| Q(ad__user=user))
        if realestate_convs:
            realestate_convs_serializer =RealestateConversationSerializer(realestate_convs,many=True)
            for realestate_conv in realestate_convs_serializer.data:
                data.append(realestate_conv)
        other_convs = OtherConversation.objects.filter(Q(starter =user)| Q(ad__user=user))
        if other_convs:
            other_convs_serializer =OtherConversationSerializer(other_convs,many=True)
            for other_conv in other_convs_serializer.data:
                data.append(other_conv)
        
        sorted_data = sorted(data, key=lambda x: x['updated_at'], reverse=True)
        
        return Response({'conversation_list':sorted_data,
                         'admin_messages':sorted_messages_data})

class AdminMessageView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self,request,category_name,ad_id):

        if category_name =='car':
            add = Car.objects.get(id =ad_id)
            serializer = CarSerializer(add)
            return Response(serializer.data)
        
        elif category_name =='realestate':
            add = RealEstate.objects.get(id =ad_id)
            serializer = RealEstateSerializer(add)
            return Response(serializer.data)
        
        elif category_name =='other':
            add = OthersAds.objects.get(id =ad_id)
            serializer = OtherAdsSerializer(add)
            return Response(serializer.data)
            




class MessagesListView(APIView):

    def get(self,request,user_id,category_name,ad_id):

        if category_name == 'car':
            car_convs = CarConversation.objects.get(Q(starter_id=user_id) & Q(ad=ad_id))
            car_convs_serializer =CarConversationSerializer(car_convs)
            
            return Response({'messages':car_convs_serializer.data['messages']})
        
        if category_name == 'realestate':
            realestate_convs = RealEstateConversation.objects.get(Q(starter_id=user_id) & Q(ad=ad_id))
            realestate_convs_serializer =RealestateConversationSerializer(realestate_convs)
            
            return Response({'messages':realestate_convs_serializer.data['messages']})
        
        if category_name == 'other':
            other_convs = OtherConversation.objects.get(Q(starter_id=user_id) & Q(ad=ad_id))
            other_convs_serializer =OtherConversationSerializer(other_convs)
            
            return Response({'messages':other_convs_serializer.data['messages']})
            
 
