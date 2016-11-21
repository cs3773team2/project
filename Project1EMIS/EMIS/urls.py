from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^patient/$', views.patient, name='patient'),
    #url(r'^login/$', views.login, {'template_name': 'EMIS/index.html'}, name='login'),
]