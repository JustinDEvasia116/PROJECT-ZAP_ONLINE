
from django.shortcuts import render,redirect
from .models import Category,Product

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from USER.models import *
import os
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
# Create your views here.
def adminstart(request):
    return render(request,"adminstart.html")



@login_required(login_url='adminstart')
@never_cache
def dashboard(request):

  
    products=Product.objects.all()
    orders = Order.objects.all().order_by('-id')
    cart = UserCart.objects.all()

    return render(request, 'dashboard.html',{'orders':orders,'products':products,'carts':cart})

@login_required(login_url='adminstart')
@never_cache
def orders(request):
    order = Order.objects.all().order_by('-id')
    cart = UserCart.objects.all()
    status = ['Ordered','Shipped','Delivered','Cancelled']
    return render(request, 'orders.html',{'orders':order,'carts':cart,'status':status})

@login_required(login_url='adminstart')
@never_cache
def users(request):
     user_details=User.objects.filter(is_superuser=False)
     return render(request, 'users.html',{'user_details':user_details})

@login_required(login_url='adminstart')
@never_cache
def addproduct(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        brand = request.POST['brand']
        quantity = request.POST['quantity']
        print(request.FILES,"  1111")
        image = request.FILES['image']
        image1 = request.FILES['image1']
        image2 = request.FILES['image2']
        image3 = request.FILES['image3']
        print(image1,"  2222")
        
        category=Category.objects.get(id=category)
        product = Product.objects.create(name=name,description=description,price=price,image=image,brand=brand,quantity=quantity)
        product.category.add(category)
        product.save()

        image1 = Images.objects.create(image=image1,product=product)
        image1.save()
        image2 = Images.objects.create(image=image2,product=product)
        image2.save()
        image3 = Images.objects.create(image=image3,product=product)
        image3.save()
        return redirect('addproduct')
    else:
        
        category=Category.objects.all()
        # subcategory =category.sub_categories.all()


        
        print(category)
        
        return render(request, 'addproduct.html',{'categories':category})
    
@login_required(login_url='adminstart')
@never_cache
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['catname']
        id = request.POST['category']
        categories= Category.objects.get(id=id)
        category = Category.objects.create(name=name)
        category.sub_categories.add(categories)
     
       
        return redirect('category')
    else:
        category=Category.objects.all()
        return render(request, 'addcategory.html',{'categories':category})

@login_required(login_url='adminstart')
@never_cache
def block(request):
    id=request.GET['id']
    user=User.objects.get(id=id)
    user.is_active=False
    user.save()
    return redirect('users')
def unblock(request):
    id=request.GET['id']
    user=User.objects.get(id=id)
    user.is_active=True
    user.save()
    return redirect('users')

@login_required(login_url='adminstart')
@never_cache
def products(request):
    product=Product.objects.all()
    return render(request, 'products.html',{'products':product})

@login_required(login_url='adminstart')
@never_cache
def category(request):
    if request.method == 'POST':

        ids = request.POST['category']
        print(ids)
        allcategory = Category.objects.all()
        
        categories = Category.objects.get(id=ids)
        print(categories)
        subcategories=categories.sub_categories.all().order_by('id')[1:]
       
        print(subcategories)
        return render(request, 'category.html', {'categories': categories,'subcategories': subcategories,'allcategory':allcategory})
        
    else:
        allcategory = Category.objects.all()
        return render(request,'category.html',{'allcategory': allcategory})
        









@login_required(login_url='adminstart')
@never_cache
def editproduct(request):
    id=request.GET['id']
    product = Product.objects.get(id=id)
    if request.method=='POST':
        id=request.GET['id']
        product = Product.objects.get(id=id)
        print(id)
        
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        category = request.POST['category']
        brand = request.POST['brand']
        print(request.FILES,"  1111")
        image = request.FILES['image']
        quantity = request.POST['quantity']
        
        category=Category.objects.get(id=category)
        product = Product.objects.get(id=id)
        product.name=name
        product.description=description
        product.price=price
        product.category=category
        product.brand=brand
        product.quantity=quantity
        product.image=image
        product.save()
        
        return redirect('products')
    else:
        id=request.GET['id']
        product=Product.objects.get(id=id)
        category=Category.objects.all()
        return render(request, 'edit_product.html',{'product':product,'categories':category})


def adminstart(request):
    if 'sessionadmin' in request.session:
        return redirect(to='dashboard')
    if request.method == 'POST':
        username = request.POST['uname']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, 'Please enter all fields')
            return redirect(to='adminstart')
        
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            auth.login(request, user)
            request.session['sessionadmin'] = username
            return redirect('dashboard')
            
        else:
            messages.info(request, 'Invalid credentials')
            return render(request, 'adminstart.html')
    else:
        
       return render (request,"adminstart.html")

