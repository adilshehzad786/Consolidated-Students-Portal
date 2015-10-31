from django.conf.urls import patterns, url

from adminStaff import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^coursesList', views.coursesList, name='courses'),
    url(r'^viewCourse/(?P<course_code>\w+)/$', views.courseHome, name='coursePage'),
    url(r'^updateAttendance/(?P<course_code>\w+)/$', views.updateAttendance, name='attendance'),
    url(r'^addNewMonthlyAttendance/(?P<course_code>\w+)/$', views.addNewMonthlyAttendance, name='attendance'),
    url(r'^updateMarks/(?P<course_code>\w+)/$', views.updateMarks, name='marks'),
    url(r'^reports', views.reports, name='reports'),
    url(r'^viewStudent/(?P<roll_no>\w+)/$', views.viewStudentProfile, name='viewStudent'),
    url(r'^searchResults', views.searchResults, name='search'),
    url(r'^exportOrEmail', views.emailOrExport, name='reportsfilters'),
    url(r'^uploadPicture', views.uploadPicture, name='reportsfilters'),
    url(r'^processUploadMarks/(?P<course_code>\w+)/$', views.processUploadMarks, name='processUploadMarks'),
    url(r'^uploadSeatingChart/(?P<course_code>\w+)/$', views.uploadSeatingChart, name='processUploadMarks'),
    url(r'^processUploadAttendance/(?P<course_code>\w+)/$', views.processUploadAttendance, name='processUploadAttendance'),
)
