from django.contrib.auth.models import User
from EMIS.forms import *
from django.shortcuts import *
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from EMIS import *

def index(request):
    if not request.user.is_authenticated():
        return redirect('/login/')
    else:
        template = loader.get_template('EMIS/home.html')
        return HttpResponse(template.render(request))

def login(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('username', None)
        template = loader.get_template('EMIS/splash.html')
    return HttpResponseRedirect('/login/')

def splash(request):
    template = loader.get_template('EMIS/splash.html')
    return HttpResponse(template.render(request))

def logout(request):
    template = loader.get_template('EMIS/logout.html')
    return HttpResponse(template.render(request))

@login_required(login_url='/') #if not logged in redirect to /
def home(request):
    return render(request, 'home.html')


@login_required()
def patient(request):
    template = loader.get_template('EMIS/patient.html')
    #context = {'pat_name': request.s}
    return HttpResponse(template.render(request))

@login_required()
def patPI(request):
    template = loader.get_template('EMIS/pat_pers-info.html')
    return HttpResponse(template.render(request))

@login_required()
def patIns(request):
    template = loader.get_template('EMIS/pat_ins-info.html')
    return HttpResponse(template.render(request))


def auth_view(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    user = authenticate(username = username, password = password)

    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect('/')

def logout_view(request):
     logout(request)
    # Redirect to a success page.

def createAccount(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        username = request.POST.get('username', None)
        email = request.POST.get('email', None)
        password = request.POST.get('username', None)
        if form.is_valid():
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)  # This line will hash the password
                user.save()  # DO NOT FORGET THIS LINE
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(user)
                    return HttpResponseRedirect('/splash/')
                # No backend authenticated the credentials
               # login(user)
                return HttpResponseRedirect('/login/')

            #login(user)
            # redirect, or however you want to get to the main view
            #return HttpResponseRedirect('/login/')
    else:
        form = UserForm()
    return render(request, 'home.html', {'form': form})

#def createAccount(request):
#    template = loader.get_template('EMIS/createAccount.html')
#    return HttpResponse(template.render(request))