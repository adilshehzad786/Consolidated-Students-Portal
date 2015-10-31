from django.db import models
from Students.models import Student

# Create your models here.

class Parents(models.Model):
	name = models.CharField(max_length=50)
	plot_flatno = models.CharField(max_length=50)
	addr_line1 = models.CharField(max_length=200)
	addr_line2 = models.CharField(max_length=200)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	country = models.CharField(max_length=50)
	pincode = models.IntegerField()
	contact_no = models.CharField(max_length=50)
	roll_no = models.IntegerField(primary_key=True)
	username = models.ForeignKey('portal.EmailUser',to_field = 'email')

	def __unicode__(self):
		return str(self.username)

	def getStudent(self):
		return Student.objects.filter(rollno = self.roll_no)[0]


