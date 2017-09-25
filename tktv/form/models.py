from django.db import models

# Create your models here.
from tktv.main.models import SubMenu


class Form(models.Model):
    submenu = models.ForeignKey(SubMenu)
    name = models.TextField()
    title = models.TextField()
    type = models.TextField(default='text')

    def __str__(self):
        return '%s, %s, %s' %(self.submenu,self.name,self.title)


class FormData(models.Model):
    form = models.ForeignKey(Form)
    value = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)


class FormImage(models.Model):
    form = models.ForeignKey(Form)
    src = models.FileField(upload_to="upload/")