

from operator import ne
from plistlib import UID
import profile
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User, auth
from guest_user.models import Guest
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
from django.http import JsonResponse
from guest_user.decorators import allow_guest_user
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException,TwilioException


generatedotp=0
offerprice=0



@never_cache
def loginpage(request):
    if request.user.is_authenticated and request.user.is_superuser == False and request.user.first_name !='':
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


# def guestsignup(request):
#     print(request.user.id)
#     id = request.user.id
    
#     if request.method == 'POST'  and 'otp' not in request.POST:
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         phone = request.POST['phone']
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         print("username=", username)
#         print(password)
        
       
       
#         user = User.objects.create_user(id=id,
#         first_name=first_name, last_name=last_name,  username=username, email=email, password=password)
#         user.save_base()
#         user_id = User.objects.get(username=username)
#         account = Accounts.objects.create(user=user_id, phone=phone)
#         account.save()
#         guest = Guest.objects.get(user_id=id)
#         guest.delete()
#         print('user created')
#         return render(request,'login.html')
        
#     elif request.method == 'POST':
#         phone = request.POST['phone']
#         # otp=968542
#         global generatedotp
#         otp = random.randint(100000, 999999)
#         generatedotp=otp
        
       
#         if otp == generatedotp:
#             return render(request, "signup.html",{ 'phone': phone})
#         else:
#           return redirect('mobile')
  
#     else:
#         return render(request, 'guestsignup.html')



def signup(request):
    print(request.user.id)
    id = request.user.id
    
    if request.method == 'POST'  and 'otp' not in request.POST:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        print("username=", username)
        print(password)
        
       
       
        user = User.objects.create_user(id=id,
        first_name=first_name, last_name=last_name,  username=username, email=email, password=password)
        user.save_base()
        user_id = User.objects.get(username=username)
        account = Accounts.objects.create(user=user_id, phone=phone)
        account.save()
        guest = Guest.objects.get(user_id=id)
        guest.delete()
        print('user created')
        return render(request,'login.html')
        
        
    elif request.method == 'POST':
        phone = request.POST['phone']
        # otp=968542
        # otp = random.randint(100000, 999999)
        global generatedotp
        otp1 =int( request.POST['otp'])
        
        print(otp1)
        if generatedotp == otp1:
            return render(request, "signup.html",{ 'phone': phone})
        else:
            return render(request, "signup.html",{ 'phone': phone})
  
    else:
        return render(request, 'signup.html')



@login_required(login_url='login')
@never_cache
def homepage(request):
    product = Product.objects.all()
    categories = Category.objects.all().order_by('id')[1:]
    brands = Brand.objects.all()
    # subcategories=categories.sub_categories.all().order_by('id')[1:]
    
    
    if request.user.is_authenticated and request.user.is_superuser == False:
        print(request.user.is_authenticated)
        user = request.user
        print('user=', user)
 
        return render(request, 'home.html', {'user': user, 'products': product, 'categories': categories,'brands':brands})
    else:
        return render(request, 'start.html', {'products': product, 'categories': categories})

@allow_guest_user()
@never_cache
def startpage(request):
    if request.user.is_authenticated and request.user.is_superuser == False and request.user.first_name !='':
        return redirect('home')
    else:
        product = Product.objects.all()
        categories = Category.objects.all().order_by('id')[1:]
        brands = Brand.objects.all()

    return render(request, 'start.html', {'products': product, 'categories': categories, 'brands':brands})


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
        try:
            num = Accounts.objects.filter(phone=phone)
            message_handler = MessageHandler(phone,num[0].otp).sent_otp_on_phone()
            return redirect(f'otp/{num[0].uid}')
            print(message.sid)
        except (TwilioRestException,TwilioException):
            messages.info(request, "Something Error occured, please try again later",extra_tags='phone_login')
            return redirect(to='login')
@never_cache
def otplogin(request,uid):
    if request.user.is_authenticated and request.user.is_superuser == False and request.user.first_name !='':
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

