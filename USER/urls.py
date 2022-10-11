from unicodedata import name
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    
    path("login",views.loginpage,name="login"),
    path("signup",views.signup,name="signup"),
    path("otp",views.otppage,name="otp"),
    path("home",views.homepage,name="home"),


    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)