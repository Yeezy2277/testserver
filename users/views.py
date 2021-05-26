import os
import math
import pathlib
import datetime
from .models import (
    MainInfoUser, RegisterInfoUser, 
    PassportInfoUser, AdressInfoUser, 
    WorkInfoUser, NoMainInfoUser, 
    MyPhoto, UserRating, 
    Debt, DebtCOntract
)
from .serializers import (
    MyPhotoSerializer, UserRatingSerializer,
    DebtSerializer, NoMainInfoUserSerializer,
    WorkInfoUserSerializer, AdressInfoUserSerializer, 
    PassportInfoUserSerializer, RegisterInfoUserSerializer, 
    MainInfoUserSerializer, UserSerializer
)

from django.contrib.auth.models import User
from django.conf import settings
from django.http import FileResponse
from django.core.files import File

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from fpdf import FPDF, HTMLMixin

from rest_framework_simplejwt.authentication import JWTAuthentication

class PhotoList(APIView):
    def post(self, request, format=None):
        serializer = MyPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        try:
            user_name = request.data.get('username')
            user_password = request.data.get('password')
            
            #check users phone
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
            for i in range(0, len(user_name)):
                if user_name[i] not in numbers:
                    return Response(data={"detail": "not valied phone"}, status=status.HTTP_400_BAD_REQUEST)
        
            #check another users with this username and password
            user = User.objects.create_user(user_name, None, user_password)
            user.save()

            #create different information of user
            a = MainInfoUser()
            a.user = user
            a.save()

            b = RegisterInfoUser()
            b.user = user
            b.save()

            c = PassportInfoUser()
            c.user = user
            c.save()

            d = AdressInfoUser()
            d.user = user
            d.save()

            e = WorkInfoUser()
            e.user = user
            e.save()

            f = NoMainInfoUser()
            f.user = user
            f.save()


            #create rating for user
            h = UserRating()
            h.user = user
            h.rating = 1
            h.save()

            return Response(status=status.HTTP_200_OK)
        except:
            return Response(data={"detail": "this user in db"}, status=status.HTTP_400_BAD_REQUEST)


class RatingList(APIView):
    def post(self, request, format=None):
        serializer = UserRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#calculate sum 

class Calculate(ViewSet):
    def get_calculate(self, request):
        class MyJWTAuthentication(JWTAuthentication):
                pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)
        
        
        rating = UserRating.objects.get(user=my_user).rating
        
        
        if rating == 1:
            return Response(data={
                'debt_sum': 1000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100),
                'percent': 50
            }, status=status.HTTP_200_OK)

        if rating == 2:
            return Response(data={
                'debt_sum': 5000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100),
                'percent': 50
            }, status=status.HTTP_200_OK)
        
        if rating == 3:
            return Response(data={
                'debt_sum': 10000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100), 
                'percent': 50
            }, status=status.HTTP_200_OK)
        
        if rating == 4:
            return Response(data={
                'debt_sum': 20000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100), 
                'percent': 50
            }, status=status.HTTP_200_OK)

        if rating == 5:
            return Response(data={
                'debt_sum': 40000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100), 
                'percent': 50
            }, status=status.HTTP_200_OK)
        
        if rating == 6:
            return Response(data={
                'debt_sum': 80000,
                'date_of_finish': datetime.date.today() + datetime.timedelta(days=100), 
                'percent': 50
            }, status=status.HTTP_200_OK)

    def create_sum(self, request):
        class MyJWTAuthentication(JWTAuthentication):
                pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)

        data_debt = request.data.get('debt')
        data_debt.update({"user": my_user.username})
        serializer = DebtSerializer(data=data_debt)
        this_debt = None
        if serializer.is_valid(raise_exception=True):
            this_debt = serializer.save()

        #create contract
        class wow(FPDF, HTMLMixin):
            pass
        
        text = '''<h1>It is pdf document</h2>'''
        pdf = wow()
        pdf.add_page()
        pdf.write_html(text)
        pdf.output(
            str(pathlib.Path(__file__).resolve().parent) + '/temporary/' +this_debt.user.username + '__' + str(this_debt.id) + '.pdf'
        )

        this_contract = DebtCOntract()
        this_contract.debt = this_debt
        this_contract.file.save(
            this_debt.user.username + '__' + str(this_debt.id) + 'pdf',
            File(open(
                str(pathlib.Path(__file__).resolve().parent) + '/temporary/' +this_debt.user.username + '__' + str(this_debt.id) + '.pdf', 'rb'
            ))
        )

        path = os.path.join(
            str(pathlib.Path(__file__).resolve().parent) + '/temporary/' +this_debt.user.username + '__' + str(this_debt.id) + '.pdf'
        )
        os.remove(path)

        return Response(status=status.HTTP_200_OK)

