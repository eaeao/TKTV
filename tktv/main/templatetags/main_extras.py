from django import template
from django.utils.datetime_safe import datetime, time

from tktv.board.models import Board

register = template.Library()

@register.filter
def get_board(value):
    return Board.objects.filter(submenu__main_menu=value,submenu__permission_read=1).order_by("-id")


@register.filter
def mod(num, val):
    return num % val


@register.filter
def time2unix(date):
    return int(time.mktime(date.timetuple()))


@register.filter
def replace_bold(con="", value=""):
    return con.replace(value, "<b class='search_key'>%s</b>"%value)