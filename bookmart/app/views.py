from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import *
from django.core.mail import send_mail
from .models import *
import random

# Create your views here.
def generate_otp():
    return str(random.randint(100000, 999999))

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

def send_otp_email(email, otp):
    subject = "Your OTP for Registration"
    message = f"Your OTP code is {otp}. It is valid for the next 10 minutes."
    from_email = "bookmarta64@gmail.com" 
    send_mail(subject, message, from_email, [email])

def register(req):
    if req.method=='POST':
        name=req.POST['name']
        email=req.POST['email']
        password=req.POST['password']
        password1=req.POST['password1']
        if password==password1:
            try:
                otp = generate_otp()
                send_otp_email(email, otp)
                req.session['otp'] = otp
                req.session['userdata'] = {
                    'name': name,
                    'email': email,
                    'password': password
                }
                messages.info(req, "An OTP has been sent to your email. Please verify to complete registration.")
                return redirect('verify_otp')
            except:
                if User.objects.filter(email=email).exists():
                    messages.warning(req,"email already exists enter a new email id")
                    return render(req,'user/register.html')
        else:
            messages.warning(req,"Password Missmatch")
            return render(req,'user/register.html')
    else:
        return render(req,'register.html')
    
def verify_otp(req):
    if req.method == 'POST':
        entered_otp = req.POST['otp']
        session_otp = req.session.get('otp')
        userdata = req.session.get('us')
        if entered_otp and session_otp and entered_otp == session_otp:
            try:
                User.objects.create_user(
                    first_name=userdata['name'],
                    email=userdata['email'],
                    password=userdata['password'],
                    username=userdata['email']
                )
                req.session.pop('userdata', None)
                req.session.pop('otp', None)
                messages.success(req, "Registration successful! You can now log in.")
                return redirect('bk_login')
            except:
                pass
        else:
            messages.warning(req, "Invalid OTP. Please try again.")
            return redirect('verify_otp')
    else:
        return render(req,'verify_otp.html')



# -----------------------User-------------------------


def bk_home(req):
    data=Books.objects.filter(bk_genres='drama')
    data1=Books.objects.filter(bk_genres='sci-fi')
    data2=Books.objects.filter(bk_genres='love')
    data3=Books.objects.filter(bk_genres='fantasy')
    return render(req,'user/home.html',{'data':data,'data1':data1,'data2':data2,'data3':data3})

def sell(req):
    return render(req,'user/sell.html')