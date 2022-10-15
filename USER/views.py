

from operator import ne
from plistlib import UID
import profile
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from USER.models import Accounts
from ADMIN.models import *
from .models import *
from django.db.models import Sum
from .mixins import MessageHandler
import random

@never_cache
def loginpage(request):
    if request.user.is_authenticated and request.user.is_superuser == False:
        return redirect('home')
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST :
        username = request.POST['username']
        password = request.POST['password']
        if len(username) == 0 or len(password) == 0:
            messages.info(request, "Please enter all fields",extra_tags='user_login')
            return redirect(to='login')      
        user = auth.authenticate(request, username=username, password=password)

        if user is not None and user.is_active and user.is_superuser == False:
            auth.login(request, user)
            return redirect(to='home')
        else:
            messages.info(request, "Invalid credentials", extra_tags='user_login')
            return redirect(to='login')
                
    else:
        return render(request, 'login.html')



def signup(request):
    


    if request.method == 'POST'  and 'otp' not in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        print("username=", username)
        print(password)
        
       
       
        user = User.objects.create_user(
        first_name=first_name, last_name=last_name,  username=username, email=email, password=password)
        user.save()
        user_id = User.objects.get(username=username)
        account = Accounts.objects.create(user=user_id, phone=phone)
        account.save()
        print('user created')
        return render(request,'login.html')
        
    elif request.method == 'POST':
        phone = request.POST['phone']
        otp=968542

        otp1 =int( request.POST['otp'])
        print(otp)
        print(otp1)
        if otp == otp1:
            return render(request, "signup.html",{ 'phone': phone})
        else:
          return redirect('mobile')
  
    else:
        return render(request, 'signup.html')



@login_required(login_url='login')
@never_cache
def homepage(request):
    product = Product.objects.all()
    categories = Category.objects.all()
    if request.user.is_authenticated:
        print(request.user.is_authenticated)
        user = request.user
        print('user=', user)
        return render(request, 'home.html', {'user': user, 'products': product, 'categories': categories})
    else:
        return render(request, 'start.html', {'products': product, 'categories': categories})

def startpage(request):
    product = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'start.html', {'products': product, 'categories': categories})


def getotp(request):
    phone = request.POST['phone']
    if len(phone) == 0 :
            messages.info(request, "Please enter all fields",extra_tags='phone_login')
            return redirect(to='login')

    otp = random.randint(100000, 999999)
    i = False
    while i == False:
       if phone.isdigit():
           i = True
       else:
            messages.info(request, "Invalid Mobile Number",extra_tags='phone_login')
            return redirect(to='login')
           
    
    if not Accounts.objects.filter(phone=phone).exists():
        messages.info(request, "Phone Number Not Registered", extra_tags='phone_login' )
        return redirect('login')
    else:
        num = Accounts.objects.filter(phone=phone).update(otp=otp)
        user = Accounts.objects.get(phone=phone)

    
    print(user.user)
    if user.user.is_active == False or user.user.is_superuser:
        messages.info(request, "Phone Number Not Registered", extra_tags='phone_login' )
        return redirect('login')
    else:
       num = Accounts.objects.filter(phone=phone)
       message_handler = MessageHandler(phone,num[0].otp).sent_otp_on_phone()
       return redirect(f'otp/{num[0].uid}')

@never_cache
def otplogin(request,uid):
    if request.user.is_authenticated and request.user.is_superuser == False:
        return redirect('home')
    if request.method == 'POST':
        otp=request.POST.get('otp')
        accounts = Accounts.objects.get(uid=uid)
     
        if otp == accounts.otp:
            login(request,accounts.user)
            return redirect('home')
        else:
          return redirect(f'/otp/{uid}')
    else:
     return render(request,"otp.html")


@never_cache
def logout(request):
    # user=request.user
    auth.logout(request)
    return redirect('start')

def view_product(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    print(product)
    prdct = Product.objects.filter(id=id)
    print(prdct)
    images = Images.objects.filter(product=prdct[0].id)
    print(images)
    return render(request, 'view_product.html', {'product': product, 'images':images})

def mobile_signup(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        if len(phone) == 0 :
            messages.info(request, "Please enter all fields",extra_tags='user_login')
            return redirect(to='mobile')
        
        elif Accounts.objects.filter(phone=phone).exists():
             messages.info(request, 'Mobile Number Already Registered')
             return redirect('mobile')
        else:
            otp = 968542
            print(otp)
            message_handler = MessageHandler(phone, otp).sent_otp_on_phone()
            return render(request, "enterotp.html",{ 'phone': phone})

    return render(request,"enterphone.html")

def cartpage(request):
     if request.user.is_authenticated:
        user = request.user
        cart = UserCart.objects.filter(user=user)
        
        return render(request,'mycart.html',{'cart':cart})




def addtocart(request):
    pid = request.GET['pid']
    product = Product.objects.get(id=pid)
    uid = request.user
    print("pid =", pid)
    print("uid =", uid)
    if UserCart.objects.filter(product=pid, user=uid).exists():
        cart = UserCart.objects.get(product=pid, user=uid)
        cart.quantity = cart.quantity+1
        cart.save()
        return redirect('mycart')
    else:
        cart = UserCart.objects.create(product=product, user=uid)
        cart = UserCart.objects.filter(user=uid)
        return redirect('mycart')

            
