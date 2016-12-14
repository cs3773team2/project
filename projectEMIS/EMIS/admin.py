from django.contrib import admin
from .models import *

admin.site.register(PersonalInfo)
admin.site.register(MedicalRecord)
admin.site.register(Event)