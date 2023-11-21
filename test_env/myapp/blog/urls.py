from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
from .views import *





app_name = 'blog'

urlpatterns = [
    
    
    
    
    #path('register/',views.user_register, name ='user_register'),
    #path('login/',views.user_login, name='login'),
    #path('logout/',views.user_logout, name='logout'),
    #path('reset/',views.UserPasswordResetView.as_view(), name = 'reset_password'),
   # path('reset/done/',views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    ##path('confirm/<uidb64>/<token>/',views.UserPasswordResetConfirmView.as_view(),name='password_reset_confirm'),
   # path('confirm/comlete',views.UserPasswordResetCompleteView.as_view(), name= 'password_reset_complete')
         ]
 

