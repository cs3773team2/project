from django.db import models
from django.contrib.auth.models import User

SEX_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)


class EMISUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_attempts = models.IntegerField(default=0)
    locked_out = models.BooleanField(default=False)
    unlock_code = models.CharField(max_length=36, default='')


class PersonalInfo(models.Model):
    f_name = models.CharField(max_length=20, null=True)
    l_name = models.CharField(max_length=30, null=True)
    mid_in = models.CharField(max_length=1, null=True)
    dob = models.DateField(null=True)
    age = models.IntegerField(null=True)
    sex = models.CharField(max_length=1, null=True, choices=SEX_CHOICES)
    address = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=20, null=True)
    zip = models.IntegerField(null=True)
    phone = models.IntegerField(null=True)

    # class Meta:
    #     db_table = u'PersonalInfo'

    #def __str__(self):
    #    return '%d %s' % (self.id, self.l_name)
