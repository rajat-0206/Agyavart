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
    path('register',views.banao,name="create_user"),
    path('auth',views.checkkaro,name="auth"),
    path('fpass',views.forgotpass,name="password"),
    path('fuser',views.forgotusername,name="username"),
    path("temp",views.temp,name ="temp"),
    path('imgcng',views.imgcng,name="DP change"),
    path('setting.html',views.setting,name='setting'),
    path('update.html',views.update,name='update'),
    path('passupdate.html',views.passupdate,name='passupdate'),
    path('profile.html',views.profile,name='profile')



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    