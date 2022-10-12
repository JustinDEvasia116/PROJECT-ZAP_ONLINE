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
    return render(request,"dashboard.html")


@login_required(login_url='adminstart') 
def orders(request):
    return render(request,"orders.html")


@login_required(login_url='adminstart')
def users(request):
     user_details=User.objects.filter(is_superuser=False)
     return render(request, 'users.html',{'user_details':user_details})

@login_required(login_url='adminstart')
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
        
        category=Category.objects.get(id=category)
        product = Product.objects.create(name=name,description=description,price=price,category=category,image=image,brand=brand,quantity=quantity)
        product.save()
        return redirect('addproduct')
    else:
        
        category=Category.objects.all()
        return render(request, 'addproduct.html',{'categories':category})
    
@login_required(login_url='adminstart')
def addcategory(request):
    if request.method == 'POST':
        name = request.POST['name']
        image = request.FILES['image']
        category = Category.objects.create(name=name,image=image)
        category.save()
        return redirect('category')
    else:
        return render(request, 'addcategory.html')

@login_required(login_url='adminstart')
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
def products(request):
    product=Product.objects.all()
    return render(request, 'products.html',{'products':product})

@login_required(login_url='adminstart')
def category(request):
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

@login_required(login_url='adminstart')
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
def delete_product(request):
    id=request.GET['id']
    product=Product.objects.filter(id=id)
    product.delete()
    return redirect('products')

@login_required(login_url='adminstart')
def delete_category(request):
    id=request.GET['id']
    category=Category.objects.filter(id=id)
    category.delete()
    return redirect('category')

@login_required(login_url='adminstart')
@never_cache
def logout(request):
    # user=request.user
    auth.logout(request)
    return redirect('adminstart')
