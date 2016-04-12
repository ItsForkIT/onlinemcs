from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sync/$', views.sync, name='sync'),
    url(r'^analysis/graphical$', views.graphicalAnalysis, name='graphicalAnalysis'),
	url(r'^analysis/tables$', views.tabularAnalysis, name='tabularAnalysis'),
    url(r'^filemanager/imageView$', views.imageView, name='imageView'),
    url(r'^filemanager/videoView$', views.videoView, name='videoView'),
    url(r'^filemanager/audioView$', views.audioView, name='audioView')
]
