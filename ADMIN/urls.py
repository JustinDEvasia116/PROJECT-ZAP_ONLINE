from unicodedata import name
from django.urls import path
from . import views

urlpatterns =[
    
    path("",views.adminstart,name="adminstart"),
    path("dashboard",views.dashboard,name="dashboard"),
    path("users",views.users,name="users"),
    path("orders",views.orders,name="orders"),
    path("products",views.products,name="products"),
    path("category",views.category,name="category"),
    path('addproduct',views.addproduct,name='addproduct'),
    path('addcategory',views.addcategory,name='addcategory'),

    path('delete_category',views.delete_category,name='delete_category'),
    path('editproduct',views.editproduct,name='editproduct'),
    path('deleteproduct',views.delete_product,name='delete_product'),
    path('block',views.block,name='block'),
    path('unblock',views.unblock,name='unblock'),
    path('adminlogout',views.logout, name='adminlogout'),
    path('cancelorder',views.cancelorder, name='cancelorder'),
    path('updatestatus',views.updatestatus, name='updatestatus'),
    path('coupons',views.coupons, name='coupons'),
    path('addcoupon',views.addcoupon, name='addcoupon'),
    path("offers",views.offers,name="offers"),
    path('prod_addoffer',views.prod_addoffer, name='prodoffer'),
    path('cate_addoffer',views.cate_addoffer, name='cateoffer'),

    

]