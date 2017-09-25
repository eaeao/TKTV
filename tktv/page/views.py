import time

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from tktv.main.models import get_or_none, SubMenu, getMain
from tktv.page.models import Page


def page(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    contents = "생성된 페이지가 없습니다."
    if submenu :
        page = get_or_none(Page,submenu=submenu)
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
        return render(request, 'page.html', context)
    return HttpResponseRedirect('/')


def page_edit(request, sub_id=None):
    if not request.user.is_active: return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    submenu = get_or_none(SubMenu,id=sub_id)

    if submenu:
        page = get_or_none(Page, submenu=submenu)
        contents = request.POST.get('contents')
        if contents:
            page.con = contents
            page.save()
            return HttpResponseRedirect('/page/%d' % submenu.id)
        else:
            contents = page.con

        context = {
            'submenu':submenu,
            'page':page,
            'contents':contents,
            'user': request.user,
            'getMain':getMain(),
            'appname':'page'
        }
        return render(request, 'page_edit.html', context)
    return HttpResponseRedirect('/')


@csrf_exempt
def page_upload(request):
    filename = ""
    CKEditorFuncNum = request.GET.get('CKEditorFuncNum')
    try :
        if 'upload' in request.FILES:
            file = request.FILES['upload']
            filename = "%s.jpg"%(str(time.time()))
            fp = open('%s/%s' % ('/root/www/media/page/', filename) , 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
    except Exception as e :
        return HttpResponse('%s'%e)
    return HttpResponse(u"""
        <script type='text/javascript'>
        window.parent.CKEDITOR.tools.callFunction(%s, '%s','Success');
        </script>
        """ % (CKEditorFuncNum, '/media/page/%s' % filename))