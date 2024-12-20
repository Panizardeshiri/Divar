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
    



def currency_to_usd(price_str):
    if 'USD' in price_str:
        return float(price_str.replace('USD', '').strip())
    elif 'EUR' in price_str:
        return float(price_str.replace('EUR', '').strip()) * 1.085 
    elif 'TRY' in price_str:
        return float(price_str.replace('TRY', '').strip()) * 0.029  
    return 0.0

def safe_float_price(ad):
    try:
        return currency_to_usd(ad.get('Price', '0'))
    except ValueError:
        return 0.0




def sort_ads(data, filter_type):
    if filter_type.lower() == 'newest':
        return sorted(data, key=lambda x: x['created_date'], reverse=True)
    elif filter_type.lower() == 'oldest':
        return sorted(data, key=lambda x: x['created_date'])
    elif filter_type.lower() == 'cheapest':
        return sorted(data, key=safe_float_price)
    elif filter_type.lower() == 'most_expensive':
        return sorted(data, key=safe_float_price, reverse=True)
    elif filter_type.lower() == 'least_visited':
        return sorted(data, key=lambda x: x['Visit_count'])
    elif filter_type.lower() == 'most_visited':
        return sorted(data, key=lambda x: x['Visit_count'], reverse=True)
    else:
        return data  # No filter applied

class FilterView(APIView):

    def get(self, request):
        filter_type = request.query_params.get('filter_type', None)
        # print('**',filter_type)

        # Fetch ads
        cars = Car.objects.filter(Q(Is_show=True) & Q(is_published=True))
        real_states = RealEstate.objects.filter(Q(Is_show=True) & Q(is_published=True))
        other_ads = OthersAds.objects.filter(Q(Is_show=True) & Q(is_published=True))

        car_serializer = CarSerializer(cars, many=True)
        realstate_serializer = RealEstateSerializer(real_states, many=True)
        otherAds_serializer = OtherAdsSerializer(other_ads, many=True)

        data = car_serializer.data + realstate_serializer.data + otherAds_serializer.data

        sorted_data = sort_ads(data, filter_type)

        return Response({'All_ads': sorted_data})


       

      






def chek_saved_ads_for_user(user, category, ad_id):
    if user.is_authenticated:
        
        saved_ads = SavedAds.objects.filter(Q(user=user) & Q( category_name__icontains = category))
        for ad in saved_ads:
            print('save ad id is: ', ad.ads_id, '--- ad is is : ', ad_id)
            if int(ad.ads_id) == int(ad_id):
                return True
        return False    
    else:
        return False

class AdsDetailView(APIView):

    def get(self,request,category_name,id):

        if category_name.lower() =='car':
            add = Car.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = CarSerializer(add)
            
        
        elif category_name.lower() =='realestate':
            add = RealEstate.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = RealEstateSerializer(add)

        
        elif category_name.lower() =='others':
            add = OthersAds.objects.get(id =id)
            add.Visit_count +=1
            add.save()
            serializer = OtherAdsSerializer(add)


        final_response = serializer.data.copy()
        if chek_saved_ads_for_user(request.user, add.category.name, add.id):
            final_response['is_saved'] = "true"
        else: 
            final_response['is_saved'] = "false"
        print('----------------',add.user.stars)

        if add.user.stars:
            if int(add.user.stars)  > 0 :
                final_response['is_star'] = "true"
        else :
            final_response['is_star'] = "false"
        
        return Response(final_response)
            
    
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
        print('----------------------------------------------------------', request.data)
        saved_ads = SavedAds.objects.filter(user=request.user, category_name=request.data['category_name'], ads_id=request.data['ads_id'])
        print('====================================================', saved_ads )
        if request.data['status']=='save':
            if not saved_ads.exists():
                saved_ads = SavedAds.objects.create(user=request.user, category_name=request.data['category_name'], ads_id=request.data['ads_id'])
                profile.Saved_Ads.add(saved_ads)
                profile.save()
        if request.data['status'] == 'delete':
            if saved_ads.exists():
                print('----------------------------------------------------------', saved_ads)
                profile.Saved_Ads.remove(saved_ads[0])
                saved_ads[0].delete()
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
        city = request.data.get('city', None) 
        sorted_data = get_data_by_search(title, city)
        


        return Response({'All_ads':sorted_data})


def get_data_by_search(title_name, city_name=None):
    all_data = []

    # Build the base query for filtering
    base_query = Q(Is_show=True) & Q(is_published=True) & (
        Q(title__icontains=title_name) | 
        Q(description__icontains=title_name) | 
        Q(category__name__icontains=title_name)
    )

    if city_name:  # Only include city filter if city_name is provided
        city_query = Q(City__icontains=city_name)
    else:
        city_query = Q()  # No city filter

    # Combine the base query and city query for each model
    car_ads = Car.objects.filter(base_query & city_query)
    car_ads_serializer = CarSerializer(car_ads, many=True)
    all_data.extend(car_ads_serializer.data)

    real_estate_ads = RealEstate.objects.filter(base_query & city_query)
    real_estate_ads_serializer = RealEstateSerializer(real_estate_ads, many=True)
    all_data.extend(real_estate_ads_serializer.data)

    other_ads = OthersAds.objects.filter(base_query & city_query)
    other_ads_serializer = OtherAdsSerializer(other_ads, many=True)
    all_data.extend(other_ads_serializer.data)

    # Sort the combined results by created_date
    sorted_data = sorted(all_data, key=lambda x: x['created_date'], reverse=True)

    return sorted_data





class ConversationListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):

        user= request.user
         
        cars = Car.objects.filter(user=user).exclude(admin_message__exact='')
        car_serializer = CarSerializer(cars,many=True)
        realestate = RealEstate.objects.filter(user=user ).exclude(admin_message__exact='')
        realestate_serializer = RealEstateSerializer(realestate,many = True)
        others = OthersAds.objects.filter(user=user).exclude(admin_message__exact='')
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
            
