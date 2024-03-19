from django.db import models
from django.contrib.auth.models import AbstractUser

sexo = (
   ("M", "Masculino"),
   ("F", "Femenino")
)  


voto = (
    ("si", "Sí"),
    ("no", "No")
)

nivel = (
    ("0", "N0"),
    ("1", "N1"),
    ("2", "N2"),
    ("3", "N3")   
)

zonas = ()


class Provincia(models.Model):
    nombre = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre

class Municipio(models.Model):
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey("Provincia", on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
class Circunscripcion(models.Model):
   nombre = models.CharField(max_length=100)
   municipio = models.ForeignKey("Municipio", on_delete=models.CASCADE)
   def __str__(self):
        return self.nombre    
    
class Sector(models.Model):
    nombre = models.CharField(max_length=100)
    circunscripcion = models.ForeignKey("Circunscripcion", on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre    
    
class Seccion(models.Model):
    nombre = models.CharField(max_length=100)
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    
 
class Recinto(models.Model):
    numero = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE, null=True)
    direccion = models.CharField(max_length=300)

    def __str__(self):
        return self.nombre       
    
class Colegio(models.Model):
    nombre = models.CharField(max_length=100)
    recinto = models.ForeignKey("Recinto", on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre    
    
    
class Ocupacion(models.Model):
    nombre = models.CharField(max_length=150)
    def __str__(self):
        return self.nombre      
    
 
class Votante(models.Model):
    id_coordinador = models.ForeignKey("Coordinador", on_delete=models.CASCADE,null=True, blank=True)
    id_votante = models.CharField(max_length=100,null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100) 
    cedula = models.CharField(max_length=13, unique=True )  
    fecha_nacimiento = models.DateField()  
    telefono = models.CharField(max_length=14) 
    circunscripcion = models.ForeignKey("Circunscripcion", on_delete=models.CASCADE) 
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE) 
    seccion = models.ForeignKey("Seccion", on_delete=models.CASCADE) 
    direccion = models.CharField(max_length=300)
    genero = models.CharField(choices=sexo, default='M',max_length=10)
    ocupacion = models.ForeignKey("Ocupacion", on_delete=models.CASCADE)
    Recinto = models.CharField(choices=voto, null=True, blank=True,max_length=10)
    voto = models.CharField(choices=voto, null=True, blank=True,max_length=10)


class Coordinador(AbstractUser):
    id_coordinador = models.ForeignKey("Coordinador", on_delete=models.CASCADE,null=True, blank=True) 
    nombre = models.CharField(max_length=100,null=True, blank=True)
    apellido = models.CharField(max_length=100,null=True, blank=True) 
    cedula = models.CharField(max_length=13, unique=True,null=True, blank=True)  
    fecha_nacimiento = models.DateField(null=True, blank=True)  
    telefono = models.CharField(max_length=14,null=True, blank=True) 
    circunscripcion = models.ForeignKey("Circunscripcion", on_delete=models.CASCADE,null=True, blank=True) 
    sector = models.ForeignKey("Sector", on_delete=models.CASCADE,null=True, blank=True) 
    seccion = models.ForeignKey("Seccion", on_delete=models.CASCADE,null=True, blank=True) 
    direccion = models.CharField(max_length=300,null=True, blank=True)
    genero = models.CharField(choices=sexo, default='M',max_length=10,null=True, blank=True)
    ocupacion = models.ForeignKey("Ocupacion", on_delete=models.CASCADE,null=True, blank=True)
    colegio = models.ForeignKey("Colegio", null=True, blank=True, on_delete=models.CASCADE)
    voto = models.CharField(choices=voto, null=True, blank=True,max_length=10)
    nivel = models.CharField(choices=nivel, null=True, blank=True,max_length=10)


   

   
   
