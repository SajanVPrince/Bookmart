from django.urls import path
from . import views

urlpatterns = [
    path('login',views.bk_login),
    path('logout',views.bk_logout),

    # --------------User------------

    path('',views.bk_home),


]