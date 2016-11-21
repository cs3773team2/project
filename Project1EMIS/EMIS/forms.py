from django.contrib.auth.forms import AuthenticationForm
from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(label='user', max_length=30)
    password = forms.CharField(label='password', widget=forms.PasswordInput(render_value=False), max_length=30)