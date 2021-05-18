from django.contrib import admin
from .models import (
    MainInfoUser, RegisterInfoUser, 
    PassportInfoUser, AdressInfoUser, 
    WorkInfoUser, NoMainInfoUser, 
    MyPhoto, UserRating, 
    Debt, DebtCOntract
)


admin.site.register(MainInfoUser)
admin.site.register(RegisterInfoUser)
admin.site.register(PassportInfoUser)
admin.site.register(AdressInfoUser)
admin.site.register(WorkInfoUser)
admin.site.register(NoMainInfoUser)
admin.site.register(MyPhoto)
admin.site.register(UserRating)
admin.site.register(Debt)
admin.site.register(DebtCOntract)