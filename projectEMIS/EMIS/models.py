from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    mid_in = models.CharField(max_length=1, default='')
    dob = models.DateField(blank=True, null=True)
    age = models.IntegerField(default=0)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='')
    address = models.CharField(max_length=50, default='')
    city = models.CharField(max_length=30, default='')
    state = models.CharField(max_length=20, default='')
    zip = models.IntegerField(default=0)
    phone = models.IntegerField(default=0)
    ins_name = models.CharField(max_length=30, default='')
    ins_mem_id = models.IntegerField(default=0)
    ins_grp_id = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        PersonalInfo.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.personalinfo.save()


class MedicalRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    date = models.DateTimeField(blank=True, null=True)
    height = models.CharField(max_length=10, default='')
    weight = models.CharField(max_length=10, default='')
    temp = models.CharField(max_length=10, default='')
    blood_pres = models.CharField(max_length=10, default='')
    heart_rate = models.CharField(max_length=10, default='')
    diag_code = models.CharField(max_length=10, default='')
    prescription = models.CharField(max_length=30, default='')
    lab_order = models.CharField(max_length=30, default='')
    notes = models.TextField(default='')
    #document = models.FileField(upload_to='uploads/')
    #image = models.ImageField(upload_to='uploads/')


class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    my_date = models.DateTimeField(blank=True, null=True)
    year = models.DateField(blank=True, null=True)
    month = models.DateField(blank=True, null=True)