def product_view(request):
    id = request.GET['id']
    product = Product.objects.get(id=id)
    
    print(product)
    print(id)
    
    prdct = Product.objects.filter(id=id)
    print(prdct)
    off=''
    offc=''
    offb=''
    categories=Category.objects.get(product=id)
    print(categories.id)
    if Offers.objects.filter(product_id=id).exists():
        off=Offers.objects.get(product_id=id)
        print("off",off.offer)
    if Offers.objects.filter(category=categories.id).exists():
        offc = Offers.objects.get(category=categories.id)
        print("offc",offc.offer)
    if Offers.objects.filter(brand=product.brand).exists():
        offb = Offers.objects.get(brand=product.brand)
        print("offb",offb.offer)        
        
    images = Images.objects.filter(product=prdct[0].id)

    offers = Offers.objects.all()
    for offer in offers:
        print(offer.product)
        print(prdct[0])
        if offer.product == prdct[0]:
            for ofr in offers:
              
                if ofr.category == product.category:
                    print("ofr=",ofr.name)
                    if ofr.offer<offer.offer:
                        print("offer",offer.offer)
                            
                        return render(request, 'product_view.html',{'product': product, 'images': images, 'offer': offer, 'offc':offc, 'off': off,'offb': offb})
                    else:
                        return render(request, 'product_view.html',{'product': product, 'images': images, 'offer':ofr,  'offc':offc, 'off': off,'offb': offb})
                    
        else: 
            for ofr in offers:
                if ofr.category == product.category:
                    print("elseofr=",ofr.name)
                    return render(request, 'product_view.html',{'product': product, 'images': images, 'offer':ofr, 'offc':offc, 'off': off,'offb': offb})
        return render(request, 'product_view.html', {'product': product, 'images': images, 'offer':ofr, 'offc':offc, 'off': off,'offb': offb})
    else:
        return redirect('home')
    


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
            # otp = 968542
            global generatedotp
            otp = random.randint(100000, 999999)
            generatedotp=otp
            print(otp)
            try:
                message_handler = MessageHandler(phone, otp).sent_otp_on_phone()
                return render(request, "enterotp.html",{ 'phone': phone,'generatedotp':generatedotp})
            except (TwilioRestException,TwilioException):
                messages.info(request, "Something Error occured, please try again later")
                return redirect(to='mobile')
     

    return render(request,"enterphone.html")



def addtocart(request):
    pid = request.GET['pid']

    product = Product.objects.get(id=pid)
    print(product.brand)
    offers = Offers.objects.all()
    
    uid = request.user
    print("pid =", pid)
    print("uid =", uid)
    if UserCart.objects.filter(product=pid, user=uid).exists():
        cart = UserCart.objects.get(product=pid, user=uid)
        cart.quantity = cart.quantity+1
        cart.save()
        return redirect('mycart')
    else:
        global offerprice
        price = 0
        offerprice=product.price
        for offer in offers:
            
            print(offerprice)
            
            category=Category.objects.get(product=pid)
            
            
            if offer.product == product or offer.category == category or offer.brand == product.brand :
                
                
                offamount = product.price * offer.offer / 100
         
               
                if offamount > offer.max_value:
                    
                    price = product.price - offer.max_value
                    if price < offerprice:
                        
                        offerprice=price
                else:
                    
                    price = product.price - offamount
                    
                    if price < offerprice:
                        offerprice=price
                        
        cart = UserCart.objects.create(
        user=uid, product=product, quantity=1, price_with_offer=offerprice)
        cart.save_base()
        return redirect('mycart')
                   



            
def updatecartpage(request):
    return render(request,'mycart.html')

@login_required(login_url='login')
def myprofile(request):
    user = request.user
    address = Address.objects.filter(user=user)
    # user_details = User.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'address': address})

def addtomycart(request):
    print(request.method)
    if request.method == 'POST':
        if request.user.is_authenticated:
            
            uid = request.user
            prod_id = int(request.POST.get('product_id'))
            print(prod_id)
            if UserCart.objects.filter(product=prod_id, user=uid).exists():
                prod_qty = int(request.POST.get('product_qty')) 
                print(prod_qty)
                cart = UserCart.objects.get(product=prod_id, user=uid)
                cart.quantity=prod_qty
                cart.save()  
                return redirect('mycart')


        else:
            return redirect('login')
    
    
    else:
        if request.user.is_authenticated:
            user = request.user
            cart = UserCart.objects.filter(user=user).order_by('-id')
            offers = Offers.objects.all()
            if len(cart) == 0:
                print('working')
                empty = "Cart is Empty"
                cartlen=len(cart)
                return render(request, 'mycart.html', {'empty': empty,'cartlen': cartlen,'offers': offers,})
            else:
                for carts in cart[0].product.category.all():
                    print("catid =", carts.id)

            # for products in cart:

            #     categories = Category.objects.get(product=products.product.id)
            #     print(categories.id)
                       
            print(len(cart))
            for i in range(len(cart)):
                 if cart[i].quantity < 1:
                    cart[i].delete()
        else:
            return redirect('login')

        if len(cart) == 0:
            print('working')
            empty = "Cart is Empty"
            cartlen=len(cart)
            if request.user.first_name !='':
                realuser=True
                return render(request, 'mycart.html', {'empty': empty,'cartlen': cartlen,'offers': offers,'realuser':realuser})
            else:
                return render(request, 'mycart.html', {'empty': empty,'cartlen': cartlen,'offers': offers,})
        else:
  
            subtotal = 0
            for i in range(len(cart)):
                if cart[i].price_with_offer !=0:
                        x = cart[i].price_with_offer*cart[i].quantity
                        subtotal = subtotal+x
                    
                else:
                        x = cart[i].product.price*cart[i].quantity
                        subtotal = subtotal+x
                    
 
            shipping = 0
            total = subtotal + shipping
            print(total)
            if request.user.first_name !='':
               realuser=True
               
               return render(request, 'mycart.html', {'cart': cart, 'subtotal': subtotal, 'total': total,'realuser':realuser,'offers': offers,})
            else:
                return render(request, 'mycart.html', {'cart': cart, 'subtotal': subtotal, 'total': total,'offers': offers,})

