from django import forms
from .models import PersonalInfo


class LoginForm(forms.Form):
    user = forms.CharField(label='user', max_length=30)
    password = forms.CharField(label='password', widget=forms.PasswordInput(render_value=False), max_length=30)


class PersonalInfoForm(forms.Form):

    class Meta:
        model = PersonalInfo

        fields = '__all__'