@login_required(login_url='adminstart')
@never_cache
def delete_product(request):
    id=request.GET['id']
    product=Product.objects.filter(id=id)
    product.delete()
    return redirect('products')

@login_required(login_url='adminstart')
@never_cache
def delete_category(request):
    id=request.GET['id']
    category=Category.objects.filter(id=id)
    category.delete()
    return redirect('category')

def cancelorder(request):
    user=request.user
    id=request.GET['id']
    Order.objects.filter(id=id).update(status='Cancelled',cancel=True)
    
    
    return redirect('orders')


def updatestatus(request):
    id=request.GET['id']
    status=request.POST['status']
    
    print(id,status)
    Order.objects.filter(id=id).update(status=status)
    return redirect('orders')


@login_required(login_url='adminlogin')
def coupons(request):
    coupon=Coupon.objects.all()
    return render(request, 'coupon_management.html',{'coupons':coupon})



def addcoupon(request):
    if request.method == 'POST':
        code = request.POST['code']
        discount = request.POST['discount']
        min_amount = request.POST['discount']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        coupon = Coupon.objects.create(code=code,discount=discount,min_amount=min_amount,start_date=start_date,end_date=end_date)
        return redirect('addcoupon')
    else:
        return render(request, "add_coupon.html")

@login_required(login_url='adminstart')
@never_cache
def offers(request):
    if request.method == 'POST':

        ids = request.POST['category']
        print(ids)
        allcategory = Category.objects.all()
        
        categories = Category.objects.get(id=ids)
        print(categories)
        subcategories=categories.sub_categories.all().order_by('id')[1:]
       
        print(subcategories)
        return render(request, 'offer_management.html', {'categories': categories,'subcategories': subcategories,'allcategory':allcategory})
        
    else:
        allcategory = Category.objects.all()
        return render(request,'offer_management.html',{'allcategory': allcategory})



@login_required(login_url='adminstart')
def prod_addoffer(request):
    if request.method == 'POST':
        name = request.POST['name']
        offer = request.POST['offer']
        startdate = request.POST['startdate']
        max_value = request.POST['max_value']
        print(startdate)
        enddate = request.POST['enddate']
        print( "end",enddate)
        product = request.POST['product']
        print(product)
        offer = Offers.objects.create(name=name,offer=offer,start_date=startdate,end_date=enddate,offer_type='product',product_id=product,max_value=max_value)
        offer.save()
        return redirect('offers')
    else:
        products=Product.objects.all()
        return render(request, "prod_addoffer.html",{'products':products})

@login_required(login_url='adminlogin')
def cate_addoffer(request):
    if request.method == 'POST':
        name = request.POST['name']
        offer = request.POST['offer']
        startdate = request.POST['startdate']
        max_value = request.POST['max_value']
        print(startdate)
        enddate = request.POST['enddate']
        print( "end",enddate)
        category = request.POST['category']
         
        offer = Offers.objects.create(name=name,offer=offer,start_date=startdate,end_date=enddate,offer_type='category',category_id=category,max_value=max_value)
        offer.save()
        return redirect('offers')
    else:
        category=Category.objects.all()
        return render(request, "cate_add_offer.html",{'category':category})







@login_required(login_url='adminstart')
@never_cache
def logout(request):
    # user=request.user
    auth.logout(request)
    return redirect('adminstart')

