from django.shortcuts import render
from django.template import RequestContext, loader
from portal.models import Course
from Students.models import Record, SGPA, Student
from adminStaff.models import *
from portal.models import *

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     template = loader.get_template('Reports/index.html')
#     context = RequestContext(request)
#     return HttpResponse(template.render(context))

def Reports(request, currentUserObject, template1, template2, app):
    current = currentUserObject
    if request.method == "POST":
        template = loader.get_template(template2)
        query_input = request.POST['list']
        course_type = request.POST['course_type']
        (StudentsList, ListofQueries) = parseQueryInput(request, query_input)
        context = RequestContext(request, {'current': current, 'list':query_input, 
                'StudentsList' : StudentsList,'course_type':course_type,
                'ListofQueries':ListofQueries, 'app': app})
    else:
        template = loader.get_template(template1)
        courseList = Course.objects.all()
        semesterList = Record.objects.raw('SELECT DISTINCT semester_date, id FROM Students_record')
        context = RequestContext(request, {'current': current, 'courseList':courseList, 'semesterList': semesterList, 'app': app })
    return HttpResponse(template.render(context))

def parseQueryInput(request, query_input):
    main_type = request.POST['main_type']
    semester_date = request.POST['semester_date']
    course_type = request.POST['course_type']
    ListofQueries = query_input.split(', ')
    if ListofQueries:
        ListofQueries.pop(0)
    if main_type == "courses":
        course = Course.objects.filter(coursename__startswith=course_type).values_list('id', flat=True)
        StudentsList = Record.objects.filter(coursecode__in=list(course))
        if ListofQueries:
            for query in ListofQueries:
                words = query.split()
                length = len(words)    
            StudentsList = parseCaller(ListofQueries, StudentsList, semester_date)
        return StudentsList, ListofQueries
    elif main_type == "career":
        Students = Student.objects.all().values_list('id', flat=True)
        list_of_records = []
        for student in Students:
            record = Record.objects.filter(rollno__in=list(Students))[0]
            list_of_records.append(record.id)
        StudentsList = Record.objects.filter(coursecode__in=list(list_of_records))
        if ListofQueries:
            for query in ListofQueries:
                words = query.split()
                length = len(words)    
            StudentsList = parseCaller(ListofQueries, StudentsList, semester_date)
        return StudentsList, ListofQueries
    elif main_type == "semester":
        StudentsList = SGPA.objects.filter(semester_date=semester_date)
        if ListofQueries:
            for query in ListofQueries:
                words = query.split()
                length = len(words)    
            StudentsList = parseCaller(ListofQueries, StudentsList, semester_date)
        return StudentsList, ListofQueries
    return ([],[])

def sendMail(ListofPeople, Subject, Message):
      send_mail(Subject, Message, 'cspssad43@gmail.com', ListofPeople, fail_silently=False)

def sendNotification(request, Student, Subject, Message):
    current = AdminStaff.objects.filter(username=request.session['username'])[0]
    if Student == 'ALL':
        flag = Notification(message=Message, fromid=current, to='ALL')
    else:
        flag = Notification(message=Message, fromid=current, to=Student.getParent)
    flag.save() 

def parseCaller(ListofQueries, StudentsList, semester_date):
    for query in ListofQueries:
        words = query.split()
        length = len(words)    
        if words[0] == "Batch":
            StudentsList = getBatchQuery(words, StudentsList)
        elif words[0] == 'Programme':
            StudentsList = getProgrammeQuery(words, StudentsList)
        elif words[0] == 'CGPA':
            StudentsList = getCGPAQuery(words, StudentsList)
        elif words[0] == 'Attendance':
            StudentsList = getAttendanceQuery(words, StudentsList)
        elif words[0] == 'Grade':
            StudentsList = getGradeQuery(words, StudentsList)
        elif words[0] == 'SGPA':
            StudentsList = getSGPAQuery(words, StudentsList, semester_date)
        elif words[0] == "Between":
            StudentsList = getTimeQuery(words, StudentsList)
        else:
            pass
    for query in ListofQueries:
        words = query.split()
        length = len(words)    
        if  words[0] == 'Marks':
            StudentsList = getMarksQuery(words, StudentsList)
    return StudentsList

