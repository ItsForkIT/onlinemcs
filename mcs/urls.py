from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^sync/$', views.sync, name='sync'),
    url(r'^analysis/graphical$', views.graphicalAnalysis, name='graphicalAnalysis'),
]
