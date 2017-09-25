from django.contrib.auth.models import User
from django.db import models

from bs4 import BeautifulSoup

# Create your models here.
from django.template.defaultfilters import safe
from django.utils.html import strip_tags

from tktv.main.models import SubMenu, encode_con


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
            return src.first()
        else :
            soup = BeautifulSoup(encode_con(self.con), "html.parser")
            img = soup.find('img')
            if img :
                src_url = soup.find('img')['src'].replace("http://tktv.co.kr/news/upload/", "/media/oldboard/")
                return {'is_visible':True, 'src':{'url':src_url}}
        return None

    @property
    def get_con(self):
        con = strip_tags(safe(encode_con(self.con)))
        for i in range(0,10) :
            con = con.replace("{{%d}}"%i, "")
        return con

    def __str__(self):
        return '[%d] (%s)%s' %(self.id,self.submenu,self.title)

class BoardImg(models.Model):
    board = models.ForeignKey(Board)
    src = models.FileField(upload_to="upload/")
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return '%s' %(self.src)

class BoardReply(models.Model):
    board = models.ForeignKey(Board)
    user = models.ForeignKey(User)
    con = models.TextField(max_length=200)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%d] (%s)%s:%s' %(self.id,self.board,self.user,self.con)