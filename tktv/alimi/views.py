import json

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from tktv.alimi.models import Shop, ShopDevice
from tktv.form.models import FormData
from tktv.main.models import get_or_none


@csrf_exempt
def alimi(request):
    state = []
    sid = request.GET.get("sid")
    pw = request.GET.get("pw")
    regid = request.GET.get("regid")
    os = request.GET.get("os",0)
    shop = get_or_none(Shop,sid=sid,password=pw)
    if shop :
        if regid :
            device = get_or_none(ShopDevice,uid=regid)
            if device :
                if sid :
                    device.sid = sid
                    device.is_admin=1
                    device.save()
            else :
                ShopDevice.objects.create(sid=sid,uid=regid,is_admin=1,os=os)
    else :
        shop = get_or_none(Shop,sid=sid)
        if regid :
            device = get_or_none(ShopDevice,uid=regid)
            if device :
                if sid :
                    device.sid = sid
                    device.is_admin=0
                    device.save()
            else :
                ShopDevice.objects.create(sid=sid,uid=regid,is_admin=0,os=os)
    state.append({
        "sid":shop.sid,
        "sname":u"%s"%shop.name,
        "url":shop.alimi_url,
        "url2":shop.event_url,
        "state":u"%s"%(regid)
    })
    return HttpResponse(json.dumps(state), content_type="application/json")

@csrf_exempt
def alimi_list(request):
    str = "LIST"
    devices = ShopDevice.objects.all()
    for device in devices :
        str = "%s<br>[%d]%s(os:%s, admin:%s) : %s"%(str, device.id, device.sid, device.os, device.is_admin, device.uid)
    return HttpResponse(str)

@csrf_exempt
def alimi_manager(request):
    if request.GET.get('delete'):
        fid = int(request.GET.get('delete',0))
        for i in range(0,7):
            get_or_none(FormData,id=fid+i).delete()
        return HttpResponse("OK")
    formdatas = FormData.objects.filter(form__submenu=25).order_by("-id")

    context = {
        "formdatas":formdatas
    }
    return render(request, "mobile/alimi_manager.html", context, content_type="application/xml")