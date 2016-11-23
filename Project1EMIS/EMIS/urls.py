from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient', views.patient, name='patient'),
    url(r'^pat_pers-info/$', views.patPI, name='patPI'),
    url(r'^pat_ins-info/$', views.patIns, name='patIns'),
]