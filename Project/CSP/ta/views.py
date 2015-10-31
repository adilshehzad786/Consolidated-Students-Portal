from django.shortcuts import render
from django.template import RequestContext, loader
from ta.models import TA
from Students.models import *
from portal.models import *
from Faculty.models import Faculty
import os,sys
from Reports.views import *
from django.core.mail import send_mail
import csv
from portal.views import checkIdentity, search, portalSearchResults
from Students.views import studentViewStudentProfile
from django.db.models import Sum
from django.core.urlresolvers import reverse
from adminStaff.forms import DocumentForm,read
import numpy as np 
from string import whitespace
import CSP.settings
# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db import connection
#from portal.views import checkIdentity,search


def processUploadAttendance(request,course_code):
    redirect = checkIdentity(request, 'ta')
    if redirect == "":
        if request.method == 'POST':
            form1 = read(request.POST, request.FILES)
            total = request.POST['date1']
            course = Course.objects.get(id= course_code)
            if form1.is_valid():
                newdoc = Document1(docfile = request.FILES['docfile'])
                newdoc.save()
                path = os.path.abspath(newdoc.docfile.url[1:])
                mark = np.genfromtxt(path, dtype='str', delimiter=',',unpack='True',skip_header=1)
                for i in range(250):
                    try:
                        # k = mark[1][i]
                        student = Student.objects.get(rollno=int(mark[1][i]))
                        studentInCourse = course.getStudents().filter(rollno=student.id)
                        if studentInCourse:
                            k = str(total).split('/')
                            l = k[2]+"-"+k[1]+'-'+k[0]
                            if mark[2][i][0] == 'P':
                                present = True
                            else:
                                present=False
                            save = AttendanceDaily.objects.create(rollno=student,coursecode=course,date=l,present=present)
                            save.save()
                    except:
                        continue
        return index(request)
    return HttpResponseRedirect(redirect)

def processUploadMarks(request,course_code):
    redirect = checkIdentity(request, 'ta')
    if redirect == "":
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            total = request.POST['totalMarks']
            examName = request.POST['examName']
            course = Course.objects.get(id= course_code)
            if form.is_valid():
                newdoc = Document(docfile = request.FILES['docfile'])
                newdoc.save()
                path = os.path.abspath(newdoc.docfile.url[1:])
                mark = np.genfromtxt(path, dtype='str', delimiter=',',unpack='True',skip_header=1)
                for i in range(250):
                    # if mark[1][i]:
                    try:
                        student = Student.objects.get(rollno=int(mark[1][i]))
                        studentInCourse = course.getStudents().filter(rollno=student.id)
                        if studentInCourse:
                            looo = mark[2][i]
                            save = Marks.objects.create(rollno=student,category=examName,semester_date=course.semester_offered[0] + str(course.year),
                                coursecode=course,marks=int(mark[2][i]),total=int(total))
                            save.save()
                    except:
                        continue
        return index(request)
    return HttpResponseRedirect(redirect)

def index(request):
    redirect = checkIdentity(request,'ta')
    if redirect == "":
        template = loader.get_template('ta/index.html')
        current = TA.objects.filter(username=request.session['username'])[0]
        ListofStudents = Record.objects.filter(coursecode=current.coursecode.id)
        context = RequestContext(request, {'current': current,'ListofStudents': ListofStudents,})
        return HttpResponse(template.render(context))
    return HttpResponseRedirect(redirect)

def uploadSeatingChart(request,course_code):
    redirect = checkIdentity(request, 'ta')
    if redirect == "":
        if request.method == 'POST':   
            date = request.POST['dateOfAttendance']
            chart = request.FILES['seating']
            seats = request.POST.getlist('SD[]')
            newdoc = Document(docfile = chart)
            newdoc.save()
            course = Course.objects.get(id= course_code)
            path = os.path.abspath(newdoc.docfile.url[1:])
            mark = np.genfromtxt(path, dtype='str', delimiter=',',unpack='True',skip_header=1)
            for i in range(250):
                try:
                    # k = mark[1][i]
                    student = Student.objects.get(rollno=int(mark[1][i]))
                    studentInCourse = course.getStudents().filter(rollno=student.id)
                    if studentInCourse:
                        seatnumber = mark[2][i]
                        if str(seatnumber) in seats:
                            present = True
                        else:
                            present = False
                        k = str(date).split('/')
                        l = k[2]+"-"+k[1]+'-'+k[0]
                        save = AttendanceDaily.objects.create(rollno=student,coursecode=course,date=l,present=present)
                        save.save()
                except:
                    continue
        return index(request)
    return HttpResponseRedirect(redirect)

