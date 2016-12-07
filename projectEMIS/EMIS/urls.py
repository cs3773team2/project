from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.login, name='login'),
    url(r'^pat_pers-info/$', views.patPI, name='patPI'),
    url(r'^pat_ins-info/$', views.patIns, name='patIns'),
    url(r'^create_account/$', views.create_account, name='create_account'),
    url(r'^splash/$', views.splash, name='splash'),
    url(r'^logout_view/$', views.logout_view, name='logout_view'),
    url(r'^forgot_password/$', views.forgot_password, name='forgot_password_view'),
    url(r'^verify_password/$', views.verify_password, name='verify_password_view'),
    url(r'^auth/$', views.auth_view),
    url(r'^patient_home/$', views.patient_home, name='patient_home'),
    url(r'^doctor_home/$', views.doctor_home, name='doctor_home'),
    url(r'^cstaff_home/$', views.cstaff_home, name='cstaff_home'),
    url(r'^nurse_home/$', views.nurse_home, name='nurse_home'),
    url(r'^lab_home/$', views.lab_home, name='lab_home'),
    url(r'^pharmacy_home/$', views.pharmacy_home, name='pharmacy_home'),
    url(r'^insurance_home/$', views.insurance_home, name='insurance_home'),
    url(r'^user_not_auth/$', views.user_not_auth, name='user_not_auth'),
]
