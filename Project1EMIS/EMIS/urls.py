from django.conf.urls import url
#from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient/$', views.patient, name='patient'),
    url(r'^pat_pers-info/$', views.patPI, name='patPI'),
    url(r'^pat_ins-info/$', views.patIns, name='patIns'),
    #url(r'^login/$', auth_views.login, {'template_name': 'EMIS/login.html'}, name='login'),
    #url(r'^login/$', views.login, {'template_name': 'EMIS/login.html'}, name='login'),
]