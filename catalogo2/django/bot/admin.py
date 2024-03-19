from django.contrib import admin
from .models import Order, Foro, Respuesta, Voto, Cliente, Configuracion, Historial, Catalogo, Catalogo1, Catalogo2, Catalogo3, Catalogo4, Catalogo5, Catalogo6, Catalogo7, Catalogo8

admin.site.register(Order)
admin.site.register(Foro)
admin.site.register(Respuesta)
admin.site.register(Voto)
admin.site.register(Cliente)
admin.site.register(Configuracion)
admin.site.register(Historial)
admin.site.register(Catalogo)
admin.site.register(Catalogo1)
admin.site.register(Catalogo2)
admin.site.register(Catalogo3)
admin.site.register(Catalogo4)
admin.site.register(Catalogo5)
admin.site.register(Catalogo6)
admin.site.register(Catalogo7)
admin.site.register(Catalogo8)

admin.site.site_header = 'Catalobot'
admin.site.index_title = 'Panel de control de Catalobot'
admin.site.site_title = 'Catalobot'

