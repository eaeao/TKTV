# -*- coding: utf-8 -*-
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render

# Create your views here.
from tktv.board.models import Board
from tktv.main.models import getMain, get_or_none, MainMenu, SubMenu, UserProfile


def main(request):
    headline = Board.objects.filter(is_headline=True).order_by("-id")
    hotlist = Board.objects.all().order_by("-hits")[:10]

    notices = Board.objects.filter(submenu=26).order_by("-date_updated")

    subimg = []
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=2),"color":"#f39c12"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=3),"color":"#27ae60"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=5),"color":"#2980b9"})
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
    come_from = request.POST.get("come_from")
    user = authenticate(username=userid, password=password)
    if user :
        login(request, user)
        request.session.set_expiry(31536000)
        return HttpResponseRedirect(come_from)
    return HttpResponseRedirect(come_from)

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def user_join(request):
    user_id = request.POST.get("user_id")
    password = request.POST.get("password")
    user_name = request.POST.get("user_name")
    user_email = request.POST.get("user_email")
    user_phone = request.POST.get("user_phone")
    user = User.objects.create_user(username=user_id,password=password,email=user_email,first_name=user_name)
    if user :
        UserProfile.objects.create(user=user,phone_number=user_phone)
        user = authenticate(username=user_id, password=password)
        if user :
            login(request, user)
            request.session.set_expiry(31536000)
            return HttpResponseRedirect('/')
    return HttpResponseRedirect('/')

def user_join_get(request):
    userid = request.POST.get("userid")
    email = request.POST.get("email")
    if userid :
        query = User.objects.filter(username=userid)
        if query :
            return HttpResponse(0);
    elif email :
        query = User.objects.filter(email=email)
        if query :
            return HttpResponse(0);
    return HttpResponse(1);