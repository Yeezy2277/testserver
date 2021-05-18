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
    DebtSerializer, NoMainInfoSerializer,
    WorkInfoUserSerializer, AdressInfoUserSerializer, 
    PassportInfoUserSerializer, RegisterInfoUserSerializer, 
    MainInfoUserSerializer
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
            numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
            for i in range(0, len(user_name)):
                if user_name[i] not in numbers:
                    return Response(data={"detail": "not valied phone"}, status=status.HTTP_400_BAD_REQUEST)
        
            #check another users with this username and password
            user = User.objects.create_user(user_name, None, user_password)
            user.save()

            #create different information of user
            a = MainInfoUser()
            a.user = User.objects.get(username=user)
            a.save()

            b = RegisterInfoUser()
            b.user = User.objects.get(username=user)
            b.save()

            c = PassportInfoUser()
            c.user = User.objects.get(username=user)
            c.save()

            d = AdressInfoUser()
            d.user = User.objects.get(username=user)
            d.save()

            e = WorkInfoUser()
            e.user = User.objects.get(username=user)
            e.save()

            f = NoMainInfoUser()
            f.user = User.objects.get(username=user)
            f.save()

            return Response(status=status.HTTP_200_OK)
        except SyntaxError:
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
        user_name = request.data.get('username')
        rating = UserRating.objects.get(user=User.objects.get(username=user_name)).rating
        
        
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
        data_debt = request.data.get('debt')
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
    def get_data_user(self, request):
        user_name  = request.data.get('username')
        #work with user's data
        main_info = MainInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        main_info_serializer = MainInfoUserSerializer(
            data=main_info
        )

        #work with register
        register_info = RegisterInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        register_info_serializer = RegisterInfoUserSerializer(
            data=register_info
        )

        #work with real adress 
        adress_info = AdressInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        adress_info_serializer = AdressInfoUserSerializer(
            data=request.data.get('adress_info_user')
        )

        #work with work 
        work_info = WorkInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        work_info_serializer = WorkInfoUserSerializer(
            data=request.data.get('work_info_user')
        )

        #work with second user's data
        second_info = NoMainInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        second_info_serializer = NoMainInfoSerializer(
            data=request.data.get('second_info_user')
        )

        return Response(data={
            "username": user_name, 
            "main_info": main_info_serializer.data, 
            "register_info": register_info_serializer.data, 
            "adress_info": adress_info_serializer.data,
            "work_info": work_info_serializer.data, 
            "second_info": second_info_serializer.data
        }, status=status.HTTP_200_OK)

    def put_data_user(self, request):
        user_name  = request.data.get('username')
        main_info = MainInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        main_info_serializer = MainInfoUserSerializer(
            instance=main_info, 
            data=request.data.get('main_info_user'), 
            partial=True
        )
        if main_info_serializer.is_valid(raise_exception=True):
            main_info_serializer.save()
        
        #update register data
        register_info = RegisterInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        register_info_serializer = RegisterInfoUserSerializer(
            instance=register_info, 
            data=request.data.get('register_info_user'), 
            partial=True
        )
        if register_info_serializer.is_valid(raise_exception=True):
            register_info_serializer.save()

        #upgrade adress 
        adress_info = AdressInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        adress_info_serializer = AdressInfoUserSerializer(
            instance=register_info, 
            data=request.data.get('adress_info_user'), 
            partial=True
        )
        if adress_info_serializer.is_valid(raise_exception=True):
            adress_info_serializer.save()

        #upgrade work
        work_info = WorkInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        work_info_serializer = WorkInfoUserSerializer(
            instance=work_info, 
            data=request.data.get('work_info_user'), 
            partial=True
        )
        if work_info_serializer.is_valid(raise_exception=True):
            work_info_serializer.save()

        #upgrade second user's information
        second_info = NoMainInfoUser.objects.get(
            user=User.objects.get(username=user_name)
        )
        second_info_serializer = NoMainInfoSerializer(
            instance=second_info, 
            data=request.data.get('second_info_user'), 
            partial=True
        )
        if second_info_serializer.is_valid(raise_exception=True):
            second_info_serializer.save()


        return Response(status=status.HTTP_200_OK)

#for return pdf file 
class ClassPdf(APIView):

    def post(self, request):
        contract = DebtCOntract.objects.get(
            debt = Debt.objects.get(id=1)
        )
        print(settings.MEDIA_ROOT+'/'+contract.file.name)

        return FileResponse(open(settings.MEDIA_ROOT+'/'+contract.file.name, 'rb'))

#it is security of header 
#after tets 
#i must to delete this function
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_header(request):
    class MyJWTAuthentication(JWTAuthentication):
        pass
    
    get_jwt_class = MyJWTAuthentication()
    my_header = get_jwt_class.get_header(request)
    my_raw_toekn = get_jwt_class.get_raw_token(my_header)
    my_valited_token = get_jwt_class.get_validated_token(my_raw_toekn)
    my_user = get_jwt_class.get_user(my_valited_token)

    print(my_user.username)



    return Response(status=status.HTTP_200_OK)


#for passprot photo 
class PassportView(ViewSet):
    def set_passport(self, request):
        class MyJWTAuthentication(JWTAuthentication):
            pass

        get_jwt_class = MyJWTAuthentication()

        passport_info = PassportInfoUser.objects.get(user=get_jwt_class.get_user(
            get_jwt_class.get_validated_token(get_jwt_class.get_raw_token(get_jwt_class.get_header(
                request
            )))
        ))
        
        serializer = PassportInfoUserSerializer(
            instance=passport_info, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return Response(status=status.HTTP_200_OK)





