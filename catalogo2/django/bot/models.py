from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.utils import timezone


martingala = (
    ("0", "0 Mg"),
    ("1", "1 Mg"),
    ("2", "2 Mg"),
    ("3", "3 Mg"),   
    ("4", "4 Mg"), 
    ("5", "5 Mg") 
)

tipo_martingala = (
    ("double", "Double"),
    ("single", "Single")  
)

modo_entrada = (
    ("vela2", "Vela 2"),
    ("vela3", "Vela 3"), 
    ("vela4", "Vela 4"),
    ("vela5", "Vela 5")
)

after_loss = (
    ("1", "1"),
    ("2", "2"), 
)

after_loss_martingala = (
    ("0", "0 Mg"),
    ("1", "1 Mg"),
    ("2", "2 Mg"),
    ("3", "3 Mg"),   
    ("4", "4 Mg")
)

class Cliente(AbstractUser):
    server = models.CharField(max_length=100, blank=True, null=True)  
    plan = models.CharField(max_length=100, blank=True, null=True) 
    plan_id = models.CharField(max_length=100, blank=True, null=True) 
    user = models.CharField(max_length=255, blank=True, null=True)
    email_iq = models.CharField(max_length=255, blank=True, null=True)
    password_iq = models.CharField(max_length=255, blank=True, null=True)
    iq_option_instance = models.TextField(null=True, blank=True)
    count = models.PositiveIntegerField(default=0)

    def get_active_sessions_count(self):
        # Obtén las sesiones activas para el cliente
        active_sessions = Session.objects.filter(
            expire_date__gte=timezone.now(),
            session_key__in=self.session_set.values_list('session_key', flat=True)
        )

        # Cuenta las sesiones activas
        active_sessions_count = active_sessions.count()

        return active_sessions_count

class Order(models.Model):
    order_id = models.CharField(max_length=100, null= True)
    name = models.CharField(max_length=191)
    email = models.EmailField()
    postal_code = models.IntegerField()
    address = models.CharField(max_length=191)
    date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

class Foro(models.Model):
    username = models.CharField(max_length=100, null= True, blank=True)
    titulo = models.CharField(max_length=500, null= True) 
    nombre = models.CharField(max_length=40, null=True) 
    estado = models.CharField(max_length=40, null=True, blank=True) 
    mensaje= models.TextField (null= True)
    fecha = models.DateField(null=True, blank=True)   
    enlace = models.ForeignKey("Foro", on_delete=models.CASCADE, null=True, blank=True)
    importe = models.CharField(max_length=10, null= True, blank=True) 
    martingala = models.CharField(choices=martingala, null=True, max_length=10, blank=True)
    tipo_martingala = models.CharField(choices=tipo_martingala, null=True, max_length=10, blank=True)
    num_operaciones = models.IntegerField(null=True, blank=True)
    modo_entrada = models.CharField(choices=modo_entrada, null=True, max_length=10, blank=True)
    after_loss = models.CharField(choices=after_loss, null=True, max_length=10, blank=True)
    after_loss_num = models.IntegerField(null=True, blank=True)
    after_loss_martingala = models.CharField(choices=after_loss_martingala, null=True, max_length=10, blank=True)
    stop_gain = models.IntegerField(null=True, blank=True)
    stop_loss = models.IntegerField(null=True, blank=True)
    voto = models.IntegerField(null=True, blank=True)

 
class Respuesta(models.Model):
    foro_id = models.CharField(max_length=100, null= True, blank=True)
    username = models.CharField(max_length=100, null= True, blank=True)
    mensaje= models.TextField (null= True)

class Voto(models.Model):
    foro_id = models.CharField(max_length=100, null= True, blank=True)
    username = models.CharField(max_length=100, null= True, blank=True)
       

class Configuracion(models.Model):
    user = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    datos = models.JSONField(null= True, blank=True)
    martingala = models.CharField(max_length=100, null= True, blank=True)
    cuadrante = models.CharField(max_length=100, null= True, blank=True)
    destino = models.CharField(max_length=100, null= True, blank=True)
    tipo_mercado = models.CharField(max_length=100, null= True, blank=True)
    porcentaje = models.JSONField(null= True, blank=True)
    


class Historial(models.Model):
    user = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    divisa = models.CharField(max_length=100, blank=True, null=True)
    ganancia = models.CharField(max_length=100, blank=True, null=True)
    martingala = models.CharField(max_length=100, blank=True, null=True) 
    estado = models.CharField(max_length=100, blank=True, null=True) 
    modo = models.CharField(max_length=100, blank=True, null=True)
    estrategia = models.CharField(max_length=100, blank=True, null=True)   
    fecha = models.DateTimeField(blank=True, null=True)

class Catalogo(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True) 
    lista = models.JSONField(null= True, blank=True)

class Catalogo1(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo2(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo3(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo4(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo5(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo6(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True) 

class Catalogo7(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Catalogo8(models.Model):
    mercado = models.JSONField(null= True, blank=True)
    mercado_otc = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)       

class Indicador(models.Model):
    indicadores = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
    pase = models.CharField(max_length=100, blank=True, null=True)

class Senal(models.Model):
    senales = models.JSONField(null= True, blank=True)
    fecha_y_hora = models.DateTimeField(auto_now=False, auto_now_add=False,blank=True, null=True)
     
