# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render

# Create your views here.
from tktv.board.models import Board
from tktv.main.models import getMain, get_or_none, MainMenu, SubMenu


def main(request):
    headline = Board.objects.filter(is_headline=True).order_by("-id")
    hotlist = Board.objects.all().order_by("-hits")[:10]

    notices = Board.objects.filter(submenu=1).order_by("-id")

    subimg = []
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=2,is_headline=True),"color":"#f39c12"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=3,is_headline=True),"color":"#27ae60"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=5,is_headline=True),"color":"#2980b9"})
    context = {
        'headline':headline,
        'hotlist':hotlist,
        'subimg':subimg,
        'notices':notices,
        'getMain':getMain(),
        'user': request.user,
        'appname':'main'
    }
    return render(request, 'main.html', context)

def user(request):
    return HttpResponse("%s"%request.user.first_name)

def user_login(request):
    userid = request.POST.get("user_id")
    password = request.POST.get("password")
    user = authenticate(username=userid, password=password)
    if user :
        login(request, user)
        request.session.set_expiry(31536000)
        return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')