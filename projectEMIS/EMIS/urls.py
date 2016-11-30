from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   # url(r'^$', views.index, name='index'),
    url(r'^$', views.login, name='login'),
  #  url(r'^patient', views.patient, name='patient'),
    url(r'^pat_pers-info/$', views.patPI, name='patPI'),
    url(r'^pat_ins-info/$', views.patIns, name='patIns'),
    url(r'^createAccount/$', views.createAccount, name='createAccount'),
    url(r'^splash/$', views.splash, name='splash'),


]