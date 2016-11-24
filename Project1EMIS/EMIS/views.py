from django.shortcuts import *
from django.http import *
from django.contrib.auth.decorators import login_required

def index(request):
    template = loader.get_template('EMIS/login.html')
    return HttpResponse(template.render(request))

def logout(request):
    template = loader.get_template('EMIS/logout.html')
    return HttpResponse(template.render(request))

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
