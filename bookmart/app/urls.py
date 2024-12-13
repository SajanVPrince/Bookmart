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
    path('sviewprod/<id>',views.sview_prod),
    path('userpro',views.userpro),
    path('dramabk',views.drama),
    path('lovebk',views.love),
    path('fantacybk',views.fantacy),
    path('scifibk',views.scifi),
    path('otherbk',views.others),
    path('usedbk',views.usedbk),
    path('favbk/<bid>',views.addfav),
    path('viewfav',views.viewfav),
    path('viewcart',views.viewcart),











]