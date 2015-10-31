from django.conf.urls import patterns, url

from ta import views

urlpatterns = patterns('',
  url(r'^$', views.index, name='home'),
  url(r'^updateAttendance/(?P<course_code>\w+)/$', views.attendance, name='view'),
    url(r'^updateMarks/(?P<course_code>\w+)/$', views.updateMarks, name='Update'),
    url(r'^processUploadMarks/(?P<course_code>\w+)/$', views.processUploadMarks, name='processUploadMarks'),
    url(r'^uploadSeatingChart/(?P<course_code>\w+)/$', views.uploadSeatingChart, name='processUploadMarks'),
    url(r'^processUploadAttendance/(?P<course_code>\w+)/$', views.processUploadAttendance, name='processUploadAttendance'),
)
