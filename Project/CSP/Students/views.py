from django.shortcuts import render
from django.template import RequestContext, loader
from Students.models import *
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from portal.views import checkIdentity,search,portalSearchResults
from adminStaff.models import *
from portal.models import Feedback

def index(request):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		template = loader.get_template('Students/index.html')
		current = Student.objects.filter(username=request.session['username'])[0]
		attendance = AttendanceDaily.objects.filter(rollno=current.id,present=False)
		context = RequestContext(request, {'current': current,'attendance':attendance,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def uploadPicture(request,roll_no):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		template = loader.get_template('Students/index.html')
		current = Student.objects.filter(username=request.session['username'])[0]
		if request.method == "POST":
			picture = request.FILES['picture']
			if picture:
				current.username.photo = picture
				current.username.save(update_fields=['photo',])
		attendance = AttendanceDaily.objects.filter(rollno=current.id,present=False)
		context = RequestContext(request, {'current': current,'attendance':attendance,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def private_index(request):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		template = loader.get_template('Students/private_profile.html')
		current = Student.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)

def feedback(request):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		current = Student.objects.filter(username=request.session['username'])[0]
		if request.method == "POST":
			feedback_message = request.POST['feedback_message']
			flag = Feedback(message=feedback_message, fromusername=str(current.username), fromrole='student')
			flag.save()
			return index(request)
	return HttpResponseRedirect(redirect)

def editStudentProfile(request,roll_no):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		current = Student.objects.filter(username=request.session['username'])[0]
		if request.method == "POST":
			fathers_name = request.POST['fathersname']
			mothers_name = request.POST['mothersname']
			roomno = request.POST['roomno']
			private = request.POST.getlist('private[]')
			if "private" in private:
				private = True
			else:
				private = False
			hostel = request.POST['hostel']
			pa_flatno = request.POST['pa_flatno']
			pa_line1 = request.POST['pa_line1']
			pa_line2 = request.POST['pa_line2']
			pa_city = request.POST['pa_city']
			pa_state = request.POST['pa_state']
			pa_country = request.POST['pa_country']
			pa_pincode = request.POST['pa_pincode']
			update = current
			update.fathers_name = fathers_name
			update.mothers_name = mothers_name
			update.roomno = roomno
			update.hostel = hostel
			update.pa_flatno = pa_flatno
			update.pa_line1 = pa_line1
			update.pa_line2 = pa_line2
			update.pa_city = pa_city
			update.pa_state = pa_state
			update.pa_country = pa_country
			update.pa_pincode = pa_pincode
			update.private = private
			update.save(update_fields=['private','fathers_name','mothers_name','roomno','hostel','pa_flatno','pa_line1','pa_line2','pa_city','pa_state','pa_country','pa_pincode',])
			return index(request)
	return HttpResponseRedirect(redirect)

def searchResults(request):
    redirect = checkIdentity(request, 'student')
    if redirect == "":
        current = Student.objects.filter(username=request.session['username'])[0]
        return portalSearchResults(request, 'Students/_searchResults.html', 'student', current)
    return HttpResponseRedirect(redirect)

def viewStudentProfile(request,roll_no):
	redirect = checkIdentity(request,'student')
	if redirect == "":
		current = Student.objects.filter(username=request.session['username'])[0]
		student = Student.objects.filter(rollno = roll_no)[0]
		private = student.private
		if student == current:
			private = False
		if private:
			template = loader.get_template('Students/private_profile.html')
			context = RequestContext(request, {'current': current, 'student':student,})
			return HttpResponse(template.render(context))
		else:
			return studentViewStudentProfile(request,roll_no,'Students/viewStudentProfile.html',current)
	return HttpResponseRedirect(redirect)

def studentViewStudentProfile(request,roll_no,template,currentUserObject):
    template = loader.get_template(template)
    current = currentUserObject
    student = Student.objects.filter(rollno = roll_no)[0]
    attendance = AttendanceDaily.objects.filter(rollno=student.id,present=False)
    context = RequestContext(request, {'current': current, 'student':student, 'attendance':attendance,})
    return HttpResponse(template.render(context))



