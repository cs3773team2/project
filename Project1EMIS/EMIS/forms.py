from django import forms

class LoginForm(forms.Form):
    user = forms.CharField(label='user', max_length=30)
    password = forms.CharField(label='password', widget=forms.PasswordInput(render_value=False), max_length=30)

class PersonalInfo(forms.Form):
    f_name = forms.CharField(max_length=20)
    l_name = forms.CharField(max_length=30)
    dob = forms.IntegerField()
    age = forms.IntegerField()
    address = forms.CharField(max_length=100)