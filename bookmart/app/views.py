from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def blogin(req):
    return render(req,'login.html')