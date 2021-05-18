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
    user = serializers.CharField()
    debt_sum = serializers.IntegerField()
    date_of_finish = serializers.DateField()
    percent = serializers.IntegerField()
    debt_admin_status = serializers.BooleanField()
    debt_status = serializers.CharField()

    def create(self, validated_data):
        new_debt = Debt()
        new_debt.user = User.objects.get(username=validated_data['user'])
        new_debt.debt_sum = validated_data['debt_sum']
        new_debt.date_of_finish = validated_data['date_of_finish']
        new_debt.percent = validated_data['percent']
        new_debt.debt_admin_status = validated_data['debt_admin_status']
        new_debt.debt_status = validated_data['debt_status']
        
        new_debt.save()
        return new_debt


###derializer for user's imformation############

class MainInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    sername = serializers.CharField()
    name = serializers.CharField()
    second_name = serializers.CharField()
    your_birthday = serializers.DateField()
    tel = serializers.CharField()
    second_tel = serializers.CharField()
    your_mail = serializers.EmailField()

    def create(self, validated_data):
        new_main_info = MainInfoUser()
        new_main_info.user = User.objects.get(username=validated_data['user'])
        new_main_info.sername = validated_data['sername']
        new_main_info.name = validated_data['name']
        new_main_info.second_name = validated_data['second_name']
        new_main_info.your_birthday = validated_data['your_birthday']
        new_main_info.tel = validated_data['tel']
        new_main_info.second_tel = validated_data['second_tel']
        new_main_info.your_mail = validated_data['your_mail']

        new_main_info.save()
        return new_main_info

    def update(self, instance, validated_data):
        instance.sername = validated_data['sername']
        instance.name = validated_data['name']
        instance.second_name = validated_data['second_name']
        instance.your_birthday = validated_data['your_birthday']
        instance.tel = validated_data['tel']
        instance.second_tel = validated_data['second_tel']
        instance.your_mail = validated_data['your_mail']
        
        instance.save()
        return instance

class RegisterInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    register_index = serializers.IntegerField()
    register_city = serializers.CharField()
    register_street = serializers.CharField()
    register_house = serializers.CharField()
    register_flat = serializers.CharField()
    register_private_house = serializers.CharField()

    def create(self, validated_data):
        new_register_info = RegisterInfoUser()
        new_register_info.user = User.objects.get(username=validated_data['user'])
        new_register_info.register_index = validated_data['register_index']
        new_register_info.register_city = validated_data['register_city']
        new_register_info.register_street = validated_data['register_street']
        new_register_info.register_house = validated_data['register_house']
        new_register_info.register_flat = validated_data['register_flat']
        new_register_info.register_private_house = validated_data['register_private_house']

        new_register_info.save()
        return new_register_info

    def update(self, instance, validated_data):
        instance.register_index = validated_data['register_index']
        instance.register_city = validated_data['register_city']
        instance.register_street = validated_data['register_street']
        instance.register_house = validated_data['register_house']
        instance.register_flat = validated_data['register_flat']
        instance.register_private_house = validated_data['register_private_house']
        
        instance.save()
        return instance

class PassportInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    passport_series = serializers.IntegerField()
    passport_nomder = serializers.IntegerField()
    passport_date = serializers.DateField()
    passport_place = serializers.CharField()
    passport_code = serializers.CharField()
    passport_photo1 = serializers.ImageField(max_length=None, allow_empty_file=False)
    passport_photo2 = serializers.ImageField(allow_empty_file=False)
    passport_photo3 = serializers.ImageField(allow_empty_file=False)


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
        print(validated_data['passport_photo1'])
        instance.passport_series = validated_data['passport_series']
        instance.passport_nomder = validated_data['passport_nomder']
        instance.passport_date = validated_data['passport_date']
        instance.passport_place = validated_data['passport_place']
        instance.passport_code = validated_data['passport_code']
        instance.passport_photo1 = validated_data['passport_photo1']
        instance.passport_photo2 = validated_data['passport_photo2']
        instance.passport_photo3 = validated_data['passport_photo3']
        
        instance.save()
        return instance

class AdressInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    adress = serializers.BooleanField()
    adress_index = serializers.IntegerField()
    adress_city = serializers.CharField()
    adress_street = serializers.CharField()
    adress_house = serializers.IntegerField()
    adress_flat = serializers.IntegerField()
    adress_private_house = serializers.BooleanField()

    def create(self, validated_data):
        new_adress_info = AdressInfoUser()
        new_adress_info.user = User.objects.get(username=validated_data['user'])
        new_adress_info.adress = validated_data['adress']
        new_adress_info.adress_city = validated_data['adress_city']
        new_adress_info.adress_street = validated_data['adress_street']
        new_adress_info.adress_house = validated_data['adress_house']
        new_adress_info.adress_flat = validated_data['adress_flat']
        new_adress_info.adress_private_house = validated_data['adress_private_house']

        new_adress_info.save()
        return new_adress_info

    def update(self, instance, validated_data):
        instance.adress = validated_data['adress']
        instance.adress_city = validated_data['adress_city']
        instance.adress_street = validated_data['adress_street']
        instance.adress_house = validated_data['adress_house']
        instance.adress_flat = validated_data['adress_flat']
        instance.adress_private_house = validated_data['adress_private_house']
        
        instance.save()
        return instance

class WorkInfoUserSerializer(serializers.Serializer):
    user = serializers.CharField()
    work_status = serializers.CharField()
    work_name = serializers.CharField()
    work_tel = serializers.CharField()
    work_position = serializers.CharField()
    work_years = serializers.IntegerField()

    def create(self, validated_data):
        new_work_info = WorkInfoUser()
        new_work_info.user = User.objects.get(username=validated_data['user'])
        new_work_info.work_status = validated_data['work_status']
        new_work_info.work_name = validated_data['work_name']
        new_work_info.work_tel = validated_data['work_tel']
        new_work_info.work_position = validated_data['work_position']
        new_work_info.work_years = validated_data['work_years']

        new_work_info.save()
        return new_work_info

    def update(self, instance, validated_data):
        instance.work_status = validated_data['work_status']
        instance.work_name = validated_data['work_name']
        instance.work_tel = validated_data['work_tel']
        instance.work_position = validated_data['work_position']
        instance.work_years = validated_data['work_years']
        
        instance.save()
        return instance

class NoMainInfoSerializer(serializers.Serializer):
    user = serializers.CharField()
    information_income = serializers.IntegerField()
    information_family = serializers.CharField()
    information_education = serializers.CharField()
    information_car = serializers.CharField()

    def create(self, validated_data):
        new_nomain_info = NoMainInfoUser()
        new_nomain_info.user = User.objects.get(username=validated_data['user'])
        new_nomain_info.information_income = validated_data['information_income']
        new_nomain_info.information_family = validated_data['information_family']
        new_nomain_info.information_education = validated_data['information_education']
        new_nomain_info.information_car = validated_data['information_car']
        
        new_nomain_info.save()
        return new_nomain_info

    def update(self, instance, validated_data):
        instance.information_income = validated_data['information_income']
        instance.information_family = validated_data['information_family']
        instance.information_education = validated_data['information_education']
        instance.information_car = validated_data['information_car']
        
        instance.save()
        return instance




###end of derializer for user's imformation#####







