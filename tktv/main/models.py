# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.core.exceptions import MultipleObjectsReturned
from django.db import models

# Create your models here.
class UserGrade(models.Model):
    grade = models.TextField()
    level = models.IntegerField(unique=True)

    def __unicode__(self):
        return u'[%d] %s' %(self.id,self.grade)

class UserProfile(models.Model):
    #required by the auth model
    user = models.ForeignKey(User, unique=True)
    src = models.FileField(upload_to="upload/",default="/static/img/main/default_user.png")
    grade = models.ForeignKey(UserGrade, default=1)
    phone_number = models.TextField()

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
        right_banner = RightBanner.objects.filter(main=self)
        return {'top_logo':top_logo,'top_banner_left':top_banner_left,'top_banner_right':top_banner_right,'side_banner_left':side_banner_left,'side_banner_right':side_banner_right,'right_banner':right_banner}

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

class RightBanner(models.Model):
    main = models.ForeignKey(Main)
    src = models.FileField(upload_to="upload/")
    url = models.TextField(default='/',null=True,blank=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class MainMenu(models.Model):
    name = models.TextField()
    order = models.IntegerField(unique=True)
    url = models.TextField(null=True,blank=True)

    def get_link(self):
        if self.url :
            return self.url
        else :
            sub = SubMenu.objects.filter(main_menu=self).order_by("order")
            if sub :
                return sub[0].get_link()
            return "/"

    def get_submenu(self):
        return SubMenu.objects.filter(main_menu=self).order_by("order")

    def __unicode__(self):
        return u'%s(%d)' %(self.name,self.order)

MODE_IN_SUBMENU_CHOICES = (
    (0, '외부링크'),
    (1, '페이지'),
    (2, '일반 게시판'),
    (3, '웹진'),
    (4, '갤러리'),
)

class SubMenu(models.Model):
    main_menu = models.ForeignKey(MainMenu)
    name = models.TextField()
    order = models.IntegerField()
    mode = models.IntegerField(default=0,choices=MODE_IN_SUBMENU_CHOICES)
    url = models.TextField(null=True,blank=True)
    permission_read = models.ForeignKey(UserGrade, default=1, related_name="note_permission_read_grade")
    permission_write = models.ForeignKey(UserGrade, default=1, related_name="note_permission_write_grade")

    def get_link(self):
        if self.mode == 0 :
            return self.url
        elif self.mode == 1 :
            return "/page/%d"%self.id
        elif self.mode == 2 :
            return "/board/%d"%self.id
        elif self.mode == 3 :
            return "/board/%d"%self.id
        elif self.mode == 4 :
            return "/board/%d"%self.id

    def __unicode__(self):
        return u'%s → %s(%d)' %(self.main_menu,self.name,self.order)

def get_or_none(model,order=None, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except MultipleObjectsReturned as e:
        if order == "-":
            res = model.objects.filter(**kwargs).order_by("-id")
        else :
            res = model.objects.filter(**kwargs).order_by("id")
        if res:
            return res[0]
        return None
    except Exception as e:
        return None

def getMain():
    mainImg = Main.objects.all().order_by("-id")
    if mainImg :
        mainImg = mainImg[0]

    main_menu = MainMenu.objects.all()

    return {'mainImg':mainImg,'main_menu':main_menu}