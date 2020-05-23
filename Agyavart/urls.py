from django.urls import path,include
from . import views


from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.home,name='home'),
    path('rmail.html',views.home,name='home'),
    path('login',views.login,name='login'),
    path('login.html',views.login,name='login'),
    path('signup',views.register,name='register'),
    path('signup.html',views.register,name='register'),
    path('message.html',views.message,name="message"),
    path('message',views.message,name="message"),
    path('register',views.banao,name="create_user"),
    path('auth',views.login,name="auth"),
    path('fpass',views.forgotpass,name="password"),
    path('fuser',views.forgotusername,name="username"),
    path("temp",views.temp,name ="temp"),
    path('imgcng',views.imgcng,name="DP change"),
    path('covercng',views.covercng,name="cover change"),
    path('setting.html',views.setting,name='setting'),
    path('setting',views.setting,name='setting'),
    path('profile.html',views.profile,name='profile'),
    path('profile',views.profile,name='profile'),
    path('logout.html',views.logout,name="logout"),
    path('newmsg',views.newmsg,name = "newmsg"),
    path('detupt',views.detupt,name="Details"),
    path('changepass/',views.changepass,name="password"),
    path('delacc/',views.delacc,name="account"),
    path('viewsent/',views.viewsent,name="account"),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    