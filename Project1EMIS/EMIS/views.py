from django.shortcuts import *
from django.http import *
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from .forms import LoginForm

def index(request):
    template = loader.get_template('EMIS/index.html')
    return HttpResponse(template.render(request))

def patient(request):
    template = loader.get_template('EMIS/patient.html')
    return HttpResponse(template.render(request))

#def login(request):
#    #redirect_to = request.META.get('HTTP_REFERER', 'patient.html')
#    if request.user.is_authenticated():
#        return HttpResponseRedirect('/thanks/')
#    if request.method == 'POST':
#        form = LoginForm(request.POST)
#        if form.is_valid():
#            user = form.cleaned_data['user']
#            password = form.cleaned_data['password']
#            user = authenticate(user=user, password=password)
#            if user is not None:
#                login(request, user)
#                return HttpResponseRedirect('/thanks/')
#        else:
#            return HttpResponseRedirect('/bad/')
#    else:
#        form = LoginForm()
#    return render_to_response('/', {'form': form}, context_instance=RequestContext(request))
