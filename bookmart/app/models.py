from django.db import models
from django.contrib.auth.models import *

# Create your models here.
class Books(models.Model):
    bk_id=models.TextField()
    name=models.TextField()
    ath_name=models.TextField()
    bk_genres=models.TextField()
    price=models.IntegerField()
    ofr_price=models.IntegerField()
    img=models.FileField()
    dis=models.TextField()

class Userdtl(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    phone=models.IntegerField()
    adress=models.TextField()
    pincode=models.IntegerField()

class Sbook(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    sname=models.TextField()
    sath_name=models.TextField()
    sbk_genres=models.TextField()
    sprice=models.IntegerField()
    simg=models.FileField()
    sdis=models.TextField()

    