def attendance(request,course_code):
    redirect = checkIdentity(request,'ta')
    if redirect == "":
        template = loader.get_template('ta/_attendance.html')
        current = TA.objects.filter(username=request.session['username'])[0]
        course = Course.objects.filter(pk=course_code)[0]
        course_semester = course.semester_offered
        if course_semester[0] == "M":
            course_semester = "Monsoon"
        else:
            course_semester = "Spring"
        faculty = course.getFaculty().name
        if request.method == "POST":
            ListofStudents = course.getStudents()
            period = request.POST['periods']
            period = AttendanceMonthly.objects.filter(id = int(period))
            if period:
                selectValue = period[0]
                attendance = []
                for student in ListofStudents:
                    l = student.id
                    k = student.rollno
                    total = AttendanceDaily.objects.filter(rollno=student.rollno, coursecode=course.id, present=True, date__range=(period[0].start_date, period[0].end_date))
                    attendance.append(total.count())
                    # return adf
                ListofStudents = zip(ListofStudents,attendance)
                total = period[0].classes_taken_place
                totalList = AttendanceMonthly.objects.filter(coursecode=course.id)
            else:
                selectValue = 0
                attendance = []
                for student in ListofStudents:
                    l = student.id
                    k = student.rollno
                    total = AttendanceDaily.objects.filter(rollno=student.rollno, coursecode=course.id, present=True)
                    attendance.append(total.count())
                    # return adf
                ListofStudents = zip(ListofStudents,attendance)
                total = AttendanceMonthly.objects.filter(coursecode=course.id).aggregate(Sum('classes_taken_place'))
                totalList = AttendanceMonthly.objects.filter(coursecode=course.id)
                # return wers
                total = total['classes_taken_place__sum']
            context = RequestContext(request, {'current': current, 'course': course, 'faculty': faculty,
             'course_semester': course_semester, 'ListofStudents': ListofStudents, 'total': total, 'totalList': totalList,'selectValue': selectValue})
        else:
            selectValue = 0
            ListofStudents = course.getStudents()
            attendance = []
            for student in ListofStudents:
                l = student.id
                k = student.rollno
                total = AttendanceDaily.objects.filter(rollno=student.rollno, coursecode=course.id, present=True)
                attendance.append(total.count())
                # return adf
            ListofStudents = zip(ListofStudents,attendance)
            total = AttendanceMonthly.objects.filter(coursecode=course.id).aggregate(Sum('classes_taken_place'))
            totalList = AttendanceMonthly.objects.filter(coursecode=course.id)
            # return wers
            form1 = read()
            total = total['classes_taken_place__sum']
            context = RequestContext(request, {'current': current, 'course': course, 'faculty': faculty,
             'course_semester': course_semester, 'ListofStudents': ListofStudents, 'total': total, 'totalList': totalList, 'selectValue':selectValue,'form1':form1})
        return HttpResponse(template.render(context))
    return HttpResponseRedirect(redirect)

def upload(request):
	redirect = checkIdentity(request,'ta')
	if redirect == "":
		template = loader.get_template('ta/upload.html')
		current = TA.objects.filter(username=request.session['username'])[0]
		context = RequestContext(request, {'current': current,})
		return HttpResponse(template.render(context))
	return HttpResponseRedirect(redirect)


