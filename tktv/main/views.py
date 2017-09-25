from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator, Page
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tktv.board.models import Board
from tktv.main.models import getMain, UserProfile


def main(request):
    headline = Board.objects.filter(is_headline=True).order_by("-date_updated")
    hotlist = []
    for board in Board.objects.all().order_by("-hits")[0:10]:
        hotlist.append(board)

    recentlist = Board.objects.filter(submenu__main_menu__id=2).order_by("-id")[:10]

    notices = Board.objects.filter(submenu=26,is_headline=True).order_by("-date_updated")

    subimg = []
    subimg.append({"ele":Board.objects.filter(submenu__main_menu__id=2).order_by("-date_updated").first(),"color":"#f39c12"})
    subimg.append({"ele":Board.objects.filter(submenu__main_menu__id=3).order_by("-date_updated").first(),"color":"#27ae60"})
    subimg.append({"ele":Board.objects.filter(submenu__main_menu__id=4).order_by("-date_updated").first(),"color":"#2980b9"})
    context = {
        'headline':headline,
        'hotlist':hotlist,
        'recentlist':recentlist,
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


def search_board(request):
    query = request.GET.get("query","")
    page = int(request.GET.get('page', 1))

    list = Board.objects.filter(Q(title__icontains=query)|Q(con__icontains=query))
    list = Paginator(list, 10)

    context = {
        'query':query,
        'list': list.page(page),
        'getMain': getMain(),
        'user': request.user,
        'appname': 'search'
    }
    return render(request, 'search_board.html', context)


def search_page(request):
    query = request.GET.get("query","")
    page = int(request.GET.get('page', 1))

    list = Page.objects.filter(con__icontains=query)
    list = Paginator(list, 10)

    context = {
        'query':query,
        'list': list.page(page),
        'getMain': getMain(),
        'user': request.user,
        'appname': 'search'
    }
    return render(request, 'search_page.html', context)