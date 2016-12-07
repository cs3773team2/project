from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save

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
    #user = models.OneToOneField(User, on_delete=models.CASCADE)
    mid_in = models.CharField(max_length=1, default='')
    dob = models.DateField(default='')
    age = models.IntegerField(default='')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='')
    address = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=20, default='')
    zip = models.IntegerField(default='')
    phone = models.IntegerField(default='')
#    objects = UserManager()


    # class Meta:
    #     db_table = u'PersonalInfo'

    #def __str__(self):
    #    return '%d %s' % (self.id, self.l_name)
