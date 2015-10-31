from django.conf.urls import patterns, url

from Reports import views

urlpatterns = patterns('',
    url(r'^Reports/$', views.Reports, name='Reports')
)