@login_required(login_url='login')
def checkout(request):
    print('checkput')
    if request.method == 'POST' and 'address_id' in request.POST :
    
        address_id = request.POST['address_id']
        address = Address.objects.get(id=address_id)
        cart = UserCart.objects.filter(user=request.user)
        subtotal = 0
        for i in range(len(cart)):
                if cart[i].price_with_offer !=0:
                    x = cart[i].price_with_offer*cart[i].quantity
                    subtotal = subtotal+x
                else:
                    x = cart[i].product.price*cart[i].quantity
                    subtotal = subtotal+x
        shipping = 0
        total = subtotal+shipping
        return render(request, 'payment.html', {'subtotal': subtotal, 'total': total, 'addresses': address,'cart':cart})     
    
    
    elif request.method == 'POST' and 'code' in request.POST:
        user = request.user
        method = request.POST['payment']
        amount = request.POST['amount']
        address = request.POST['address']
        addresses = Address.objects.get(id=address)
        cart = UserCart.objects.filter(user=user)
        print("address",address)
        total = float(request.POST['amount'])
        code = request.POST['code']
        print(code)
        subtotal = 0
        for i in range(len(cart)):
            if cart[i].cancel != True:
                if cart[i].price_with_offer !=0:
                    x = cart[i].price_with_offer*cart[i].quantity
                    subtotal = subtotal+x
                else:
                    x = cart[i].product.price*cart[i].quantity
                    subtotal = subtotal+x
        shipping = 0
        message=False
        coupon = Coupon.objects.get(code=code)
        min_amount = coupon.min_amount*2
        print(min_amount)
        if total>min_amount:
            total = total-coupon.discount
        else:
            message = "Minimum Amount is not reached"    
        print(message)
        print(total)
        return render(request, 'payment.html', { 'subtotal':subtotal,'total': total,'message':message, 'addresses': addresses,'cart':cart, 'code':code, 'offer':coupon})
    else:
        print('else===')
        user = request.user
        cart = UserCart.objects.filter(user=user)
        addresses = Address.objects.filter(user=user)
        print(addresses)
        print(cart)
        subtotal = 0
        for i in range(len(cart)):
                if cart[i].price_with_offer !=0:
                    x = cart[i].price_with_offer*cart[i].quantity
                    subtotal = subtotal+x
                else:
                    x = cart[i].product.price*cart[i].quantity
                    subtotal = subtotal+x
        shipping = 0
        total = subtotal+shipping
        # return HttpResponse('else')
        return render(request, 'checkout.html', {'subtotal': subtotal, 'total': total, 'addresses': addresses})

def razorpay(request):
    cart = UserCart.objects.filter(user=request.user)
    subtotal = 0
    print(subtotal)
    for i in range(len(cart)):
        x = cart[i].product.price*cart[i].quantity
        subtotal = subtotal+x
    shipping = 0
    total = subtotal+shipping
    return JsonResponse({
                         'total': total,})


@login_required(login_url='login')
def addaddress(request):

    if request.method == 'POST':
        user = request.user
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']
        address = Address.objects.create(
            name=name, phone=phone, address=address, city=city, state=state, pincode=pincode, user=user)
        address.save()
        return redirect('checkout')
    else:
        return render(request, 'addaddress.html')

