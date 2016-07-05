# -*- coding: utf-8 -*-
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from tktv.form.models import Form, FormData
from tktv.main.models import SubMenu, get_or_none, getMain, upload


def form(request, sub_id=None):
    submenu = get_or_none(SubMenu,id=sub_id)
    if submenu :
        if request.POST.get("csrfmiddlewaretoken") :
            forms = Form.objects.filter(submenu=submenu)
            if forms :
                for form in forms :
                    value=request.POST.get(form.name)
                    if value :
                        FormData.objects.create(user=request.user,form=form,value=value)
                    #upload(request)
                context = {
                    'submenu':submenu,
                    'user': request.user,
                    'getMain':getMain(),
                    'appname':'form'
                }
            return render(request, 'form_result.html', context)
        else :
            forms = Form.objects.filter(submenu=submenu)
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