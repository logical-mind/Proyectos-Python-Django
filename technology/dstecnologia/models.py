
from django.contrib.auth.models import AbstractUser
from django.db import models


secciones = (
            ("A", "A"),
            ("B", "B"),
            ("C", "C"))

niveles = (
            ("Inicial", "Inicial"),
            ("Primaria", "Primaria"),
            ("Secundaria", "Secundaria"))

grados = (
            ("1th", "1th"),
            ("2th", "2th"),
            ("3th", "3th"),
            ("4th", "4th"),
            ("5th", "5th"),
            ("6th", "6th")
            ) 

sexo = (
   ("M", "Masculino"),
   ("F", "Femenino")
)  

notas = (
   ("Logrado", "Logrado"),
   ("En proceso", "En proceso"),
   ("Iniciado","Iniciado")
)   
      
class grado(models.Model):
   id = models.AutoField(primary_key=True)    
   nombre = models.CharField(max_length=100, choices=grados, default = "4th")
   seccion = models.CharField(max_length=100, choices=secciones, default = "A")
   nivel = models.CharField(max_length=100, choices=niveles, default = "Primaria") 

class estudiantes(AbstractUser):
 id = models.AutoField(primary_key=True)
 grado = models.CharField(max_length=100, choices=grados, default = "4th")
 seccion = models.CharField(max_length=100, choices=secciones, default = "A")
 nivel = models.CharField(max_length=100, choices=niveles, default = "Primaria") 
 sexo = models.CharField(max_length=100, choices=sexo, default = "F")

class calificacion(models.Model):
   id = models.AutoField(primary_key=True)    
   username = models.CharField(max_length=100)
   grado = models.CharField(max_length=100, choices=grados, default = "4th")
   seccion = models.CharField(max_length=100, choices=secciones, default = "A")
   nivel = models.CharField(max_length=100, choices=niveles, default = "Primaria")
   mes = models.CharField(max_length=100)
   semana = models.CharField(max_length=100)
   mes = models.CharField(max_length=100)
   nota = models.CharField(max_length=100, choices=notas, default = "Iniciado")
   meta = models.CharField(max_length=400, null=True)
   comentario = models.CharField(max_length=100)

  