from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import *
from django.core.mail import send_mail
from .models import *
import random

# Create your views here.

def bk_login(req):
    if 'user' in req.session:
        return redirect(userpro)
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
            try:
                data=User.objects.create_user(first_name=name,email=email,password=password,username=email)
                data.save()
                return redirect(bk_login)
               
            except:
                if User.objects.filter(email=email).exists():
                    messages.warning(req,"email already exists enter a new email id")
                    return render(req,'user/register.html')
        else:
            messages.warning(req,"Password Missmatch")
            return render(req,'user/register.html')
    else:
        return render(req,'register.html')
    
# ------------------------ADMIN---------------------

def adhome(req):
    return render(req,'admin/admin.html')
    

# -----------------------User-------------------------


def bk_home(req):
    data=Books.objects.filter(bk_genres='drama')[::-1][:4]
    data1=Books.objects.filter(bk_genres='sci-fi')[::-1][:4]
    data2=Books.objects.filter(bk_genres='love')[::-1][:4]
    data3=Books.objects.filter(bk_genres='fantasy')[::-1][:4]
    return render(req,'user/home.html',{'data':data,'data1':data1,'data2':data2,'data3':data3})

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

def userpro(req):
    return render(req,'user/userprofile.html')