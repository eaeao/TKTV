from django.shortcuts import render

# Create your views here.
from tktv.main.models import Main, MainMenu


def main(request):

    mainImg = Main.objects.all().order_by("-id")
    if mainImg :
        mainImg = mainImg[0].get_img()

    main_menu = MainMenu.objects.all()

    context = {
        'mainImg':mainImg,
        'main_menu':main_menu,
        'user': request.user,
        'appname':'main'
    }
    return render(request, 'main.html', context)