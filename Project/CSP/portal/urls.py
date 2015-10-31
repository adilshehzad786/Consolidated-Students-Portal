from django.conf.urls import patterns, url
from portal import views

urlpatterns = patterns('',
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^access_denied/$', views.access_denied, name='denied'),
)


