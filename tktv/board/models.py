# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.db import models
from tktv.main.models import SubMenu

# Create your models here.

class Board(models.Model):
    submenu = models.ForeignKey(SubMenu)
    user = models.ForeignKey(User)
    title = models.TextField()
    con = models.TextField()
    hits = models.IntegerField(default=0)
    is_headline = models.BooleanField(default=False)
    date_updated = models.DateTimeField(auto_now_add=True)

    def get_src(self):
        src = BoardImg.objects.filter(board=self)
        if src :
            return src[0]
        return None

    def get_con(self):
        con = self.con
        for i in range(0,10) :
            con = con.replace("{{%d}}"%i, "")
        if con.__len__() > 230 :
            con = "%s..."%con[:230]
        return con

    def __unicode__(self):
        return u'[%d] (%s)%s' %(self.id,self.submenu,self.title)

class BoardImg(models.Model):
    board = models.ForeignKey(Board)
    src = models.FileField(upload_to="upload/")
    is_visible = models.BooleanField(default=True)

    def __unicode__(self):
        return u'%s' %(self.src)

class BoardReply(models.Model):
    board = models.ForeignKey(Board)
    user = models.ForeignKey(User)
    con = models.TextField(max_length=200)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%d] (%s)%s:%s' %(self.id,self.board,self.user,self.con)