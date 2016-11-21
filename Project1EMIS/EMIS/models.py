from django.db import models

class PersonalInfo(models.Model):
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=30)
    dob = models.IntegerField()
    age = models.IntegerField()
    address = models.CharField(max_length=100)
