from django.urls import path
from . import views

urlpatterns = [
    path('login',views.bk_login, name='login'),
    path('logout',views.bk_logout , name='logout'),
    path('register',views.register , name='register'),
    path('verifyotp',views.verify_otp, name='verify_otp'),
    path('resend',views.resend_otp, name='resend_otp'),
    path('forget',views.forgetpassword , name='forgetpassword'),
    path('reset',views.resetpassword , name='resetpassword'),
    path('verify_otp_reg',views.verify_otp_reg, name='verify_otp_reg'),
    path('resend_otp_reg',views.resend_otp_reg, name='resend_otp_reg'),

    # -------------Admin------------

    path('adminpro',views.adminpro),
    path('adhome',views.adhome),
    path('addbook',views.addbook),
    path('viewbook',views.viewbook),
    path('editbook/<id>',views.edit_book),
    path('deletebook/<id>',views.delete_book),
    path('viewuser',views.view_user),
    path('deleteuser/<id>',views.delete_user),
    path('viewbuy',views.view_buy),
    path('viewsbook',views.view_sbook),
    path('deletesbook/<id>',views.delete_sbook),
    path('deletebuy/<id>',views.delete_buy),
    path('viewreview',views.view_review),
    path('deletereview/<id>',views.delete_review),




    # --------------User------------

    path('',views.bk_home),
    path('home',views.bk_home),
    path('sell',views.sell),
    path('viewprod/<id>',views.view_prod),
    path('sviewprod/<id>',views.sview_prod),
    path('userpro',views.userpro ,name='userpro'),
    path('change_pass',views.change_pass),
    path('dramabk',views.drama),
    path('lovebk',views.love),
    path('fantacybk',views.fantacy),
    path('scifibk',views.scifi),
    path('othersbk',views.others),
    path('usedbk',views.usedbk),
    path('favbk/<bid>',views.addfav),
    path('viewfav',views.viewfav),
    path('deletefav',views.delete_fav),
    path('fav_to_cart',views.fav_to_cart),
    path('add_to_cart/<pid>',views.add_to_cart),
    path('viewcart',views.viewcart),
    path('product_buy/<id>',views.product_buy),
    path('delete_cart/<id>',views.delete_cart),
    path('cart_buy/<id>',views.cart_buy),
    path('search',views.search),
    path('viewoders',views.view_odrs),
    path('manageadd',views.addrs),
    path('delete_address/<pid>',views.delete_address),
    path('soldbooks',views.view_soldbooks),
    path('ordersucces',views.order_success , name='order_success'),
    path('cancel_oder/<id>',views.cancel_order),
    path('view_details/<id>',views.view_booking_details),


# ----------------Footer------------------

    path('about',views.about),
    path('faq',views.faq),
    path('service',views.services),
    path('privacy',views.privacy),





]