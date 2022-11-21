
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns =[
    
    path("login",views.loginpage,name="login"),
    path("signup",views.signup,name="signup"),
    # path("guestsignup",views.guestsignup,name="guestsignup"),
    path("mobile",views.mobile_signup,name="mobile"),
    # path("mobile_otp",views.otp_signup,name="signupotp"),
    path('otp/<uid>',views.otplogin, name='otplogin'),
    path('getotp',views.getotp, name='getotp'),
    path("home",views.homepage,name="home"),
    path("",views.startpage,name="start"),
    path('logout',views.logout, name='logout'),
    # path('view_product',views.view_product, name='view_product'),
    path("addtocart",views.addtocart,name="addtocart"),
    path("mycart",views.addtomycart,name="mycart"),
    path("updatecart",views.updatecartpage,name="updatecart"),
    path('checkout',views.checkout,name='checkout'),
    path('addaddress',views.addaddress,name='addaddress'),
    path('payment',views.payment,name='payment'),
    path('myorder',views.myorder,name='myorder'),
    path('cancelorder',views.cancelorder,name='cancelorder'),
    path('profile',views.myprofile,name='profile'),
    path('deleteaddress',views.deleteaddress,name='deleteaddress'),
    path('editprofile',views.editprofile,name='editprofile'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('product',views.product_view, name='product_view'),
    path('razorpay',views.razorpay,name='razorpay'),
    path('removecart',views.removecart,name='removecart'),

    path('error',views.error,name='error'),


    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)