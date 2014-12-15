from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from tktv import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tktv.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'tktv.main.views.main'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^board/detailed/(?P<board_id>.*)$', 'tktv.board.views.board_detailed'),
    url(r'^board/(?P<sub_id>.*)$', 'tktv.board.views.board'),
    url(r'^page/(?P<sub_id>.*)$', 'tktv.page.views.page'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
urlpatterns += staticfiles_urlpatterns()