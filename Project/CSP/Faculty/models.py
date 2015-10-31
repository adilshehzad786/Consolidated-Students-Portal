from django.db import models
from portal.models import Course
# Create your models here.

# FACULTY
# Faculty ID ---- NOT NULL Primary Key
# Name ----  NOT NULL String
# Office No ---- Integer
# Building Name ---- String 
# Username ----  NOT NULL String Unique
# Password ----  NOT NULL String 
# Teaches  ---- NOT NULL Boolean

class Faculty(models.Model):
	name = models.CharField(max_length=50)
	officeno = models.IntegerField()
	buildingno = models.CharField(max_length=75)
	username = models.ForeignKey('portal.EmailUser',to_field = 'email')
	teaches = models.BooleanField()

	def __unicode__(self):
		return unicode(self.username)

	def coursesTaught(self):
		return Course.objects.filter(faculty=self.id)

	def getFacultyStaff(self):
		return FacultyStaff.objects.filter(facultyid = self.id)

