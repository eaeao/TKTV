# -*- coding: utf-8 -*-

from django.shortcuts import render

# Create your views here.
from tktv.board.models import Board
from tktv.main.models import getMain, get_or_none


def main(request):

    headline = Board.objects.filter(is_headline=True).order_by("-id")
    hotlist = Board.objects.all().order_by("hits")[:10]

    subimg = []
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=2,is_headline=True),"color":"#f39c12"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=3,is_headline=True),"color":"#27ae60"})
    subimg.append({"ele":get_or_none(Board,order="-",submenu__main_menu__order=5,is_headline=True),"color":"#2980b9"})

    context = {
        'headline':headline,
        'hotlist':hotlist,
        'subimg':subimg,
        'getMain':getMain(),
        'user': request.user,
        'appname':'main'
    }
    return render(request, 'main.html', context)