
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    
    path("login",views.loginpage,name="login"),
    path("signup",views.signup,name="signup"),
    path('otplogin',views.otplogin, name='otplogin'),
    path('getotp',views.getotp, name='getotp'),
    path("home",views.homepage,name="home"),


    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)