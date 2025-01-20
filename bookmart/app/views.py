from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import *
from django.core.mail import send_mail
from .models import *

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
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        password1=req.POST['password1']
        if password==password1:
            data=User.objects.create_user(first_name=name,email=email,password=password1,username=email)
            data.save()
            return render(req,'login.html')
        else:
            messages.warning(req,"Password Missmatch")
            return render(req,'user/register.html')
    else:
        return render(req,'register.html')
    
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
        return redirect(addbook)
    else:
        return render(req,'admin/admin.html')
    

def addbook(req):
    if 'shop' in req.session:
        if req.method=='POST':
            name=req.POST['name']
            ath_name=req.POST['ath_name']
            price=req.POST['price']
            bk_genres=req.POST['bk_genres']
            img=req.FILES['img']
            dis=req.POST['dis']
            stock=req.POST['stock']
            data=Books.objects.create(name=name,ath_name=ath_name,price=price,bk_genres=bk_genres,img=img,dis=dis,stock=stock)
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
        data=Buy.objects.all()
        return render(req,'admin/buy.html',{'data':data})
    else:
        return redirect(bk_login)
    
def delete_buy(req,id):
    buy=Buy.objects.get(pk=id)
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
    user=User.objects.get(username=req.session['user'])
    return render(req,'user/userprofile.html',{'data':user})

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

def product_buy(req,id):
    if 'user' in req.session:
        if req.method=='POST':
            fullname=req.POST['fullname']
            adress=req.POST['address']
            pincode=req.POST['pincode']
            city=req.POST['city']
            state=req.POST['state']
            phone=req.POST['phnum']
            altphone=req.POST['aphnum']
            landmark=req.POST['landmark']
            user=User.objects.get(username=req.session['user'])
            data=Userdtl.objects.create(user=user,phone=phone,fullname=fullname,city=city,state=state,altphone=altphone,landmark=landmark,adress=adress,pincode=pincode)
            data.save()
        try:
            prod = Books.objects.get(pk=id)
            if prod.stock > 0: 
                user = User.objects.get(username=req.session['user'])
                data = Buy.objects.create(user=user, product=prod)
                data.save()
                prod.stock -= 1
                prod.save()
                return render(req, 'user/buypage.html',)
            else:
                return render(req, 'user/buypage.html',{'prod':prod})
        except Books.DoesNotExist:
            return render(req, 'user/buypage.html',)
    else:
        return redirect(bk_login)

def view_odrs(req):
    if 'user' in req.session:
        user=User.objects.get(username=req.session['user'])
        buy=Buy.objects.filter(user=user)
        return render (req,'user/myoders.html',{'data':buy})
    else:
        return redirect(bk_login)
    
def cart_buy(req, id):
    user = User.objects.get(username=req.session['user'])
    cart = Cart.objects.filter(user=user)
    for i in cart:
        prod = i.product 
        if prod.stock > 0:
            data = Buy.objects.create(user=user, product=prod)
            data.save()
            prod.stock -= 1
            prod.save()
            i.delete()
        else:
            return render(req, 'user/cart.html', {'message': f'{prod.name} is out of stock!'})
    return render(req,'user/buypage.html')

# ------------------------Footer------------------------------

def about(req):
    return render(req,'footer/about.html')

def faq(req):
    return render(req,'footer/faq.html')

def services(req):
    return render(req,'footer/our_services.html')

def privacy(req):
    return render(req,'footer/privacy.html')

