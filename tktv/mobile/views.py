from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from tktv.board.models import Board, BoardImg
from tktv.form.models import Form, FormData, FormImage
from tktv.main.models import getMain, get_or_none, SubMenu, encode_con, UserProfile
from tktv.page.models import Page


def main(request):
    context = {
        'user': request.user,
        'getMain':getMain(),
        'appname':'main'
    }
    return render(request, 'mobile/main.html', context)


def recent(request):
    recentlist = Board.objects.filter(submenu__main_menu__id=2).order_by("-id")[:10]
    context = {
        'user': request.user,
        'getMain': getMain(),
        'recentlist':recentlist,
        'appname': 'recent'
    }
    return render(request, 'mobile/recent.html', context)


def board(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        page = int(request.GET.get('page',1))
        list = Board.objects.filter(submenu=submenu).order_by("-date_updated")
        list = Paginator(list,15)
        headlines = Board.objects.filter(submenu=submenu, is_headline=True).order_by("-date_updated")
        context = {
            'submenu':submenu,
            'list':list.page(page),
            'headlines':headlines,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_mobile'
        }
        return render(request, 'mobile/board_mobile.html', context)
    return HttpResponseRedirect('/mobile/')


def board_write(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if request.POST.get("input_title") :
        input_title = request.POST.get("input_title")
        input_con = request.POST.get("input_con")
        input_headline = int(request.POST.get("input_headline",0))
        board = Board.objects.create(submenu=submenu,user=request.user,title=input_title,con=input_con,is_headline=input_headline)
        if board :
            for img_file in request.FILES.getlist('input_file'):
                board_img = BoardImg.objects.create(board=board,src="",is_visible=True)
                board_img.src.save(img_file.name, ContentFile(img_file.read()))
            return HttpResponseRedirect("/mobile/board/detail/%d"%(board.id))
    if submenu :
        recent_board = Board.objects.all()[0]
        boards_list = SubMenu.objects.filter(mode__in=[2, 3, 4], permission_write__lte=request.user.profile.grade)
        context = {
            'submenu': submenu,
            'user': request.user,
            'boards_list':boards_list,
            'recent_board': recent_board,
            'getMain': getMain(),
            'appname': 'board_write'
        }
        return render(request, 'mobile/board_write.html', context)
    return HttpResponseRedirect('/mobile/')


def board_detail(request, board_id=None):
    board = get_or_none(Board,id=board_id)
    if board :
        boardimg = BoardImg.objects.filter(board=board)
        contents = encode_con(board.con)
        for i in range(0,len(boardimg)) :
            contents = contents.replace("{{%d}}"%i, "<a href='%s' target='_blank'><img src='%s' class='img_board_src'></a>"%(boardimg[i].src.url,boardimg[i].src.url))
        if not request.user.is_superuser:
            board.hits = board.hits + 1
            board.save()
        context = {
            'submenu':board.submenu,
            'board':board,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_detail'
        }
        return render(request, 'mobile/board_detail.html', context)
    return HttpResponseRedirect('/mobile/')


def board_modify(request, board_id=None):
    board = get_or_none(Board,id=board_id)
    if request.POST.get("input_title") :
        input_title = request.POST.get("input_title")
        input_con = request.POST.get("input_con")
        input_headline = int(request.POST.get("input_headline",0))
        board.title = input_title
        board.con = input_con
        board.is_headline = input_headline
        board.save()
        if board :
            for img_file in request.FILES.getlist('input_file'):
                board_img = BoardImg.objects.create(board=board,src="",is_visible=True)
                board_img.src.save(img_file.name, ContentFile(img_file.read()))
            return HttpResponseRedirect("/mobile/board/detail/%d"%(board.id))
    if board :
        contents = encode_con(board.con)
        boardimg = BoardImg.objects.filter(board=board)
        context = {
            'board':board,
            'submenu':board.submenu,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_write'
        }
        return render(request, 'mobile/board_write.html', context)
    return HttpResponseRedirect('/mobile/')


def page(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    contents = "생성된 페이지가 없습니다."
    if submenu :
        page = get_or_none(Page, submenu=submenu)
        if page :
            contents = page.con

        context = {
            'submenu':submenu,
            'page':page,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'page'
        }
        return render(request, 'mobile/page.html', context)
    return HttpResponseRedirect('/mobile/')


def form(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        forms = Form.objects.filter(submenu=submenu)
        if request.POST.get("csrfmiddlewaretoken") :
            for form in forms :
                if request.FILES.getlist(form.name) :
                    form_data = FormData.objects.create(form=form, value="")
                    for img_file in request.FILES.getlist(form.name):
                        form_img = FormImage.objects.create(form=form,src='')
                        form_img.src.save(img_file.name, ContentFile(img_file.read()))
                        form_data.value = form_img.src.url
                        form_data.save()
                else :
                    value=request.POST.get(form.name,"")
                    FormData.objects.create(form=form,value=value)
            context = {
                'submenu':submenu,
                'user': request.user,
                'getMain':getMain(),
                'appname':'form'
            }
            return render(request, 'mobile/form_success.html', context)
        else :
            if forms :
                context = {
                    'submenu':submenu,
                    'forms':forms,
                    'user': request.user,
                    'getMain': getMain(),
                    'appname': 'form'
                }
                return render(request, 'mobile/form.html', context)
            return HttpResponseRedirect('/mobile/')


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
    return HttpResponseRedirect('/mobile/')

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
            return HttpResponseRedirect('/mobile/')
    return HttpResponseRedirect('/mobile/')

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