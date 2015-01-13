from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from hitcount.views import update_hit_count_ajax
from tktv import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tktv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^ajax/hit/$', update_hit_count_ajax, name='hitcount_update_ajax'),
    url(r'^$', 'tktv.main.views.main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/$', 'tktv.main.views.user'),
    url(r'^user/login/$', 'tktv.main.views.user_login'),
    url(r'^user/logout/$', 'tktv.main.views.user_logout'),
    url(r'^user/join/$', 'tktv.main.views.user_join'),
    url(r'^user/join/get/$', 'tktv.main.views.user_join_get'),
    url(r'^board/reply/delete/$', 'tktv.board.views.board_reply_delete'),
    url(r'^board/reply/post/$', 'tktv.board.views.board_reply_post'),
    url(r'^board/reply/(?P<board_id>.*)$', 'tktv.board.views.board_reply'),
    url(r'^board/delete/$', 'tktv.board.views.board_delete'),
    url(r'^board/write/(?P<sub_id>.*)$', 'tktv.board.views.board_write'),
    url(r'^board/detail/(?P<board_id>.*)$', 'tktv.board.views.board_detail'),
    url(r'^board/modify/(?P<board_id>.*)$', 'tktv.board.views.board_modify'),
    url(r'^board/(?P<sub_id>.*)$', 'tktv.board.views.board'),
    url(r'^page/(?P<sub_id>.*)$', 'tktv.page.views.page'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()