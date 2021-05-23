from django.urls import path
from .views import * 

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view()), 
    path('token/refresh/', TokenRefreshView.as_view()), 

    path('register/', RegisterUser.as_view()), 


    path('info/', WorkWithUserData.as_view({'post': 'get_data_user'})),
    path('set-info/', WorkWithUserData.as_view({'post': 'put_data_user'})), 
    path('getcontract/', ClassPdf.as_view()), 

    path('calculate/', Calculate.as_view({'post': 'get_calculate'})), 
    path('new-calculate/', Calculate.as_view({'post': 'create_sum'})), 


    #test 
    path('test-get-user/', test_header), 
    path('test-get-user-passport/', PassportView.as_view({'post': 'set_passport'})),
]
