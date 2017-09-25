from django.db import models

# Create your models here.
from tktv.main.models import SubMenu


class Page(models.Model):
    submenu = models.ForeignKey(SubMenu, unique=True)
    con = models.TextField()
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u'[%d] %s' %(self.id,self.submenu)