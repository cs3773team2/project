from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.core.mail import send_mail

from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))


class ExtendUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ('mid_in','dob','age','sex',
                  'address','city','state','zip','phone')
        labels = {
            'mid_in': 'Middle Initial',
            'dob': 'Date of Birth',
            'age': 'Age',
            'sex': 'Gender',
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zip': 'Zip Code',
            'phone': 'Phone',
        }


class InsInfoForm(forms.ModelForm):
    class Meta:
        model = PersonalInfo
        fields = ('ins_name','ins_mem_id','ins_grp_id')
        labels = {
            'ins_name': 'Insurance Name',
            'ins_mem_id': 'Member ID',
            'ins_grp_id': 'Group ID',
        }


class MedRecForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('date','height', 'weight', 'temp','blood_pres',
                  'heart_rate','diag_code','prescription',
                  'lab_order','notes')
        labels = {
            'date': 'Date of Service',
            'height': 'Height',
            'weight': 'Weight',
            'temp': 'Temperature',
            'blood_pres': 'Blood Pressure',
            'heart_rate': 'Heart Rate',
            'diag_code': 'Diag Code',
            'prescription': 'Prescription',
            'lab_order': 'Lab Order',
            'notes': 'Notes',
        }


class AddMedRecForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ('date', 'notes')
        labels = {
            'date': 'Date of Service',
            'notes': 'Description',
        }


class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s, %s" % (obj.last_name, obj.first_name)


class docAddMedRecForm(forms.ModelForm):
    patient = CustomModelChoiceField(queryset=User.objects.exclude(username='admin'))

    class Meta:
        model = MedicalRecord
        fields = ('patient','date', 'height', 'weight', 'temp', 'blood_pres',
                  'heart_rate', 'diag_code', 'prescription',
                  'lab_order', 'notes')
        labels = {
            'patient': 'Patient',
            'date': 'Date of Service',
            'height': 'Height',
            'weight': 'Weight',
            'temp': 'Temperature',
            'blood_pres': 'Blood Pressure',
            'heart_rate': 'Heart Rate',
            'diag_code': 'Diag Code',
            'prescription': 'Prescription',
            'lab_order': 'Lab Order',
            'notes': 'Notes',
        }

class docAddEvent(forms.ModelForm):
    patient = CustomModelChoiceField(queryset=User.objects.exclude(username='admin'))

    class Meta:
        model = Event
        fields = ('patient', 'my_date')
        labels = {
            'patient': 'Patient',
            'my_date': 'Add Appointment',
        }


##checks if username exists
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


class UserForm(ModelForm):
    """
    Used to create accounts.  Not used to login
    """
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))

#    if username_present(username): # Comment this out when running python manage.py makemigrations or migrate
#        raise forms.ValidationError("The username already exists.")

    email = forms.CharField(label="Email", max_length=30,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))

    password = forms.CharField(validators=[
        DictionaryValidator(words=['banned_word'], threshold=0.9),
        LengthValidator(min_length=8),
        ComplexityValidator(complexities=dict(UPPER=1, LOWER=1, DIGITS=1)), ])

    # email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    # def save(self, commit=True):
    #     user = super(UserForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #         EMISUser.objects.create(user=user)
    #     return user


class ContactForm(forms.Form):
    """
    Used for contact.html email sending.
    """
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Contact name:"
        self.fields['contact_email'].label = "Contact email:"
        self.fields['content'].label = "Email body:"


class ScheduleAppointmentForm(forms.Form):
    """
    Used for contact.html email sending.
    """
    contact_name = forms.CharField(required=True)
    # contact_email = forms.EmailField(required=True)
    date = forms.DateTimeField(required=True)
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
    )

    def __init__(self, *args, **kwargs):
        super(ScheduleAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        # self.fields['contact_email'].label = "Contact email:"
        self.fields['date'].label = "Appointment Date/Time"
        self.fields['content'].label = "Appointment Details"