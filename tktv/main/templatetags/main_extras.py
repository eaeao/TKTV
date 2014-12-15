# -*- coding: utf-8 -*-
from django import template

from tktv.board.models import Board
from tktv.main.models import SubMenu

register = template.Library()

@register.filter
def get_board(value):
    return Board.objects.filter(submenu__main_menu=value).order_by("-id")