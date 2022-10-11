import imp
from django.shortcuts import render,redirect
from .models import *
from USER.models import *
from ADMIN.models import Category, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
def loginpage(request):
    return render(request,"login.html")

def signup(request):
    return render(request, 'signup.html')

def otppage(request):
    return render(request,"otp.html")

def homepage(request):
    product = Product.objects.all()
    categories = Category.objects.all()

    return render(request, 'home.html', {'products': product, 'categories': categories})