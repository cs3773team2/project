from django.shortcuts import *
from django.http import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
#from django.views.decorators.csrf import requires_csrf_token
from django.template import RequestContext
from .forms import LoginForm

def index(request):
    template = loader.get_template('EMIS/login.html')
    return HttpResponse(template.render(request))

def logout(request):
    template = loader.get_template('EMIS/logout.html')
    return HttpResponse(template.render(request))

@login_required()
def patient(request):
    template = loader.get_template('EMIS/patient.html')
    return HttpResponse(template.render(request))

@login_required()
def patPI(request):
    template = loader.get_template('EMIS/pat_pers-info.html')
    return HttpResponse(template.render(request))

@login_required()
def patIns(request):
    template = loader.get_template('EMIS/pat_ins-info.html')
    return HttpResponse(template.render(request))

#def login(request):
#    redirect_to = request.META.get('HTTP_REFERER', '/')
#    print("you suck")
#    if request.user.is_authenticated():
#        return HttpResponseRedirect(redirect_to)
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            user = form.cleaned_data['user']
#            password = form.cleaned_data['password']
#            user = authenticate(user=user, password=password)
#            if user is not None:
#                login(request, user)
#                return HttpResponseRedirect('/emis/patient.html')
#            else:
#                print("you suck")
#        else:
#            return HttpResponseRedirect(redirect_to)
#    else:
#        form = LoginForm()
#    return render_to_response('/', {'form': form}, context_instance=RequestContext(request))
