from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class MainInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    sername = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    your_birthday = models.DateField(null=True, blank=True)
    tel = models.CharField(max_length=50, blank=True)
    second_tel = models.CharField(max_length=50, null=True, blank=True)
    your_mail = models.EmailField(null=True, blank=True)
    
class RegisterInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    register_index = models.IntegerField(null=True, blank=True)
    register_city = models.CharField(max_length=100, null=True, blank=True)
    register_street = models.CharField(max_length=100, null=True, blank=True)
    register_house = models.IntegerField(null=True, blank=True)
    register_flat = models.IntegerField(null=True, blank=True)
    register_private_house = models.BooleanField(null=True, blank=True)

class PassportInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    passport_series = models.IntegerField(null=True, blank=True)
    passport_nomder = models.IntegerField(null=True, blank=True)
    passport_date = models.DateField(null=True, blank=True)
    passport_place = models.CharField(max_length=100, null=True, blank=True)
    passport_code = models.CharField(max_length=10, null=True, blank=True)
    passport_photo1 = models.ImageField(upload_to='myphoto/', null=True, blank=True)
    passport_photo2 = models.ImageField(upload_to='myphoto/', null=True, blank=True)
    passport_photo3 = models.ImageField(upload_to='myphoto/', null=True, blank=True)

class AdressInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    adress = models.BooleanField(null=True, blank=True)
    adress_index = models.IntegerField(null=True, blank=True)
    adress_city = models.CharField(max_length=100, null=True, blank=True)
    adress_street = models.CharField(max_length=100, null=True, blank=True)
    adress_house = models.IntegerField(null=True, blank=True)
    adress_flat = models.IntegerField(null=True, blank=True)
    adress_private_house = models.BooleanField(null=True, blank=True)

class WorkInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    work_status = models.CharField(max_length=50, null=True, blank=True)
    work_name = models.CharField(max_length=50, null=True, blank=True)
    work_tel = models.CharField(max_length=50, null=True, blank=True)
    work_position = models.CharField(max_length=50, null=True, blank=True)
    work_years = models.IntegerField(null=True, blank=True)

class NoMainInfoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    information_income = models.IntegerField(null=True, blank=True)
    information_family = models.CharField(max_length=20, null=True, blank=True)
    information_education = models.CharField(max_length=30, null=True, blank=True)
    information_car = models.CharField(max_length=50, null=True, blank=True)
    


class MyPhoto(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='wow', null=True, max_length=255)


class UserRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rating = models.IntegerField()

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    debt_sum = models.IntegerField(null=True, blank=True)
    date_of_finish = models.DateField(null=True, blank=True)
    percent = models.IntegerField(null=True, blank=True)
    debt_admin_status = models.BooleanField(null=True, blank=True)
    debt_status = models.CharField(max_length=50, null=True, blank=True)

class DebtCOntract(models.Model):
    debt = models.OneToOneField(Debt, on_delete=models.CASCADE, primary_key=True)
    file = models.FileField(upload_to='hz')
    



'''
class Money(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, primary_key=True)
     = 
'''



