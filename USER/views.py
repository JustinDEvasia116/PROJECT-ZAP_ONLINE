

import profile
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from USER.models import Accounts
from ADMIN.models import *
from .models import *
from django.db.models import Sum
from .mixins import MessageHandler
import random
# Create your views here.
# def loginpage(request):
#     if 'sessionlog' in request.session:
#         print(request.session)
#         return redirect(to='home')
    
#     if request.method == 'POST':
#         username=request.POST['username']
#         password=request.POST['password']
#         if len(username) == 0 or len(password) == 0:
#             messages.info(request, 'Please enter all fields')
#             return redirect(to='login')
#         else:
#             user = auth.authenticate(username=username, password=password)
            
#             if user is not None and user.is_superuser==False:
#                 auth.login(request, user)
#                 request.session['sessionlog'] = username
#                 return redirect(to='home')
#             else:
#                 messages.info(request, 'Invalid credentials')
#                 return redirect(to='start')
                
        
#     else:
#         return render(request, 'login.html')

def loginpage(request):
    # if request.user.is_authenticated and request.user.is_superuser == False:
    #     return redirect('home')
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST and 'otp' not in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.get(username=username)
        
        user = auth.authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser==False:
            auth.login(request, user)
            return redirect(to='home')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect(to='login')
                
    # elif request.method == 'POST' and 'otp' in request.POST:
    #     otp = request.POST['otp']
    #     print(otp)
        
    #     if Accounts.objects.filter(otp=otp).exists():
    #         user = auth.authenticate(request, username=username, password=password)
    #         print("user = ", user)

    #     if user is not None and user.is_active and user.is_superuser == False:
    #         auth.login(request, user)
    #         return redirect(to='home')
    #     else:
    #         messages.info(request, "Invalid Credentials")
    #         return redirect('login')
    else:
        return render(request, 'login.html')



def signup(request):
    
    if request.method == 'POST':
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
        
    else:
        return render(request, 'signup.html')



def homepage(request):
    product = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {'products': product, 'categories': categories})

def getotp(request):
    phone = request.POST['phone']
    if not Accounts.objects.filter(phone=phone).exists():
        messages.info(request, "Phone Number Not Registered")
        return redirect('login')
    else:
        number = Accounts.objects.get(phone=phone)
        num = Accounts.objects.filter(phone=phone)
        
        print('1', number.phone)
        user = User.objects.get(id=number.user_id)
        num[0].otp = random.randint(100000, 999999)
        num[0].save()
        print(num[0].otp)

        message_handler = MessageHandler(phone,num[0].otp).sent_otp_on_phone()
        return redirect(f'otp/{num[0].uid}')

def otplogin(request,uid):
    if request.method == 'POST':
        otp=request.POST.get('otp')
        accounts = Accounts.objects.get(uid=uid)
        if otp == accounts.otp:
            login(request,accounts.user)
            return redirect('home')
        else:
          return redirect(f'otp/{uid}')
    else:
     return render(request,"otp.html")





            
