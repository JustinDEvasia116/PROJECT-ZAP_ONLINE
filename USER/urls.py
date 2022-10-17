
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    
    path("login",views.loginpage,name="login"),
    path("signup",views.signup,name="signup"),
    path("mobile",views.mobile_signup,name="mobile"),
    # path("mobile_otp",views.otp_signup,name="signupotp"),
    path('otp/<uid>',views.otplogin, name='otplogin'),
    path('getotp',views.getotp, name='getotp'),
    path("home",views.homepage,name="home"),
    path("",views.startpage,name="start"),
    path('logout',views.logout, name='logout'),
    path('view_product',views.view_product, name='view_product'),
    path("addtocart",views.addtocart,name="addtocart"),
    path("mycart",views.addtomycart,name="mycart"),
    path("updatecart",views.updatecartpage,name="updatecart"),


    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)