# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from tktv.board.models import Board, BoardImg
from tktv.main.models import SubMenu, get_or_none, getMain


def board(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        list = Board.objects.filter(submenu=submenu).order_by("-id")
        context = {
            'submenu':submenu,
            'list':list,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board'
        }
        return render(request, 'board.html', context)
    return HttpResponseRedirect('/')

def board_detailed(request, board_id=None):
    board = get_or_none(Board,id=board_id)
    if board :
        boardimg = BoardImg.objects.filter(board=board)
        contents = board.con
        for i in range(0,len(boardimg)) :
            contents = contents.replace("{{%d}}"%i, "<img src='%s' class='img_board_src'>"%(boardimg[i].src.url))
        context = {
            'submenu':board.submenu,
            'board':board,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_detailed'
        }
        return render(request, 'board_detailed.html', context)
    return HttpResponseRedirect('/')