def getBatchQuery(query, StudentsList):
    if len(query) != 3:
        return ""
    else:
        if query[1] == "before":
            StudentsList = StudentsList.filter(rollno__batch__lt=query[2])
        elif query[1] == "after":
            StudentsList = StudentsList.filter(rollno__batch__gt=query[2])
        elif query[1] == "is":
            StudentsList = StudentsList.filter(rollno__batch=query[2])
        return StudentsList
        
def getProgrammeQuery(query, StudentsList):
    if len(query) != 3 and len(query) != 4:
        return ""
    else:
        if len(query) == 4:
            StudentsList = StudentsList.exclude(rollno__programme=query[3])
        else:
            if query[2] == "*" and query[1] == 'is':
                return StudentsList
            else:
                 StudentsList = StudentsList.filter(rollno__programme=query[2])

        return StudentsList

def getCGPAQuery(query, StudentsList):
    if len(query) != 6:
        return ""
    else:
        if query[2] == "between":
            StudentsList = StudentsList.filter(rollno__current_CGPA__gte=query[3]).filter(rollno__current_CGPA__lte=query[5])
    return StudentsList

def getSGPAQuery(query, StudentsList, semester_date):
    if len(query) != 8:
        return ""
    else:
        if query[2] == "between":
            StudentsList = StudentsList.filter(sgpa__gte=query[3]).filter(sgpa__lte=query[5])
    return StudentsList

def getAttendanceQuery(query, StudentsList): #only for course
    if len(query) != 6:
        return ""
    else:
        if query[2] == "between":
            query[3] = query[3][:-1]
            query[5] = query[5][:-1]
            StudentsList = StudentsList.filter(attendance_percentage__gte=query[3]).filter(attendance_percentage__lte=query[5])
    return StudentsList

def getGradeQuery(query, StudentsList):
    if len(query) != 6:
        return ""
    else:
        if query[2] == "between":
            diction = {'A+':10,'A':10,'A-':9,'B':8,'B-':7,'C':6,'C-':5,'D':4,'F':2,}
            diction2 = {'A+':'10','A':'10','A-':'9','B':'8','B-':'7','C':'6','C-':'5','D':'4','F':'2',}
            gradesflag = []
            listgrades = []
            for each in diction:
                flag = 0
                if diction[each] >= diction[query[3]] and  diction[each] <= diction[query[5]]:
                    flag = 1
                if flag == 1:
                    gradesflag.append(1)
                    listgrades.append(diction2[each])
            StudentsList = StudentsList.filter(grade__in = listgrades)
    return StudentsList

def getMarksQuery(query, StudentsList):
    if len(query) != 8:
        return ""
    else:
        MD1 = 0
        ESM = 0
        MD2 = 0
        if query[2] == "between":
            if query[7] == 'MidSem1':
                for stud in StudentsList:
                    MD1 = stud.getMD1Percentage()
                    if MD1 <= int(query[5]) and  MD1 >= int(query[3]):
                        pass
                    else:
                        StudentsList = StudentsList.exclude(rollno=stud.rollno)
            elif query[7] == 'MidSem2':
                for stud in StudentsList:
                    MD2 = stud.getMD2Percentage()
                    if MD2 <= int(query[5]) and  MD2 >= int(query[3]):
                        pass
                    else:
                        StudentsList = StudentsList.exclude(rollno=stud.rollno)
            elif query[7] == 'Final':
                for stud in StudentsList:
                    ESM = stud.getESMPercentage()
                    if ESM <= int(query[5]) and  ESM >= int(query[3]):
                        pass
                    else:
                        StudentsList = StudentsList.exclude(rollno=stud.rollno)
            return StudentsList

def getTimeQuery(query, StudentsList):
    pass
