
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    
    path("login",views.loginpage,name="login"),
    path("signup",views.signup,name="signup"),
    path('otp/<uid>',views.otplogin, name='otplogin'),
    path('getotp',views.getotp, name='getotp'),
    path("home",views.homepage,name="home"),
    path("",views.startpage,name="start"),
    path('logout',views.logout, name='logout'),
    path('view_product',views.view_product, name='view_product'),


    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)