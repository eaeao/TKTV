# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from tktv.main.models import SubMenu

class Form(models.Model):
    submenu = models.ForeignKey(SubMenu)
    name = models.TextField()
    title = models.TextField()
    type = models.TextField(default='text')

    def __unicode__(self):
        return u'%s, %s, %s' %(self.submenu,self.name,self.title)

class FormData(models.Model):
    user = models.ForeignKey(User)
    form = models.ForeignKey(Form)
    value = models.TextField()