class AdminFunc(ViewSet):
    def get_new(self, request):
        debt = Debt.objects.filter(debt_admin_status=False)
        list_of_new_debt = []
        for i in debt:
            list_of_new_debt.append({
                "debt_id": i.id,
                "user": i.user.id,
                "debt_sum": i.debt_sum, 
                "date_of_finish": i.date_of_finish, 
                "percent": i.percent, 
                "debt_admin_status": i.debt_admin_status,
                "debt_status": i.debt_status
            })
        
        return Response(data={"list of debt": list_of_new_debt}, status=status.HTTP_200_OK)

    def get_new_one(self, request):
        debt = Debt.objects.get(id=request.data.get('debt_id'))
        

class WorkWithUserData(ViewSet):
    #get user with token
    def get_data_user(self, request):
        class MyJWTAuthentication(JWTAuthentication):
            pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)
        
        mainInfoUser = MainInfoUser.objects.get(user=my_user)
        mainInfo = {
            "sername": mainInfoUser.sername, 
            "name": mainInfoUser.name, 
            "second_name": mainInfoUser.second_name, 
            "your_birthday": mainInfoUser.your_birthday, 
            "tel": mainInfoUser.tel, 
            "second_tel": mainInfoUser.second_tel, 
            "your_mail": mainInfoUser.your_mail
        }

        registerInfoUser = RegisterInfoUser.objects.get(user=my_user)
        registerInfo = {
            "register_index": registerInfoUser.register_index,
            "register_city": registerInfoUser.register_city,
            "register_street": registerInfoUser.register_street,
            "register_house": registerInfoUser.register_house,
            "register_flat": registerInfoUser.register_flat, 
            "register_private_house": registerInfoUser.register_private_house,
        }
        
        adressInfoUser = AdressInfoUser.objects.get(user=my_user)
        adressInfo = {
            "adress": adressInfoUser.adress,
            "adress_index": adressInfoUser.adress_index, 
            "adress_city": adressInfoUser.adress_city,
            "adress_street": adressInfoUser.adress_street,
            "adress_house": adressInfoUser.adress_house,
            "adress_flat": adressInfoUser.adress_flat,
            "adress_private_house": adressInfoUser.adress_private_house
        }

        workInfoUser =  WorkInfoUser.objects.get(user=my_user)
        workInfo = {
            "work_status": workInfoUser.work_status,
            "work_name": workInfoUser.work_name, 
            "work_tel": workInfoUser.work_tel,
            "work_position": workInfoUser.work_position,
            "work_years": workInfoUser.work_years
        }

        noMainInfo = NoMainInfoUser.objects.get(user=my_user)
        noMain = {
            "information_income": noMainInfo.information_income,
            "information_family": noMainInfo.information_family, 
            "information_education": noMainInfo.information_education,
            "information_car": noMainInfo.information_car
        }
        
        return Response(data={
            "main_info": mainInfo, 
            "register_info": registerInfo,
            "adress_info": adressInfo, 
            "work_info": workInfo, 
            "other_information": noMain
        }, status=status.HTTP_200_OK)

    def put_data_user(self, request):
        class MyJWTAuthentication(JWTAuthentication):
            pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)

        my_data = request.data
        
        #work with main user's data
        mainInfo = my_data.get('main_info')
        mainInfo.update({'user': {'username': my_user.username}})
        mainInfoUserSerializer = MainInfoUserSerializer(data=mainInfo)
        if mainInfoUserSerializer.is_valid(raise_exception=True):
            mainInfoUserSerializer.save()

        #work with register
        registerInfo = my_data.get('register_info')
        registerInfo.update({'user': {'username': my_user.username}})
        registerInfoUserSerializer = RegisterInfoUserSerializer(data=registerInfo)
        if registerInfoUserSerializer.is_valid(raise_exception=True):
            registerInfoUserSerializer.save()
        

        #work with real adress 
        adressInfo = request.data.get('adress_info')
        adressInfo.update({'user': {'username': my_user.username}})
        adressInfoUserSerializer = AdressInfoUserSerializer(data=adressInfo)
        if adressInfoUserSerializer.is_valid(raise_exception=True):
            adressInfoUserSerializer.save()

        
        #work with work
        workInfo = request.data.get('work_info')
        workInfo.update({'user': {'username': my_user.username}})
        workInfoUserSerializer = WorkInfoUserSerializer(data=workInfo)
        if workInfoUserSerializer.is_valid(raise_exception=True):
            workInfoUserSerializer.save()

        #work with no main
        noMain = request.data.get('other_information')
        noMain.update({'user': {'username': my_user.username}})
        mainInfoUserSerializer = NoMainInfoUserSerializer(data=noMain)
        if mainInfoUserSerializer.is_valid(raise_exception=True):
            mainInfoUserSerializer.save()
        

        return Response(status=status.HTTP_200_OK)

