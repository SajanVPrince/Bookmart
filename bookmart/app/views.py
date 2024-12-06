from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import *

# Create your views here.
def bk_login(req):
    if 'book' in req.session:
        return redirect(bk_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['book']=uname   
                return redirect(ad_home)
            else:
                login(req,data)
                req.session['user']=uname
                return redirect(bk_home)
        else:
            messages.warning(req,"please check your username or password")
            return render(req,'login.html')
    
    else:
        return render(req,'login.html')

def bk_logout(req):
    req.session.flush()          
    logout(req)
    return redirect(bk_login)

def register(req):
    return render(req,'register.html')

# -----------------------User-------------------------


def bk_home(req):
    data=Books.objects.filter(bk_genres='drama')
    data1=Books.objects.filter(bk_genres='sci-fi')
    data2=Books.objects.filter(bk_genres='love')
    data3=Books.objects.filter(bk_genres='fantasy')
    return render(req,'user/home.html',{'data':data,'data1':data1,'data2':data2,'data3':data3})

def sell(req):
    return render(req,'user/sell.html')