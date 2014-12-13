from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class UserGrade(models.Model):
    grade = models.TextField()

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.grade)

class UserProfile(models.Model):
    #required by the auth model
    user = models.ForeignKey(User, unique=True)
    src = models.FileField(upload_to="upload/")
    grade = models.ForeignKey(UserGrade, default=1)

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.user.first_name)

class Main(models.Model):
    title = models.TextField()

    def get_img(self):
        top_logo = get_or_none(TopLogo,main=self)
        top_banner_left = get_or_none(TopBannerLeft,main=self)
        top_banner_right = get_or_none(TopBannerRight,main=self)
        side_banner_left = get_or_none(SideBannerLeft,main=self)
        side_banner_right = get_or_none(SideBannerRight,main=self)
        return {'top_logo':top_logo,'top_banner_left':top_banner_left,'top_banner_right':top_banner_right,'side_banner_left':side_banner_left,'side_banner_right':side_banner_right}

    def __unicode__(self):
        return u'[%d]%s' %(self.id,self.title)

class TopLogo(models.Model):
    main = models.ForeignKey(Main, unique=True)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class TopBannerLeft(models.Model):
    main = models.ForeignKey(Main, unique=True)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class TopBannerRight(models.Model):
    main = models.ForeignKey(Main, unique=True)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class SideBannerLeft(models.Model):
    main = models.ForeignKey(Main, unique=True)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class SideBannerRight(models.Model):
    main = models.ForeignKey(Main, unique=True)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class MainMenu(models.Model):
    name = models.TextField()
    order = models.IntegerField(unique=True)
    url = models.TextField(null=True,blank=True)

    def get_submenu(self):
        return SubMenu.objects.filter(main_menu=self)

    def __unicode__(self):
        return u'%s(%d)' %(self.name,self.order)

class SubMenu(models.Model):
    main_menu = models.ForeignKey(MainMenu)
    name = models.TextField()
    order = models.IntegerField(unique=True)
    url = models.TextField(null=True,blank=True)

    def __unicode__(self):
        return u'%s >> %s(%d)' %(self.main_menu,self.name,self.order)

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except Exception as e:
        return None