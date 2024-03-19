from django import forms
from .models import Votante,Coordinador
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):

    class Meta:
        model= Coordinador
        fields = '__all__' 

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Votante
        fields = '__all__'


    