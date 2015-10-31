from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.shortcuts import render_to_response
from django.db import connection
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.views import logout
from django.shortcuts import render
from django.template import RequestContext, loader
from adminStaff.models import AdminStaff, AttendanceDaily
from portal.models import Course, Feedback, Notification
from Students.models import Student

# Create your views here.

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
               #if user.is_active:
                login(request, user)
                redirect_link = check_redirect(request,user)  
                return HttpResponseRedirect(redirect_link)
#               else:
#                return HttpResponse("Your account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details: {0}, {1}".format(username, password))
    else:
        return render_to_response('portal/login.html', {}, context)


def checkIdentity(request, type_of_user):
    logged_in = 'username' in request.session
    if logged_in is False:
        redirect = '/'
    else:
        identity = request.session[type_of_user]
        if identity is True:
            redirect = ""
        elif identity is False:
            redirect = ('/portal/access_denied')
        # return dfasd
    return redirect

def search(request,many):
    query = "SELECT name,rollno,id FROM Students_student WHERE "
    for word in many:
        query += "rollno LIKE \'%" + word + "%\' OR name LIKE \'%" + word + "%\' OR "
    query += " name = \'" + many[0] + "\'"
    row =  Student.objects.raw(query)
    return row,query

def portalSearchResults(request,template,app,currentUserObject):
    template = loader.get_template(template)
    current = currentUserObject
    if request.method == 'POST':
        search_input = request.POST['search_input']
        if search_input != "":
            many = search_input.split()
            (ListofStudents,query) = search(request,many)
        else:
            ListofStudents = ""
        context = RequestContext(request, {'app':app,'current': current, 'ListofStudents': ListofStudents, 'search_input': search_input})
    else:
        context = RequestContext(request, {'current': current,})
    return HttpResponse(template.render(context))

def logout_view(request):
    logout(request)
    template = loader.get_template('portal/logout.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def access_denied(request):
    template = loader.get_template('portal/access_denied.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))

def check_redirect(request,user):
    request.session['username'] = user.email
    request.session['student'] = user.is_student
    request.session['parent'] = user.is_parent
    request.session['adminstaff'] = user.is_adminstaff
    request.session['faculty'] = user.is_faculty
    request.session['facultystaff'] = user.is_facultystaff
    request.session['ta'] = user.is_ta
    redirect = 'portal/login.html'
    if user.email.find("@students.iiit.ac.in") != -1 or user.email.find("@research.iiit.ac.in") != -1:
        if request.session['student']:
            redirect = '/student/'
        else:
            redirect = '/portal/access_denied/'
    elif user.email.find("@faculty.iiit.ac.in") != -1:
        if request.session['faculty']:
            redirect = '/faculty/'
        elif request.session['facultystaff']:
            redirect = '/facultystaff/'
        elif request.session['adminstaff']:
            redirect = '/adminStaff/'
        else:
            redirect = '/portal/access_denied/'
    elif user.email.find("@iiit.ac.in") != -1:
        if request.session['adminstaff']:
            redirect = '/adminStaff/'
        else:
            redirect = '/portal/access_denied/'
    elif user.email.find("@parents.iiit.ac.in") != -1:
        if request.session['parent']:
            redirect = '/parents/'
        else:
            redirect = '/portal/access_denied/'
    return redirect
