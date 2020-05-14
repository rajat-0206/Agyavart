from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login',views.home,name='home'),
    path('login.html',views.home,name='home'),
    path('signup',views.register,name='register'),
    path('signup.html',views.register,name='register')

]
