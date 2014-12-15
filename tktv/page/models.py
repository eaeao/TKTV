# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from tktv.main.models import SubMenu


class Page(models.Model):
    submenu = models.ForeignKey(SubMenu, unique=True)
    con = models.TextField()
    date_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.submenu)

class PageImg(models.Model):
    page = models.ForeignKey(Page)
    src = models.FileField(upload_to="upload/")

    def __unicode__(self):
        return u'%s' %(self.src)