from django.db import models
from django.contrib.auth.models import User
import re
import uuid
from Students.models import Record
from Parents.models import Parents
from django.core import validators
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django import forms
from ta.models import TA
from PIL import Image

class UserManager(BaseUserManager):
 
	def _create_user(self, email, password,
	is_staff, is_superuser, is_student,is_faculty,is_ta,is_facultystaff,is_adminstaff,is_parent):
		now = timezone.now()
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		is_active = True
		user = self.model(email=email, is_staff=is_staff, is_active=is_active,
		is_superuser=is_superuser, last_login=now,
		date_joined=now, is_student=is_student,is_faculty=is_faculty,is_ta=is_ta,is_facultystaff=is_facultystaff,is_adminstaff=is_adminstaff,is_parent=is_parent)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password, is_student,is_faculty,is_ta,is_facultystaff,is_adminstaff,is_parent):
		is_staff = False
		return self._create_user(email, password, is_staff, False, is_student,is_faculty,is_ta,is_facultystaff,is_adminstaff,is_parent)
	def create_superuser(self, email, password):
		return self._create_user(email, password, True, True, False, False, False, False, False, False)


class EmailUser(AbstractBaseUser, PermissionsMixin):
	firstname = models.CharField(_('first name'), max_length=50, blank=True, null=True)
	lastname = models.CharField(_('last name'), max_length=50, blank=True, null=True)
	email = models.EmailField(_('email address'), max_length=255,unique=True,db_index=True)
	is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
	is_active = models.BooleanField(_('active'), default=False, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
	is_student = models.BooleanField(_('Student Status'), default=False,)
	is_faculty = models.BooleanField(_('Faculty Status'), default=False,)
	is_facultystaff = models.BooleanField(_('Faculty Staff Status'), default=False,)
	is_adminstaff = models.BooleanField(_('Admin Staff Status'), default=False,)
	is_ta = models.BooleanField(_('TA Status'), default=False,)
	is_parent = models.BooleanField(_('Parent Status'), default=False,)
	date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
	photo = models.ImageField(upload_to='images',blank=True)
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
 	objects = UserManager()

 	def __unicode__(self):
 		return self.email

	def get_full_name(self):
		fullname = self.firstname + " " + self.lastname
		return fullname.strip()
 
	def get_short_name(self):
		return self.firstname
 
	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.username])

	def getParent(self,student):
		return Parents.objects.filter(roll_no = student.rollno)
		
	def createParent(self,student):
		k = student.username.email
		k = student.name.lower().replace(' ', '.')
		k = k+'@parents.iiit.ac.in'
		l = student.rollno%1000
		if l < 100:
			passend = '0' + str(l)
		else:
			passend = str(l)
		password = student.name[0:3].lower() + passend
		emailuser = EmailUser.objects.create_user(k,password,False,False,False,False,False,True)
		parent = Parents.objects.create(name=student.fathers_name,plot_flatno=student.pa_flatno,addr_line1=student.pa_line1,
			addr_line2=student.pa_line2,city=student.pa_city,state=student.pa_state,country=student.pa_country,pincode=student.pa_pincode,
			contact_no='-',roll_no=student.rollno,username=emailuser)
		parent.save()


	class Meta:
   		verbose_name = _('user')
    	verbose_name_plural = _('users')

class Course(models.Model):
	coursetype = models.CharField(max_length=3)
	courseno = models.IntegerField()
	coursecode = models.CharField(max_length=6)
	coursename = models.CharField(max_length=50)
	course_description = models.CharField(max_length=1800)
	semester_offered = models.CharField(max_length=5)
	year = models.IntegerField()
	faculty = models.ForeignKey('Faculty.Faculty')
	no_of_credits = models.IntegerField()

	def __unicode__(self):
		return self.coursecode

	def getTAs(self):
		return TA.objects.filter(coursecode_id = self.id)

	def getFaculty(self):
		return self.faculty

	def getStudents(self):
		return Record.objects.filter(coursecode=self.id)

	def getCourseDate(self):
		return self.semester_offered[0].upper() + str(self.year)

class Notification(models.Model):
	date = models.DateField(auto_now=False, auto_now_add=True)
	message = models.CharField(max_length=1800)
	fromid = models.ForeignKey('adminStaff.AdminStaff',to_field='username')
	to = models.CharField(max_length=500)

	def __unicode__(self):
		return self.message

class Feedback(models.Model):
	STUDENT = 'ST'
	FACULTY = 'FA'
	FACULTY_STAFF = 'FS'
	TEACHING_ASSISTANTS = 'TA'
	PARENT ='PT'
	ROLE = {
		(STUDENT, 'Student'),
		(FACULTY, 'Faculty'),
		(FACULTY_STAFF, 'Faculty Staff'),
		(TEACHING_ASSISTANTS, 'Teaching Assistant'),
		(PARENT, 'PARENT'),
	}
	date = models.DateField(auto_now=False, auto_now_add=True)
	message = models.CharField(max_length=1800)
	fromusername = models.CharField(max_length=75)
	fromrole = models.CharField(max_length=2, choices=ROLE, default=STUDENT)

	def __unicode__(self):
		return self.message

