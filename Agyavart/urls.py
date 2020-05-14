from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('rmail.html',views.home,name='home'),
    path('login',views.login,name='login'),
    path('login.html',views.login,name='login'),
    path('signup',views.register,name='register'),
    path('signup.html',views.register,name='register'),
    path('register',views.banao,name="create_user"),
    path('auth',views.checkkaro,name="auth")

]
