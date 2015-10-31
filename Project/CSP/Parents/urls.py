from django.conf.urls import patterns, url
from Parents import views

urlpatterns = patterns('',
    url(r'^index', views.index, name='index'),
    url(r'^attendance', views.attendance, name='attendance'),
    url(r'^contacts', views.contacts, name='contacts'),
    url(r'^grades', views.grades, name='grades'),
    url(r'^links', views.links, name='links'),
    url(r'^$', views.notifications, name='notifications'),
    url(r'^notifications', views.notifications, name='notifications'),
    url(r'^editprofile', views.profile, name='profile'),
    url(r'^statistics', views.statistics, name='statistics'),
    url(r'^feedback', views.feedback, name='feedback')
   
)
