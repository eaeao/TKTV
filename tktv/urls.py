"""tktv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from tktv import settings
from tktv.alimi import views as alimiview
from tktv.board import views as boardview
from tktv.form import views as formview
from tktv.main import views as mainview
from tktv.mobile import views as mobileview
from tktv.page import views as pageview

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', mainview.main),
                  url(r'^user/$', mainview.user),
                  url(r'^user/login/$', mainview.user_login),
                  url(r'^user/logout/$', mainview.user_logout),
                  url(r'^user/join/$', mainview.user_join),
                  url(r'^user/join/get/$', mainview.user_join_get),
                  url(r'^search/$', mainview.search_board),
                  url(r'^search/board/$', mainview.search_board),
                  url(r'^search/page/$', mainview.search_board),
                  url(r'^board/reply/delete/$', boardview.board_reply_delete),
                  url(r'^board/reply/post/$', boardview.board_reply_post),
                  url(r'^board/reply/(?P<board_id>.*)$', boardview.board_reply),
                  url(r'^board/delete/$', boardview.board_delete),
                  url(r'^board/write/(?P<sub_id>.*)$', boardview.board_write),
                  url(r'^board/detail/(?P<board_id>.*)$', boardview.board_detail),
                  url(r'^board/modify/(?P<board_id>.*)$', boardview.board_modify),
                  url(r'^board/(?P<sub_id>.*)$', boardview.board),
                  url(r'^page/upload/$', pageview.page_upload),
                  url(r'^page/edit/(?P<sub_id>.*)$', pageview.page_edit),
                  url(r'^page/(?P<sub_id>.*)$', pageview.page),
                  url(r'^form/result/(?P<sub_id>.*)$', formview.form_result),
                  url(r'^form/(?P<sub_id>.*)$', formview.form),
                  url(r'^alimi/$', alimiview.alimi),
                  url(r'^alimi/list/$', alimiview.alimi_list),
                  url(r'^alimi/manager/$', alimiview.alimi_manager),
                  url(r'^mobile/$', mobileview.main),
                  url(r'^mobile/recent/$', mobileview.recent),
                  url(r'^mobile/board/write/(?P<sub_id>.*)$', mobileview.board_write),
                  url(r'^mobile/board/detail/(?P<board_id>.*)$', mobileview.board_detail),
                  url(r'^mobile/board/modify/(?P<board_id>.*)$', mobileview.board_modify),
                  url(r'^mobile/board/(?P<sub_id>.*)$', mobileview.board),
                  url(r'^mobile/page/(?P<sub_id>.*)$', mobileview.page),
                  url(r'^mobile/form/(?P<sub_id>.*)$', mobileview.form),
                  url(r'^mobile/user/$', mobileview.user),
                  url(r'^mobile/user/login/$', mobileview.user_login),
                  url(r'^mobile/user/logout/$', mobileview.user_logout),
                  url(r'^mobile/user/join/$', mobileview.user_join),
                  url(r'^mobile/user/join/get/$', mobileview.user_join_get),
                  url(r'^mobile/auto_down/$', TemplateView.as_view(template_name='mobile/auto_down.html', content_type='text/html')),
                  url(r'^mobile/facebook_link.html$', TemplateView.as_view(template_name='mobile/facebook_link.html', content_type='text/html')),
                  url(r'^mobile/kakao_link.html$', TemplateView.as_view(template_name='mobile/kakao_link.html', content_type='text/html')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
