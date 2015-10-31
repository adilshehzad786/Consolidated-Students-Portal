from django.db import models

# Create your models here.
# TAs
# Roll No ---- NOT NULL Integer Foreign Key(Students)
# Username ---- NOT NULL String Unique
# Password ---- NOT NULL String
# Course Code ---- NOT NULL String Foreign Key(Courses)
# Role ---- String

class TA(models.Model):
	rollno = models.ForeignKey('Students.Student',to_field='rollno')
	username = models.ForeignKey('portal.EmailUser',to_field = 'email',unique=True)
	role = models.CharField(max_length=100)
	coursecode = models.ForeignKey('portal.Course')

	def __unicode__(self):
		return str(self.username)

class Document(models.Model):
	docfile = models.FileField(upload_to='documents/%Y/%m/%d')