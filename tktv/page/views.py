# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from tktv.main.models import SubMenu, get_or_none, getMain
from tktv.page.models import Page, PageImg


def page(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    contents = "생성된 페이지가 없습니다."
    if submenu :
        page = get_or_none(Page,submenu=submenu)
        if page :
            pageimg = PageImg.objects.filter(page=page)
            contents = page.con

            for i in range(0,len(pageimg)) :
                contents = contents.replace("{{%d}}"%i, "<img src='%s' class='img_page_src'>"%(pageimg[i].src.url))

        context = {
            'submenu':submenu,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'page'
        }
        return render(request, 'page.html', context)
    return HttpResponseRedirect('/')