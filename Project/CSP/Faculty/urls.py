from django.conf.urls import patterns, url

from Faculty import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^attendance/(?P<course_code>\w+)/$', views.attendance, name='attendance'),
    url(r'^grades/(?P<course_code>\w+)/$', views.grades, name='grades'),
    url(r'^editProfile', views.editprofile, name='schedule'),
    url(r'^reports', views.reports, name='reports'),
 	url(r'^viewStudent/(?P<roll_no>\w+)/$', views.viewStudentProfile, name='viewStudent'),
	url(r'^searchResults', views.searchResults, name='search'),
	url(r'^exportOrEmail', views.emailOrExport, name='reportsfilters'),
	url(r'^processUploadMarks/(?P<course_code>\w+)/$', views.processUploadMarks, name='processUploadMarks'),
	url(r'^uploadSeatingChart/(?P<course_code>\w+)/$', views.uploadSeatingChart, name='processUploadMarks'),
	url(r'^processUploadAttendance/(?P<course_code>\w+)/$', views.processUploadAttendance, name='processUploadAttendance'),    
)
