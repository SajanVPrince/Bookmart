from django.db import models

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