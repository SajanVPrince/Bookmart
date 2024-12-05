from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


# Create your views here.
def bk_login(req):
    if 'eshop' in req.session:
        return redirect(bk_home)
    if req.method=='POST':
        uname=req.POST['uname']
        password=req.POST['pswd']
        data=authenticate(username=uname,password=password)
        if data:
            if data.is_superuser:
                login(req,data)
                req.session['eshop']=uname   
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

# -----------------------User-------------------------


def bk_home(req):
    return render(req,'user/home.html')