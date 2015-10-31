from django.shortcuts import render
from django.template import RequestContext, loader
from Parents.models import Parents
from adminStaff.models import AttendanceDaily
from portal.models import *
from Students.models import Student
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from portal.views import checkIdentity,search
from django.db.models import Q
from random import randint

def index(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/index.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def attendance(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/attendance.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		dailyAttendance = AttendanceDaily.objects.filter(rollno = current.getStudent().id,present=False)
		context = RequestContext(request, {'current': current,'dailyAttendance':dailyAttendance})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)


def contacts(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/contacts.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)


def grades(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/grades.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)


def links(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/links.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)


def notifications(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/notifications.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		# notifications = Notification.objects.raw("SELECT * FROM portal_notification WHERE to LIKE \'%"+str(current.username)+"\'% OR to = 'ALL' ")
		lab = str(current.username)
		notifications = Notification.objects.filter(Q(to__contains = str(current.username))| Q(to__contains='ALL')) 
		context = RequestContext(request, {'current': current,'notifications':notifications})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def feedback(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		current = Parents.objects.filter(username=request.session['username'])[0]
		if request.method == "POST":
			feedback_message = request.POST['feedback_message']
			flag = Feedback(message=feedback_message, fromusername=str(current.username), fromrole='parent')
			flag.save()
			return notifications(request)
	return HttpResponseRedirect(redirect)

def profile(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		current = Parents.objects.filter(username=request.session['username'])[0]
		if request.method == "POST":
			name = request.POST['name']
			contact_number = request.POST['contact_number']
			plot_no = request.POST['plot_no']
			addr_line1 = request.POST['addr_line1']
			addr_line2 = request.POST['addr_line2']
			city = request.POST['city']
			state = request.POST['state']
			country = request.POST['country']
			pincode = request.POST['pincode']
			update = current
			update.name = name
			update.contact_no = contact_number
			update.plot_flatno = plot_no
			update.addr_line1 = addr_line1
			update.addr_line2 = addr_line2
			update.city = city
			update.state = state
			update.country = country
			update.pincode = pincode
			update.save(update_fields=['name','contact_no','plot_flatno','addr_line1','addr_line2','city','state','country','pincode',])
			# return afsd
			return notifications(request)
		else:
			template = loader.get_template('Parents/editprofile.html')
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def getCGPAByRange(cgpa_min, cgpa_max,current):
	StudentsList = Student.objects.filter(batch=current.getStudent().batch).filter(current_CGPA__gt=str(cgpa_min)).filter(current_CGPA__lte=str(cgpa_max)).count()
	return StudentsList

def getCGPAByRangeAndProgramme(cgpa_min, cgpa_max,current):
	StudentsList = Student.objects.filter(batch=current.getStudent().batch).filter(programme=current.getStudent().programme).filter(current_CGPA__gt=str(cgpa_min)).filter(current_CGPA__lte=str(cgpa_max)).count()
	return StudentsList

def getRandomColor():
	hexa = ('1','2','3','4','5','6','7','8','9','A','B','C','D','E','F')
	color = "#"
	i = 0
	while i < 6:
		color += hexa[randint(0,14)]
		i = i + 1
	return color

def statistics(request):
	redirect = checkIdentity(request,'parent')
	if redirect == "":
		template = loader.get_template('Parents/statistics.html')
		current = Parents.objects.filter(username=request.session['username'])[0]
		cgpalist = []
		colorlist1 = []
		colorlist2 = []
		keylist = []
		k = 6
		while k != 11:
			cgpalist.append(getCGPAByRange(k-1,k,current))
			colorlist1.append(getRandomColor())
			colorlist2.append(getRandomColor())
			keylist.append("CGPA - "+str(k-1)+".0 and "+str(k)+".0")
			k = k + 1
		cgpalist1 = zip(cgpalist,colorlist1,colorlist2,keylist)
		cgpalist = []
		colorlist1 = []
		colorlist2 = []
		keylist = []
		k = 6
		while k != 11:
			cgpalist.append(getCGPAByRangeAndProgramme(k-1,k,current))
			colorlist1.append(getRandomColor())
			colorlist2.append(getRandomColor())
			keylist.append("CGPA - "+str(k-1)+".0 and "+str(k)+".0")
			k = k + 1
		cgpalist2 = zip(cgpalist,colorlist1,colorlist2,keylist)
		context = RequestContext(request, {'current': current, 'cgpalist1': cgpalist1,'cgpalist2':cgpalist2})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)