def payment(request):
    if request.method == 'POST':
        user = request.user
        method = request.POST['payment']
        amount = request.POST['amount']
        print(amount)
        cart = UserCart.objects.filter(user=user)
        address = request.POST['address']
        print("address",address)
        address = Address.objects.get(id=address)
        subtotal = 0
        for i in range(len(cart)):
            x = cart[i].product.price*cart[i].quantity
            # prdct.quantity=prdct.quantity-cart[i].quantity
            subtotal = subtotal+x
        shipping = 0
        total = subtotal + shipping
        crt = UserCart.objects.filter(user=user)
        print(method)
        order = Order.objects.create(
            user=user, address=address, amount=amount, method=method)
        order.save()
        for i in range(len(cart)):
            oldcart = AdminCart.objects.create(
                user=user, quantity=crt[i].quantity, product=crt[i].product, order=order)
            oldcart.save()
        cart.delete()
        prdcts=AdminCart.objects.filter(order=order)
        for i in range(len(prdcts)-1):
            p=Product.objects.filter(id=prdcts[i].product.id)
            # # print("qty",p[i].quantity)
            # print("cartqty",prdcts[i].quantity)
            # print("pqty",p[i].quantity-prdcts[i].quantity)
            # print("pid",prdcts[i].product.id)
            Product.objects.filter(id=prdcts[i].product.id).update(quantity=p[i].quantity-prdcts[i].quantity)
        success = True
        product = Product.objects.all()
        categories = Category.objects.all()
        print("==",categories)
        payMode=request.POST['payment']
        if payMode=='Razorpay' or  payMode=='Paypal':
            print(payMode)
            return JsonResponse({'status' : "Your Order has been placed successfully"})
        return render(request, 'home.html', {'user': user, 'products': product, 'categories': categories, 'success': success})
    else:
        user = request.user
        cart = UserCart.objects.filter(user=user)
        subtotal = 0
        for i in range(len(cart)):
            x = cart[i].product.price*cart[i].quantity
            subtotal = subtotal+x
        shipping = 0
        total = subtotal + shipping
        return render(request, 'payment.html', {'subtotal': subtotal, 'total': total, 'cart': cart})

@login_required(login_url='login')
def myorder(request):
    order = Order.objects.filter(user=request.user).order_by('-id')
    cart = UserCart.objects.filter(user=request.user)
    oldcart = AdminCart.objects.filter(user=request.user)
    if len(order) == 0:
        empty = "No Order Placed"
        return render(request, 'myorders.html', {'empty': empty})
    subtotal = 0
    for i in range(len(cart)):
        x = cart[i].product.price*cart[i].quantity
        subtotal = subtotal+x
    shipping = 0
    total = subtotal + shipping
    return render(request, 'myorders.html', {'orders': order, 'cart': oldcart, 'total': total})


def cancelorder(request):
    user = request.user
    id = request.GET['id']
    Order.objects.filter(id=id).update(status='Cancelled', cancel=True)
    return JsonResponse({'status': True})
    # return redirect('myorder')

def removecart(request):
    id=request.GET['id']
    print(id)
    cart = UserCart.objects.get(id=id)
    cart.delete()
    return redirect('mycart')


def deleteaddress(request):
    id=request.GET['id']
    address = Address.objects.get(id=id)
    address.delete()
    return redirect('profile')

@login_required(login_url='adminstart')

def editprofile(request):
    id=request.GET['id']
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        email = request.POST['email']
        
 
        user = User.objects.filter(id=id).update(first_name=first_name, last_name=last_name,email=email)
        
        Accounts.objects.filter(user_id=id).update(phone=phone)
        print('user updated')
        return render(request,'profile.html')
    else:
         user = User.objects.filter(id=id)
         return render(request,"editprofile.html",{'user':user})

def date_select(request):
    start = request.POST['start_date']
    end = request.POST['end_date']
    print("end=",end)
    order = Order.objects.filter(ordered_date__range=[start,end])
    if len(order) ==0:
        # messages.info(request, 'No Orders Found')
        return render(request, 'sales.html')
    else:
        return render(request, 'sales.html',{'orders':order})

def changepassword(request):
    id=request.GET['id']
    if request.method == 'POST':
        fname=request.POST['first_name']
        lname=request.POST['last_name']
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
 
        user = User.objects.create_user(id=id,username=username, password=password, first_name=fname, last_name=lname, email=email)
        print(user.password)
        user.save_base()
        print('success')
        success=True
        return render(request,"login.html",{"success":success})
    else:
         user = User.objects.filter(id=id)
         return render(request,"changepassword.html",{'user':user})

def error(request):
  return render(request,"404.html")
