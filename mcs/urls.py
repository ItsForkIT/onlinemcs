from django.conf.urls import url,patterns
from django.conf import settings
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sync/$', views.sync, name='sync'),
    url(r'^analysis/graphical$', views.graphicalAnalysis, name='graphicalAnalysis'),
    url(r'^analysis/embs$', views.embs, name='embs'),
	url(r'^analysis/tables$', views.tabularAnalysis, name='tabularAnalysis'),
    url(r'^filemanager/imageView$', views.imageView, name='imageView'),
    url(r'^filemanager/videoView$', views.videoView, name='videoView'),
    url(r'^filemanager/audioView$', views.audioView, name='audioView'),
    url(r'^filemanager/groupView$', views.groupView, name='groupView'),
    url(r'^reportGen$', views.reportGen, name='reportGen'),
    url(r'^sms$', views.sms, name='sms'),
    url(r'^missing$', views.missing, name='missing'),
    url(r'^editProfile$', views.editProfile, name='editProfile'),
    url(r'^tasks/$', views.tasks.task_list, name='task_list'),
   # url(r'^tasks/(?P<pk>[0-9]+)$', 'task_detail', name='task_detail'),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