#for return pdf file 
class ClassPdf(APIView):

    def post(self, request):
        contract = DebtCOntract.objects.get(
            debt = Debt.objects.get(id=1)
        )
        print(settings.MEDIA_ROOT+'/'+contract.file.name)

        return FileResponse(open(settings.MEDIA_ROOT+'/'+contract.file.name, 'rb'))


#for passprot photo 
class PassportView(ViewSet):
    def set_passport(self, request):
        class MyJWTAuthentication(JWTAuthentication):
            pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)

        saved_passport = PassportInfoUser.objects.get(user=my_user)        

        serializer = PassportInfoUserSerializer(
            instance=saved_passport, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    def get_photo1(self, request):
        try:
            class MyJWTAuthentication(JWTAuthentication):
                pass
    
            get_jwt_class = MyJWTAuthentication()
            my_header = get_jwt_class.get_header(request)
            my_raw_toekn = get_jwt_class.get_raw_token(my_header)
            my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
            my_user = get_jwt_class.get_user(my_valited_token)
            
            a_a = PassportInfoUser.objects.get(user=my_user)
            

            return FileResponse(open(a_a.passport_photo1.path, 'rb'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_photo2(self, request):
        try:
            class MyJWTAuthentication(JWTAuthentication):
                pass
    
            get_jwt_class = MyJWTAuthentication()
            my_header = get_jwt_class.get_header(request)
            my_raw_toekn = get_jwt_class.get_raw_token(my_header)
            my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
            my_user = get_jwt_class.get_user(my_valited_token)
            
            a_a = PassportInfoUser.objects.get(user=my_user)
            

            return FileResponse(open(a_a.passport_photo2.path, 'rb'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get_photo3(self, request):
        try:
            class MyJWTAuthentication(JWTAuthentication):
                pass
    
            get_jwt_class = MyJWTAuthentication()
            my_header = get_jwt_class.get_header(request)
            my_raw_toekn = get_jwt_class.get_raw_token(my_header)
            my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
            my_user = get_jwt_class.get_user(my_valited_token)
            
            a_a = PassportInfoUser.objects.get(user=my_user)
            

            return FileResponse(open(a_a.passport_photo3.path, 'rb'))
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get_other(self, request):
        class MyJWTAuthentication(JWTAuthentication):
                pass
    
        get_jwt_class = MyJWTAuthentication()
        my_header = get_jwt_class.get_header(request)
        my_raw_toekn = get_jwt_class.get_raw_token(my_header)
        my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
        my_user = get_jwt_class.get_user(my_valited_token)        

        a_a = PassportInfoUser.objects.get(user=my_user)

        return Response(data={
            "passport_series": a_a.passport_series,
            "passport_nomder": a_a.passport_nomder,
            "passport_date": a_a.passport_date,
            "passport_place": a_a.passport_place,
            "passport_code": a_a.passport_code,
        }, status=status.HTTP_200_OK)





