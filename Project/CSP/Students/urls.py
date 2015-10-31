from django.conf.urls import patterns, url

from Students import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^viewStudent/(?P<roll_no>\w+)/$', views.viewStudentProfile, name='private'),
    url(r'^editStudentProfile/(?P<roll_no>\w+)/$', views.editStudentProfile, name='private'),
    url(r'^feedback/$', views.feedback, name='private'),
    url(r'^searchResults/$', views.searchResults, name='private'),
    url(r'^uploadPicture/(?P<roll_no>\w+)/$', views.uploadPicture, name='private'),
)
