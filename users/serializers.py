from rest_framework import serializers
from .models import (
    MainInfoUser, RegisterInfoUser, 
    PassportInfoUser, AdressInfoUser,
    WorkInfoUser, NoMainInfoUser, 
    MyPhoto, UserRating, 
    Debt, DebtCOntract
)
from django.contrib.auth.models import User


class MyPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPhoto
        fields = ('id', 'name', 'image')

class UserRatingSerializer(serializers.Serializer):
    user = serializers.CharField()
    rating = serializers.IntegerField()
    
    def create(self, validated_data):
        a_a = UserRating.objects.create(
            user = User.objects.get(username=validated_data['user']),
            rating = validated_data['rating']
        )
        a_a.save()
        return a_a

    def update(self, instance, validated_data):
        instance.rating = validated_data['rating'] 
        instance.save()
        return instance



class DebtSerializer(serializers.Serializer):
    user = serializers.CharField(required=False,default='some_default_value')
    debt_sum = serializers.IntegerField(required=False,default='some_default_value')
    date_of_finish = serializers.DateField(required=False,default='some_default_value')
    percent = serializers.IntegerField(required=False,default='some_default_value')
    debt_admin_status = serializers.BooleanField(required=False,default='some_default_value')
    debt_status = serializers.CharField(required=False,default='some_default_value')

    def create(self, validated_data):
        new_debt = Debt()
        try: 
            new_debt.user = User.objects.get(username=validated_data['user'])
        except: 
            pass
        try: 
            new_debt.debt_sum = validated_data['debt_sum']
        except: 
            pass
        try: 
            new_debt.date_of_finish = validated_data['date_of_finish']
        except: 
            pass
        try: 
            new_debt.percent = validated_data['percent']
        except: 
            pass
        
        new_debt.debt_admin_status = False
        new_debt.debt_status = "Не рассмотрено"
        
        
        new_debt.save()
        return new_debt


###derializer for user's imformation############
class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    
class MainInfoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MainInfoUser
        fields = ['sername', 'name', 'second_name', 
            'your_birthday', 'tel','second_tel', 
            'your_mail', 'user'
        ]
    
    def create(self, validated_data):
        this_username = validated_data.pop('user')
        this_user = User.objects.get(username=this_username['username'])

        
        mainInfoUser = MainInfoUser.objects.get(user=this_user)
        mainInfoUser.delete()
        mainInfoUser = MainInfoUser.objects.create(user=this_user, **validated_data)
        mainInfoUser.save()

        return mainInfoUser
        

class RegisterInfoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RegisterInfoUser
        fields = ['register_index', 'register_city', 
            'register_street', 'register_house', 
            'register_flat','register_private_house', 
            'user'
        ]
    
    def create(self, validated_data):
        this_username = validated_data.pop('user')
        this_user = User.objects.get(username=this_username['username'])

        registerInfoUser = RegisterInfoUser.objects.get(user=this_user)
        registerInfoUser.delete()
        registerInfoUser = RegisterInfoUser.objects.create(user=this_user, **validated_data)
        registerInfoUser.save()

        return registerInfoUser
    
    
    

class PassportInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField(required=False,default='some_default_value')
    passport_series = serializers.IntegerField(required=False,default='some_default_value')
    passport_nomder = serializers.IntegerField(required=False,default='some_default_value')
    passport_date = serializers.DateField(required=False,default='some_default_value')
    passport_place = serializers.CharField(required=False,default='some_default_value')
    passport_code = serializers.CharField(required=False,default='some_default_value')
    passport_photo1 = serializers.ImageField(required=False,default='some_default_value')
    passport_photo2 = serializers.ImageField(required=False,default='some_default_value')
    passport_photo3 = serializers.ImageField(required=False,default='some_default_value')


    def create(self, validated_data):
        new_pasport_info = PassportInfoUser()
        new_pasport_info.user = User.objects.get(username=validated_data['user'])
        new_pasport_info.passport_series = validated_data['passport_series']
        new_pasport_info.passport_nomder = validated_data['passport_nomder']
        new_pasport_info.passport_date = validated_data['passport_date']
        new_pasport_info.passport_place = validated_data['passport_place']
        new_pasport_info.passport_code = validated_data['passport_code']
        new_pasport_info.passport_photo1 = validated_data['passport_photo1']
        new_pasport_info.passport_photo2 = validated_data['passport_photo2']
        new_pasport_info.passport_photo3 = validated_data['passport_photo3']


        new_pasport_info.save()
        return new_pasport_info

    def update(self, instance, validated_data):
        instance.passport_nomder = validated_data['passport_nomder']
        instance.passport_date = validated_data['passport_date']
        instance.passport_place = validated_data['passport_place']
        instance.passport_code = validated_data['passport_code']
        try:
            instance.passport_photo1 = validated_data['passport_photo1']
        except:
            pass
        instance.passport_photo2 = validated_data['passport_photo2']
        instance.passport_photo3 = validated_data['passport_photo3']
        
        instance.save()
        return instance

class AdressInfoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = AdressInfoUser
        fields = ['adress', 'adress_index', 
            'adress_city', 'adress_street', 
            'adress_house','adress_flat', 
            'adress_private_house', 'user'
        ]
    
    def create(self, validated_data):
        this_username = validated_data.pop('user')
        this_user = User.objects.get(username=this_username['username'])

        adressInfoUser = AdressInfoUser.objects.get(user=this_user)
        adressInfoUser.delete()
        adressInfoUser = AdressInfoUser.objects.create(user=this_user, **validated_data)
        adressInfoUser.save()

        return adressInfoUser

class WorkInfoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = WorkInfoUser
        fields = ['work_status', 'work_name', 
            'work_tel', 'work_position', 
            'work_years', 'user'
        ]
    
    def create(self, validated_data):
        this_username = validated_data.pop('user')
        this_user = User.objects.get(username=this_username['username'])

        workInfoUser = WorkInfoUser.objects.get(user=this_user)
        workInfoUser.delete()
        workInfoUser = WorkInfoUser.objects.create(user=this_user, **validated_data)
        workInfoUser.save()

        return workInfoUser

class NoMainInfoUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = NoMainInfoUser
        fields = ['information_income', 'information_family', 
            'information_education', 'information_car', 
            'user'
        ]
    
    def create(self, validated_data):
        this_username = validated_data.pop('user')
        this_user = User.objects.get(username=this_username['username'])

        noMain = NoMainInfoUser.objects.get(user=this_user)
        noMain.delete()
        noMain = NoMainInfoUser.objects.create(user=this_user, **validated_data)
        noMain.save()

        return noMain




###end of derializer for user's imformation#####







