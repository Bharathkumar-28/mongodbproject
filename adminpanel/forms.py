
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate


class registerform(forms.ModelForm):
    username=forms.CharField(label='username',max_length=100,required=True)
    email=forms.CharField(label='email',max_length=100,required=True)
    password=forms.CharField(label='password',max_length=100,required=True)
    password_confirm=forms.CharField(label='password_confirm',max_length=100,required=True)

    class Meta:
        model=User
        fields=['username','email','password']
    def clean(self):
        cleaneddata=super().clean()  
        password=cleaneddata.get('password')
        password_confirm=cleaneddata.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('password do not match')
from django import forms
from pymongo import MongoClient
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

from django import forms
from pymongo import MongoClient
from django.contrib.auth.hashers import check_password  # Use Django's password hashers

# forms.py
from django import forms

class loginform(forms.Form):
    username = forms.CharField(label="Username", max_length=100, required=True)
    password = forms.CharField(label="Password", max_length=100, required=True)
from django import forms

class ResumeForm(forms.Form):
    name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone = forms.CharField(label='Phone Number', max_length=20)
    skills = forms.CharField(widget=forms.Textarea, label='Skills')
    experience = forms.CharField(widget=forms.Textarea, label='Experience')
    internships = forms.CharField(widget=forms.Textarea, label='Internships', required=False)
