from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import estudiantes, calificacion
from django.core.exceptions import ValidationError


class registerForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
     model = estudiantes
     fields = ["username", "email", "password1", "password2", "first_name", "last_name","grado","nivel","seccion","sexo","groups"]


class calificaciones(forms.ModelForm):  
    class Meta:
     model = calificacion
     fields = ["username", "nota", "meta", "comentario","grado","nivel","seccion","semana","mes"]

   
