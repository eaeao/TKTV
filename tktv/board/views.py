from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from tktv.board.models import Board, BoardImg, BoardReply
from tktv.main.models import get_or_none, SubMenu, getMain, encode_con


def board(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        page = int(request.GET.get('page',1))
        list = Board.objects.filter(submenu=submenu).order_by("-date_updated")
        page_count = 10
        if submenu.mode == 2:
            page_count = 15
        list = Paginator(list,page_count)
        headlines = Board.objects.filter(submenu=submenu, is_headline=True).order_by("-date_updated")
        context = {
            'submenu':submenu,
            'list':list.page(page),
            'headlines':headlines,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_%d'%(submenu.mode)
        }
        return render(request, 'board_%d.html'%(submenu.mode), context)
    return HttpResponseRedirect('/')


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
            return HttpResponseRedirect("/board/detail/%d"%(board.id))
    if submenu :
        recent_board = Board.objects.all()[0]
        context = {
            'submenu':submenu,
            'user': request.user,
            'recent_board':recent_board,
            'getMain':getMain(),
            'appname':'board_write'
        }
        return render(request, 'board_write.html', context)
    return HttpResponseRedirect('/')


def board_detail(request, board_id=None):
    board = get_or_none(Board,id=board_id)
    if board :
        boardimg = BoardImg.objects.filter(board=board)
        contents = encode_con(board.con)
        for i in range(0,len(boardimg)) :
            contents = contents.replace("{{%d}}"%i, "<a href='%s' target='_blank'><img src='%s' class='img_board_src'></a>"%(boardimg[i].src.url,boardimg[i].src.url))

        contents = contents.replace("http://tktv.co.kr/news/upload/", "/media/oldboard/")
        if not request.user.is_superuser :
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
        return render(request, 'board_detail.html', context)
    return HttpResponseRedirect('/')


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
            return HttpResponseRedirect("/board/detail/%d"%(board.id))
    if board :
        contents = board.con
        boardimg = BoardImg.objects.filter(board=board)
        context = {
            'board':board,
            'submenu':board.submenu,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'board_write'
        }
        return render(request, 'board_write.html', context)
    return HttpResponseRedirect('/')


def board_delete(request):
    board_id = request.POST.get("board_id")
    board = get_or_none(Board,id=board_id)
    sub_menu = board.submenu
    if board :
        if board.user == request.user or request.user.profile().grade.level == 10 :
            board.delete()
            return HttpResponse("")
    return HttpResponse("삭제 실패")


def board_reply(request, board_id=None):
    boardreply = BoardReply.objects.filter(board=board_id).order_by("-date_updated")
    context = {
            'boardreply':boardreply,
            'user': request.user
        }
    return render(request, 'board_reply.html', context)


def board_reply_post(request):
    board_id = request.POST.get("board_id")
    con = request.POST.get("con")
    BoardReply.objects.create(board_id=board_id,user=request.user,con=con)
    return board_reply(request, board_id)


def board_reply_delete(request):
    boardreply_id = request.POST.get("boardreply_id")
    boardreply = get_or_none(BoardReply,id=boardreply_id)
    if boardreply :
        if boardreply.user == request.user or request.user.profile().grade.level == 10 :
            board = boardreply.board
            boardreply.delete()
            return board_reply(request, board.id)
    return HttpResponse("로드 실패")