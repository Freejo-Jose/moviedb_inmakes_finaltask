from django import forms
from .models import Movie,Category
from django.contrib.auth.models import User

class Movieform(forms.ModelForm):
    class Meta:
        model=Movie
        fields=['name','desc','pict','actors','utubelink','category','released']

class Categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields=['name','desc','pict']

class Userform(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','first_name','last_name']