from django.urls import path
from . import views

urlpatterns = [
    path('login',views.bk_login),
    path('logout',views.bk_logout),
    path('register',views.register),
    # path('verifyotp',views.verify_otp),

    # -------------Admin------------

    path('adhome',views.adhome),




    # --------------User------------

    path('',views.bk_home),
    path('home',views.bk_home),
    path('sell',views.sell),
    path('viewprod/<id>',views.view_prod),
    path('userpro',views.userpro),





]