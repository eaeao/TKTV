from django.db import models

# Create your models here.
class Shop(models.Model):
    sid = models.TextField()
    password = models.TextField()
    name = models.TextField()
    alimi_url = models.TextField(null=True,blank=True)
    event_url = models.TextField(null=True,blank=True)

OS_IN_DEVICE_CHOICES = (
    (0, '안드로이드'),
    (1, '아이폰')
)

class ShopDevice(models.Model):
    sid = models.TextField()
    uid = models.TextField()
    os = models.IntegerField(default=0,choices=OS_IN_DEVICE_CHOICES)
    is_admin = models.BooleanField(default=0)