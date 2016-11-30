from django import forms
from .models import PersonalInfo
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)



from django.contrib.auth.forms import UserCreationForm
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

class auth_view(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))
    email = forms.CharField(label="email", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'password'}))

class PersonalInfoForm(forms.Form):
    class Meta:
        model = PersonalInfo

        fields = '__all__'

##checks if username exists
def username_present(username):
    if User.objects.filter(username=username).exists():
        return True
    return False

class UserForm(ModelForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))

    email = forms.CharField(label="Email", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))

    password = forms.CharField(validators=[
        DictionaryValidator(words=['banned_word'], threshold=0.9),
        LengthValidator(min_length=8),
        ComplexityValidator(complexities=dict( UPPER=1, LOWER=1, DIGITS=1)),])

    if username_present(username):
        raise forms.ValidationError(_("The username already exists."))

    class Meta:
        model = User
        fields = ('username', 'email','password')

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
           user.save()
        return user


'''
class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat your password")
    email = forms.EmailField()
    email2 = forms.EmailField(label="Repeat your email")
    ##create new model using data?

    def clean_email(self):
        if self.data['email'] != self.data['email2']:
            raise forms.ValidationError('Emails are not the same')
        return self.data['email']

    def clean_password(self):
        if self.data['password'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password']

    def clean(self, *args, **kwargs):
        self.clean_email()
        self.clean_password()
        return super(SignupForm, self).clean(*args, **kwargs)
'''