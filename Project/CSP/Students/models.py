from django.db import models
from django.db.models import Sum
# from Parents.models import Parents
# from portal.models import EmailUser
# from adminStaff.models import AttendanceDaily


class Student(models.Model):
	CSE = 'CSE'
	CSD = 'CSD'
	CND = 'CND'
	CHD = 'CHD'
	CLD = 'CLD'
	ECE = 'ECE'
	ECD = 'ECD'
	BSD = 'BSD'
	PROGRAMME = {
		(CSE, 'CSE'),
		(CSD, 'CSD'),
		(CND, 'CND'),
		(CHD, 'CHD'),
		(CLD, 'CLD'),
		(ECE, 'ECE'),
		(ECD, 'ECD'),
		(BSD, 'BSD'),
	}
	M = 'Male'
	F = 'Female'
	GENDER = {
		(M, 'Male'),
		(F, 'Female'),
	}
	rollno = models.IntegerField(unique=True)
	name = models.CharField(max_length=50)
	programme = models.CharField(max_length=3, choices=PROGRAMME,default=CSE)
	batch = models.CharField(max_length=4)
	gender = models.CharField(max_length=6, choices=GENDER, default=M)
	username = models.ForeignKey('portal.EmailUser',to_field = 'email')
	current_CGPA = models.DecimalField( max_digits=4, decimal_places=2)
	fathers_name = models.CharField(max_length=50)
	mothers_name = models.CharField(max_length=50)
	roomno = models.IntegerField()
	hostel = models.CharField(max_length=40)
	pa_flatno = models.CharField(max_length=50)
	pa_line1 = models.CharField(max_length=150)
	pa_line2 = models.CharField(max_length=150)
	pa_city = models.CharField(max_length=50)
	pa_state = models.CharField(max_length=50)
	pa_country = models.CharField(max_length=50)
	pa_pincode = models.IntegerField()
	private = models.BooleanField(default=False)
	tutorial_section = models.CharField(max_length=2)
	probation = models.BooleanField(default=False)

	def __unicode__(self):
		return unicode(self.rollno)

	def getPermanentAddress(self):
		Address = self.pa_flatno + " " + self.pa_line1 + "\n" + self.pa_line2 + "\n" + self.pa_city + ", " + self.pa_state + " " + self.pa_country + " - " + self.pa_pincode
		return Address

	def getSGPAs(self):
		return SGPA.objects.filter(rollno = self.id)

	def creditsCompleted(self):
		 total =  SGPA.objects.filter(rollno=self.id).aggregate(Sum('semester_credits'))
		 return total['semester_credits__sum']

	def getCurrentCourses(self):
		return Record.objects.raw("SELECT * FROM Students_record WHERE grade = 'NA' AND rollno = \'"+self.id+"\'")

	def getAllCourses(self):
		return Record.objects.filter(rollno=self.id)

	def getMarks(self):
		return Record.objects.raw("SELECT * FROM Students_marks WHERE rollno = \'"+self.id+"\'")

	def getCGPA(self):
		temp = self.getSGPAs()
		total1 = 0
		total2 = 0
		if temp:
			for sgpa in temp:
				total1 += sgpa.sgpa * sgpa.semester_credits
				total2 += sgpa.semester_credits
			return total1/total2
		else:
			return 0

	def save(self, *args, **kwargs):
		k = self.username.getParent(self)
		if not k:
			self.username.createParent(self)
		super(Student, self).save(*args, **kwargs)


class SGPA(models.Model):
	rollno = models.ForeignKey('Student')
	semester_date = models.CharField(max_length=5)
	sgpa = models.DecimalField( max_digits=4, decimal_places=2)
	cgpa = models.DecimalField( max_digits=4, decimal_places=2)
	semester_credits = models.IntegerField()

	def __unicode__(self):
		return str(self.rollno) + " - " + str(self.semester_date) + " - " + str(self.sgpa)


class Record(models.Model):
	Aplus = '10'
	A = '10'
	Aminus = '9'
	B = '8'
	Bminus = '7'
	C = '6'
	Cminus = '5'
	D = '4'
	F = '2'
	NA = '0'
	GRADES = {
		(NA, 'NA'),
		(Aplus, 'A+'),
		(A, 'A'),
		(Aminus, 'A-'),
		(B, 'B'),
		(Bminus, 'B-'),
		(C, 'C'),
		(Cminus, 'C-'),
		(D, 'D'),
		(F, 'F'),
	}
	rollno = models.ForeignKey('Student')
	semester_date = models.CharField(max_length=5)
	coursecode = models.ForeignKey('portal.Course')
	grade = models.CharField(max_length=2,choices=GRADES,default=NA)
	attendance_percentage = models.IntegerField(default = 0)

	def __unicode__(self):
		return unicode(self.rollno) 

	def getStudent(self):
		return self.rollno

	# def save(self, *args, **kwargs):
	# 	self.attendance_percentage = self.getAttendancePercentage()
	# 	super(Record, self).save(*args, **kwargs)

	def getMD1Percentage(self):
		record = Marks.objects.filter(rollno=self.rollno,coursecode=self.coursecode,category="MD1")
		if record:
			return (record[0].marks/record[0].total) * 100

	def getMD2Percentage(self):
		record = Marks.objects.filter(rollno=self.rollno,coursecode=self.coursecode,category="MD2")
		if record:
			return (record[0].marks/record[0].total) * 100

	def getESMPercentage(self):
		record = Marks.objects.filter(rollno=self.rollno,coursecode=self.coursecode,category="ESM")
		if record:
			return (record[0].marks/record[0].total) * 100

	def save(self, *args, **kwargs):
		super(Record, self).save(*args, **kwargs)
		
class Marks(models.Model):
	M1 = 'MD1'
	M2 = 'MD2'
	E = 'ESM'
	Q1 = 'Quiz1'
	Q2 = 'Quiz2'
	Q3 = 'Quiz3'
	CATEGORY = {
		(M1, 'MidSem1'),
		(M2, 'MidSem2'),
		(E, 'EndSem'),
		(Q1, 'Quiz1'),
		(Q2, 'Quiz2'),
		(Q3, 'Quiz3'),
	}

	rollno = models.ForeignKey('Student')
	semester_date = models.CharField(max_length=5)
	coursecode = models.ForeignKey('portal.Course')
	marks = models.DecimalField(max_digits=6 ,decimal_places=2)
	total = models.DecimalField(max_digits=6 ,decimal_places=2)
	category = models.CharField(max_length=3 ,choices=CATEGORY,default=M1)

	def __unicode__(self):
		#return str(self.rollno)  + " - " + str(self.semester_date)  + " - " + str(self.coursecode)  + " - " + str(self.category)  + " -" + str(self.marks) 
		return unicode(self.rollno)

	def getPercentage(self):
		return (self.marks)/(self.total)

class marksupload(models.Model):
	M1 = 'MD1'
	M2 = 'MD2'
	E = 'ESM'
	Q1 = 'Quiz1'
	Q2 = 'Quiz2'
	Q3 = 'Quiz3'
	CATEGORY = {
		(M1, 'MidSem1'),
		(M2, 'MidSem2'),
		(E, 'EndSem'),
		(Q1, 'Quiz1'),
		(Q2, 'Quiz2'),
		(Q3, 'Quiz3'),
	}
	category = models.CharField(max_length=3 ,choices=CATEGORY,default=M1)
	date = models.DateField()
	#epw_file = ContentTypeRestrictedFileField(upload_to='documents/EPW_DATA', content_types=['text/epw'],max_upload_size=5242880)
	epw_file = models.FileField(upload_to='documents/EPW_DATA/')





	
