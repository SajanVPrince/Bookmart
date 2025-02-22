from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import *
from .models import *
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

# Create your views here.

def bk_login(req):
    if 'user' in req.session:
        return redirect(userpro)
    if 'shop' in req.session:
        return redirect(adminpro)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['password']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['shop']=uname
                return redirect(adhome)
            else:
                login(req,data)
                req.session['user']=uname
                req.session['user1']= data.id
                return redirect(bk_home)
        else:
            messages.warning(req,"Invalid uname or password")
            return redirect(bk_login)
    else:
        return render(req,'login.html')

def bk_logout(req):
    req.session.flush()          
    logout(req)
    return redirect(bk_login)


def register(req):
    if req.method == 'POST':
        fname = req.POST['fname']
        email = req.POST['email']
        password = req.POST['password']
        if User.objects.filter(email=email).exists():
            messages.warning(req, "Email already registered")
            return redirect('register')
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        req.session['email'] = email
        req.session['fname'] = fname
        req.session['password'] = password
        send_mail(
            'Your OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP sent to your email")
        return redirect('verify_otp_reg')
    return render(req, 'register.html')

def verify_otp_reg(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp'] 
        stored_otp = req.session.get('otp')
        email = req.session.get('email')
        fname = req.session.get('fname')
        password = req.session.get('password')
        if entered_otp == stored_otp:
            user = User.objects.create_user(first_name=fname,email=email,password=password,username=email)
            user.is_verified = True
            user.save()      
            messages.success(req, "Registration successful! You can now log in.")
            send_mail('User Registration Succesfull', 'Account Created Succesfully And Welcome To Bookmart', settings.EMAIL_HOST_USER, [email])
            return redirect('login')
        else:
            messages.warning(req, "Invalid OTP. Try again.")
            return redirect('verify_otp_reg')

    return render(req, 'verify_oto_reg.html')

def resend_otp_reg(req):
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        
        send_mail(
            'Your New OTP Code',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER, [email]
        )
        messages.success(req, "OTP resent to your email")
    
    return redirect('verify_otp_reg')
        
def forgetpassword(req):
    if req.method == 'POST':
        email = req.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = get_random_string(length=6, allowed_chars='0123456789')
            req.session['otp'] = otp
            req.session['email'] = email
            send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
            messages.success(req, "OTP sent to your email")
            return redirect('verify_otp')
        except User.DoesNotExist:
            messages.warning(req, "Email not found")
            return redirect('forgetpassword')
    return render(req, 'forgetpassword.html')

def verify_otp(req):
    if req.method == 'POST':
        otp = req.POST['otp']
        if otp == req.session.get('otp'):
            return redirect('resetpassword')
        else:
            messages.warning(req, "Invalid OTP")
            return redirect('verify_otp')
    return render(req, 'verify_otp.html')

def resend_otp(req):  
    email = req.session.get('email')
    if email:
        otp = get_random_string(length=6, allowed_chars='0123456789')
        req.session['otp'] = otp
        send_mail('Password Reset OTP', f'Your OTP is: {otp}', settings.EMAIL_HOST_USER, [email])
        messages.success(req, "OTP resent to your email")
    return redirect('verify_otp')

def resetpassword(req):
    if req.method == 'POST':
        password = req.POST['password']  
        email = req.session.get('email')
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            messages.success(req, "Password reset successfully")
            return redirect('login')
        except User.DoesNotExist:
            messages.warning(req, "Error resetting password")
            return redirect('resetpassword')
    return render(req, 'resetpassword.html')
    
# ------------------------ADMIN---------------------

def adminpro(req):
    return render(req,'admin/adminprofile.html')

def adhome(req):
    if req.method=='POST':
        name=req.POST['name']
        ath_name=req.POST['ath_name']
        price=req.POST['price']
        ofr_price=req.POST['ofr_price']
        bk_genres=req.POST['bk_genres']
        img=req.FILES['img']
        dis=req.POST['dis']
        stock=req.POST['stock']
        data=Books.objects.create(name=name,ath_name=ath_name,price=price,ofr_price=ofr_price,bk_genres=bk_genres,img=img,dis=dis,stock=stock)
        data.save()
        return redirect(adhome)
    else:
        return render(req,'admin/admin.html')
    

def addbook(req):
    if 'shop' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            ath_name=req.POST['ath_name']
            price=req.POST['price']
            ofr_price=req.POST['ofr_price']
            bk_genres=req.POST['bk_genres']
            img=req.FILES['img']
            dis=req.POST['dis']
            stock=req.POST['stock']
            data=Books.objects.create(name=name,ath_name=ath_name,price=price,ofr_price=ofr_price,bk_genres=bk_genres,img=img,dis=dis,stock=stock)
            data.save()
            return redirect(addbook)
        else:
            return render(req,'admin/addbook.html')
    else:
        return redirect(bk_login)
    

def search(req):
    if 'shop' in req.session:
        if req.method=='POST':
            search=req.POST['search']
            data=Books.objects.filter(name__contains=search)
            return render(req,'user/search.html',{'data':data})
    else:
        return redirect(bk_login)
    
def viewbook(req):
    if 'shop' in req.session:
        data=Books.objects.all()
        return render(req,'admin/books.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_book(req,id):
    book=Books.objects.get(pk=id)
    book.delete()
    return redirect(viewbook)

def edit_book(req,id):
    if 'shop' in req.session:
        data=Books.objects.get(pk=id)
        if req.method=='POST':
            bk_name=req.POST['bk_name']
            ath_name=req.POST['ath_name']
            bk_price=req.POST['bk_price']
            bk_genres=req.POST['bk_genres']
            img=req.FILES['img']
            bk_dis=req.POST['bk_dis']
            stock=req.POST['stock']
            data.bk_name=bk_name
            data.ath_name=ath_name
            data.bk_price=bk_price
            data.bk_genres=bk_genres
            data.img=img
            data.bk_dis=bk_dis
            data.stock=stock
            data.save()
            return redirect(viewbook)
        else:
            return render(req,'admin/edit.html',{'data':data})
    else:
        return redirect(bk_login)
    
def view_sbook(req):
    if 'shop' in req.session:
        data=Sbook.objects.all()
        return render(req,'admin/sbooks.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_sbook(req,id):
    book=Sbook.objects.get(pk=id)
    book.delete()
    return redirect(view_sbook)

def view_user(req):
    if 'shop' in req.session:
        data=User.objects.all()
        return render(req,'admin/users.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_user(req,id):
    user=User.objects.get(pk=id)
    user.delete()
    return redirect(view_user)
   
def view_buy(req):
    if 'shop' in req.session:
        data=Buys.objects.all()
        return render(req,'admin/buy.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_buy(req,id):
    buy=Buys.objects.get(pk=id)
    buy.delete()
    return redirect(view_buy)
    

def view_review(req):
    if 'shop' in req.session:
        data=Review.objects.all()
        return render(req,'admin/review.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_review(req,id):
    review=Review.objects.get(pk=id)
    review.delete()
    return redirect(view_review)
    



    

    

# -----------------------User-------------------------


def bk_home(req):
    data=Books.objects.filter(bk_genres='drama')[::-1][:4]
    data1=Books.objects.filter(bk_genres='sci-fi')[::-1][:4]
    data2=Books.objects.filter(bk_genres='love')[::-1][:4]
    data3=Books.objects.filter(bk_genres='fantasy')[::-1][:4]
    if 'user' in req.session:
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            review=req.POST['review']
            data4=Review.objects.create(user=user,review=review)
            data4.save()
            messages.success(req,"Thanks for your complements")
    
    rev=Review.objects.all()[::-1]
    return render(req,'user/home.html',{'data':data,'data1':data1,'data2':data2,'data3':data3,'rev':rev})

def sell(req):
    if 'user' in req.session:
        data=Sbook.objects.all()[::-1]
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            bk_name=req.POST['bk_name']
            ath_name=req.POST['ath_name']
            bk_price=req.POST['bk_price']
            bk_genres=req.POST['bk_genres']
            img=req.FILES['img']
            bk_dis=req.POST['bk_dis']
            data=Sbook.objects.create(user=user,sname=bk_name,sath_name=ath_name,sprice=bk_price,sbk_genres=bk_genres,simg=img,sdis=bk_dis)
            data.save()
            return redirect(sell)
        else:
            return render(req,'user/sell.html',{'data':data})
    else:
        return redirect(bk_login)


def view_prod(req,id):
    data=Books.objects.get(pk=id)
    return render(req,'user/viewprod.html',{'data':data})

def sview_prod(req,id):
    data=Sbook.objects.get(pk=id)
    return render(req,'user/sviewprod.html',{'data':data})

def userpro(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data1=Userdtl.objects.filter(user=user)
        if req.method == 'POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            altphn=req.POST['altphn']
            pin=req.POST['pin']
            land=req.POST['land']
            adrs=req.POST['adrs']
            city=req.POST['city']
            state=req.POST['state']
            data=Userdtl.objects.create(user=user,fullname=name,phone=phn,pincode=pin,landmark=land,adress=adrs,city=city,state=state,altphone=altphn)
            data.save()
            return redirect(userpro)
        elif req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            old_pass=req.POST['oldpass']
            new_pass=req.POST['newpass']
            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                messages.success(req,"Password changed successfully")
                return redirect(userpro)
            else:
                messages.warning(req,"Old password is incorrect")
                return redirect(change_pass)
        else:
            return render(req,'user/userprofile.html',{'data':user,'data1':data1})
    else:
        return render(req,'user/userprofile.html',{'data':user})

def change_pass(req):
    if 'user' in req.session:
        if req.method=='POST':
            user=User.objects.get(username=req.session['user'])
            old_pass=req.POST['oldpass']
            new_pass=req.POST['newpass']
            if user.check_password(old_pass):
                user.set_password(new_pass)
                user.save()
                messages.success(req,"Password changed successfully")
                return redirect(userpro)
            else:
                messages.warning(req,"Old password is incorrect")
                return redirect(change_pass)
        else:
            return render(req,'user/changepass.html')
    else:
        return redirect(bk_login)

def drama(req):
    data=Books.objects.filter(bk_genres='drama')[::-1]
    return render(req,'user/books/drama.html',{'data':data})

def love(req):
    data=Books.objects.filter(bk_genres='love')[::-1]
    return render(req,'user/books/love.html',{'data':data})

def fantacy(req):
    data=Books.objects.filter(bk_genres='fantasy')[::-1]
    return render(req,'user/books/fantacy.html',{'data':data})

def scifi(req):
    data=Books.objects.filter(bk_genres='sci-fi')[::-1]
    return render(req,'user/books/scifi.html',{'data':data})

def others(req):
    data=Books.objects.filter(bk_genres='others')[::-1]
    return render(req,'user/books/others.html',{'data':data})

def usedbk(req):
    if 'user1' in req.session:
        user1 = req.session['user1']
        data = Sbook.objects.exclude(user_id=user1).order_by('-id')
    else:
        data=Sbook.objects.all()[::-1]
    return render(req,'user/usedbook.html',{'data':data})

def addfav(req,bid):
    if 'user' in req.session:
        prod=Books.objects.get(pk=bid)
        user=User.objects.get(username=req.session['user'])
        data=Favorite.objects.create(user=user,product=prod)
        data.save()
        return redirect(viewfav)
    else:
        return redirect(bk_login)

def viewfav(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data=Favorite.objects.filter(user=user)
        return render(req,'user/favorite.html',{'fav':data})
    else:
        return redirect (bk_login) 
    
def delete_fav(req):
    fav=Favorite.objects.all()
    fav.delete()
    return redirect(viewfav)

def fav_to_cart(req):
    return redirect(viewcart)

def add_to_cart(req,pid):
    if 'user' in req.session:
        prod=Books.objects.get(pk=pid)
        user=User.objects.get(username=req.session['user'])
        data=Cart.objects.create(user=user,product=prod)
        data.save()
        return redirect(viewcart)
    else:
        return redirect(bk_login)

def viewcart(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        cart=Cart.objects.filter(user=user)
        return render(req,'user/cart.html',{'data':cart})
    else:
        return redirect (bk_login)

def delete_cart(req,id):
    cart=Cart.objects.get(pk=id)
    cart.delete()
    return redirect(viewcart)

def product_buy(req, id):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        saved_addresses = Userdtl.objects.filter(user=user)
        prod = None
        try:
            prod = Books.objects.get(pk=id)
        except Books.DoesNotExist:
            return redirect('home')

        if req.method == 'POST':
            if 'address_id' in req.POST:
                selected_address_id = req.POST['address_id']
                user_address = Userdtl.objects.get(id=selected_address_id)
            else:
                fullname = req.POST['fullname']
                address = req.POST['address']
                pincode = req.POST['pincode']
                city = req.POST['city']
                state = req.POST['state']
                phone = req.POST['phnum']
                altphone = req.POST['aphnum']
                landmark = req.POST['landmark']
                user_address = Userdtl.objects.create(
                    user=user,
                    phone=phone,
                    fullname=fullname,
                    city=city,
                    state=state,
                    altphone=altphone,
                    landmark=landmark,
                    adress=address,
                    pincode=pincode
                )
                user_address.save()

            if prod.stock > 0:
                purchase = Buys.objects.create(user=user, product=prod, address=user_address)
                purchase.save()
                prod.stock -= 1
                prod.save()
                return redirect(order_success)

        return render(req, 'user/buypage.html', {'prod': prod, 'saved_addresses': saved_addresses})
    else:
        return redirect(bk_login)
    
def order_success(req):
    return render(req, 'user/ordersuccess.html')

def view_odrs(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        buy=Buys.objects.filter(user=user)
        return render (req,'user/myoders.html',{'data':buy})
    else:
        return redirect(bk_login)
    
def cart_buy(req, id):
    user = User.objects.get(username=req.session['user'])
    cart = Cart.objects.filter(user=user)
    for i in cart:
        prod = i.product 
        if prod.stock > 0:
            data = Buys.objects.create(user=user, product=prod)
            data.save()
            prod.stock -= 1
            prod.save()
            i.delete()
            return redirect(product_buy)
        else:
            return render(req, 'user/cart.html', {'message': f'{prod.name} is out of stock!'})
    return render(req,'user/buypage.html')

def addrs(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        data1=Userdtl.objects.filter(user=user)

        if req.method == 'POST':
            user=User.objects.get(username=req.session['user'])
            name=req.POST['name']
            phn=req.POST['phn']
            altphn=req.POST['altphn']
            pin=req.POST['pin']
            land=req.POST['land']
            adrs=req.POST['adrs']
            city=req.POST['city']
            state=req.POST['state']
            data=Userdtl.objects.create(user=user,fullname=name,phone=phn,pincode=pin,landmark=land,adress=adrs,city=city,state=state,altphone=altphn)
            data.save()
            return redirect(addrs)
        else:
            return render(req,'user/adress.html',{'data1':data1})
    else:
        return render(req,"user/userprf.html")

def delete_address(req,pid):
    if 'user' in req.session:
        data=Userdtl.objects.get(pk=pid)
        data.delete()
        return redirect(userpro)
    else:
        return redirect(userpro)

def view_soldbooks(req):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        data = Sbook.objects.filter(user=user)
        return render(req, 'user/soldbk.html', {'data': data})
    else:
        return redirect(bk_login)
    
def cancel_order(req, id):
    if 'user' in req.session:
        order = Buys.objects.get(pk=id)
        order.delete()
        return redirect(view_odrs)
    else:
        return redirect(bk_login)
    
def view_booking_details(req,id):
    if 'user' in req.session:
        user = User.objects.get(username=req.session['user'])
        bookings =  Buys.objects.filter(user=user)
        return render(req, 'user/viewbookingdetails.html', {'bookings': bookings})
    else:
        return redirect(bk_login)

# ------------------------Footer------------------------------

def about(req):
    return render(req,'footer/about.html')

def faq(req):
    return render(req,'footer/faq.html')

def services(req):
    return render(req,'footer/our_services.html')

def privacy(req):
    return render(req,'footer/privacy.html')
