from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    
    path("",views.adminstart,name="start"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("users",views.users,name="users"),
    path("orders",views.orders,name="orders"),
    path("products",views.products,name="products"),
    path("category",views.category,name="category"),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('editproduct',views.editproduct,name='editproduct'),
]