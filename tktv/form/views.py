import json
import urllib
import urllib.request

from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from tktv.form.models import Form, FormData, FormImage
from tktv.main.models import get_or_none, SubMenu, getMain


def form(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        forms = Form.objects.filter(submenu=submenu)
        if request.POST.get("csrfmiddlewaretoken") :
            recaptcha_response = request.POST.get('g-recaptcha-response')
            url = "https://www.google.com/recaptcha/api/siteverify"
            values = {
                'secret': '6LeLLiMUAAAAANevvEFmfvl8QwGde4GxHZE9tz-1',
                'response': recaptcha_response
            }
            data = urllib.parse.urlencode(values).encode()
            req = urllib.request.Request(url, data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode())

            if result['success']:
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
                        #upload(request)
                context = {
                    'submenu':submenu,
                    'user': request.user,
                    'getMain':getMain(),
                    'appname':'form'
                }
                return render(request, 'form_success.html', context)
        else :
            if forms :
                context = {
                    'submenu':submenu,
                    'forms':forms,
                    'user': request.user,
                    'getMain':getMain(),
                    'appname':'form'
                }
            return render(request, 'form.html', context)
    return HttpResponseRedirect('/')


def form_result(request, sub_id=None):
    if not request.user:
        return HttpResponse("권한이 없습니다.")
    if not request.user.is_superuser :
        return HttpResponse("권한이 없습니다.")
    submenu = get_or_none(SubMenu, id=sub_id)
    if submenu:
        forms = Form.objects.filter(submenu=submenu).order_by("id")
        formdatas = FormData.objects.filter(form__submenu=submenu).order_by("id")
        context = {
            'submenu': submenu,
            'forms':forms,
            'formdatas': formdatas,
            'user': request.user,
            'getMain': getMain(),
            'appname': 'form'
        }
        return render(request, 'form_result.html', context)
    return HttpResponseRedirect('/')