from django import forms
from .models import PersonalInfo, EMISUser
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelForm
from django.contrib.auth.models import User

from passwords.validators import (
    DictionaryValidator, LengthValidator, ComplexityValidator)


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
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
        #fields = ('username', 'email', 'password')
        fields = '__all__'

    # def save(self, commit=True):
    #     user = super(UserForm, self).save(commit=False)
    #     user.email = self.cleaned_data["email"]
    #     if commit:
    #         user.save()
    #         EMISUser.objects.create(user=user)
    #     return user
