from django.contrib import admin
from portal.models import EmailUser
from portal.models import Course, Notification, Feedback
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from portal.forms import EmailUserCreationForm, EmailUserChangeForm
from django.utils.translation import ugettext_lazy as _
from django import forms
# Register your models here.

class EmailUserAdmin(UserAdmin):
	fieldsets = (
		(None, {'fields': ('email', 'password')}),
		(_('Roles'), {'fields': ('photo','is_student', 'is_parent','is_adminstaff','is_faculty','is_facultystaff','is_ta')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
			'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(_('Login Details'), {'classes': ('wide',),'fields': ('email', 'password1', 'password2')}),(_('Roles'), {'fields': ('is_student', 'is_parent','is_adminstaff','is_faculty','is_facultystaff','is_ta')}),
	)
	form = EmailUserChangeForm
	add_form = EmailUserCreationForm

	list_display = ('email', 'is_staff')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ('groups', 'user_permissions',)
 
admin.site.register(EmailUser, EmailUserAdmin)
admin.site.register(Course)
admin.site.register(Notification)
admin.site.register(Feedback)
