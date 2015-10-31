from django.db import models
# from Faculty import Faculty
from portal.models import Course

# Create your models here.

# FACULTY STAFF
# ID ----  NOT NULL Integer Primary Key
# Faculty ID ----  NOT NULL Integer Foreign Key(Faculty)
# Course Code ----  NOT NULL String Foreign Key(Courses)
# Username ----  NOT NULL String Unique
# Password ---- NOT NULL String

class FacultyStaff(models.Model):
	name = models.CharField(max_length=50)
	facultyid = models.ForeignKey('Faculty.Faculty')
	username = models.ForeignKey('portal.EmailUser',to_field = 'email')
	coursecode = models.ForeignKey('portal.Course')

	def __unicode__(self):
		return str(self.username)

	def facultyDetails(self):
		return Faculty.objects.filter(id = self.facultyid)

	def courseDetails(self):
		return self.coursecode