def updateMarks(request, course_code):
    redirect = checkIdentity(request, 'ta')
    if redirect == "":
        if request.method == 'POST':
            category = request.POST['category']
            k = []
            # if category == 'Quiz1':
            # 	cat = "Q1"
            # 	k = request.POST.getlist('Q1[]')
            #     k1 = request.POST.getlist('Q1T[]')
            # if category == 'Quiz2':
            # 	cat = "Q2"
            # 	k = request.POST.getlist('Q2[]')
            #     k1 = request.POST.getlist('Q2T[]')
            # if category == 'Quiz3':
            # 	cat = "Q3"
            # 	k = request.POST.getlist('Q3[]')
            #     k1 = request.POST.getlist('Q3T[]')
            if category == 'MidSem1':
                cat = "MD1"
                k = request.POST.getlist('MD1[]')
                k1 = request.POST.getlist('MD1T[]')
            elif category == 'MidSem2':
                cat = "MD2"
                k = request.POST.getlist('MD2[]')
                k1 = request.POST.getlist('MD2T[]')
            else:
                cat = "ESM"
                k = request.POST.getlist('ESM[]')
                k1 = request.POST.getlist('ESMT[]')
            names = request.POST.getlist('rollnos[]')
            UpdateList = zip(names,k,k1)
            course = Course.objects.filter(pk=course_code)[0]
            # return asf
            for name,marks,total in UpdateList:
                try:
                    Students = Marks.objects.get(coursecode=course.id, category=cat,rollno=name)
                    Students.marks = marks
                    Students.total = total
                    marks = marks
                    Students.save(update_fields=['marks','total'])
                except:
                    k = Student.objects.get(id=name)
                    if not marks:
                        marks = 0
                    if not total:
                        total = 0
                    l = Marks.objects.create(rollno=k,coursecode=course,category=cat,marks=float(int(marks)),total=float(int(total)))
                    l.save()
                #return ihuh
        template = loader.get_template('ta/_updateMarks.html')
        current = TA.objects.filter(username=request.session['username'])[0]
        course = Course.objects.filter(pk=course_code)[0]
        ListofStudents = course.getStudents()
        StudentName = []
        StudentID = []
        ListofMarks1 = []
        ListofMarks2 = []
        ListofMarks3 = []
        ListofTotal1 = []
        ListofTotal2 = []
        ListofTotal3 = []
        # ListofMarks4 = []
        # ListofMarks5 = []
        # ListofMarks6 = []
        # ListofTotal4 = []
        # ListofTotal5 = []
        # ListofTotal6 = []
        for student in ListofStudents:
            StudentName.append(student.rollno.name)
            StudentID.append(student.rollno.id)
            L1 = Marks.objects.filter(coursecode=course.id, category='MD1', rollno = student.rollno.id)
            L2 = Marks.objects.filter(coursecode=course.id, category='MD2', rollno = student.rollno.id)
            L3 = Marks.objects.filter(coursecode=course.id, category='ESM', rollno = student.rollno.id)
            # L4 = Marks.objects.filter(coursecode=course.id, category='Q1', rollno = student.rollno.id)
            # L5 = Marks.objects.filter(coursecode=course.id, category='Q2', rollno = student.rollno.id)
            # L6 = Marks.objects.filter(coursecode=course.id, category='Q3', rollno = student.rollno.id)
            if L1:
                ListofMarks1.append(L1[0].marks)
                ListofTotal1.append(L1[0].total)
            else:
                ListofMarks1.append([])
                ListofTotal1.append([])
            if L2:
                ListofMarks2.append(L2[0].marks)
                ListofTotal2.append(L2[0].total)
            else:
                ListofMarks2.append([])
                ListofTotal2.append([])
            if L3:
                ListofMarks3.append(L3[0].marks)
                ListofTotal3.append(L3[0].total)
            else:
                ListofMarks3.append([])
                ListofTotal3.append([])
            # if L4:
            #     ListofMarks4.append(L4[0].marks)
            #     ListofTotal4.append(L4[0].total)
            # else:
            #     ListofMarks4.append([])
            #     ListofTotal4.append([])
            # if L5:
            #     ListofMarks5.append(L5[0].marks)
            #     ListofTotal5.append(L5[0].total)
            # else:
            #     ListofMarks5.append([])
            #     ListofTotal5.append([])
            # if L6:
            #     ListofMarks6.append(L6[0].marks)
            #     ListofTotal6.append(L6[0].total)
            # else:
            #     ListofMarks6.append([])
            #     ListofTotal6.append([])
        ListofMarks = zip(StudentID,StudentName,ListofMarks1,ListofTotal1,ListofMarks2,ListofTotal2,ListofMarks3,ListofTotal3)#,ListofMarks4,ListofTotal4,ListofMarks5,ListofTotal5,ListofMarks6,ListofTotal6)
        form = DocumentForm()
        context = RequestContext(request, {'current': current, 'course': course, 'ListofMarks': ListofMarks,'form':form})
        return HttpResponse(template.render(context))
    return HttpResponseRedirect(redirect)
