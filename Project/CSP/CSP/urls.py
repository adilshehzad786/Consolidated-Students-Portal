from django.conf.urls import patterns, include, url
from portal import views
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'portal.views.user_login', name='login'),
    url(r'^logout/', 'portal.views.logout_view', name='logout'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^reports/', include('Reports.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^Parents/', include('Parents.urls')),
    url(r'^parents/', include('Parents.urls')),
    url(r'^faculty/', include('Faculty.urls')),
    url(r'^facultystaff/', include('facultyStaff.urls')), 
    url(r'^portal/', include('portal.urls')),
    url(r'^adminStaff/', include('adminStaff.urls')),
    url(r'^student/', include('Students.urls')),
    url(r'^ta/', include('ta.urls')),
    url(r'^TA/', include('ta.urls')),
    url(r'^accounts/password_change/$', 
            'django.contrib.auth.views.password_change', 
            {'post_change_redirect' : '/accounts/password_change/done/'}, 
            name="password_change"), 
        (r'^accounts/password_change/done/$', 
            'django.contrib.auth.views.password_change_done'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

