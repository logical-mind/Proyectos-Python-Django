from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Foro, Respuesta, Voto, Cliente


class ForoForm(forms.ModelForm):
    class Meta:
        model = Foro
        fields = '__all__'

class CustomAuthenticationForm(AuthenticationForm):
    # Define tu propio formulario de inicio de sesión personalizado aquí
    class Meta:
        model = User  # Reemplaza 'User' con el modelo de usuario que estás utilizando
        fields = ['email', 'password']        

class RespuestaForm(forms.ModelForm):
    class Meta:
        model = Respuesta
        fields = '__all__'  

class VotoForm(forms.ModelForm):
    class Meta:
        model = Voto
        fields = '__all__'              


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')  
    class Meta:
        model= Cliente
        fields = ['username','email','password1','password2'] 


subscription_options = [
    ('1-month', '1-Month subscription ($10 USD/Mon)'),
    ('6-month', '6-Month subscription Save $10 ($50 USD/Mon)'),
    ('1-year', '1-Year subscription Save $30 ($90 USD/Mon)'),
]

class SubscriptionForm(forms.Form):
    plans = forms.ChoiceField(choices=subscription_options)


################################# RESET PASSWORD#######
