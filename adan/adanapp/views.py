from django.shortcuts import render, redirect
from .forms import PostForm
from django.forms import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .forms import RegisterForm

import json
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from adanapp.models import Votante, Seccion, Sector, Circunscripcion, Ocupacion, Coordinador




def index(request):
    return render(request, 'index.html')

@login_required
def unete(request):
    return render(request, 'dashboard.html')

@csrf_exempt
def secciones(request):

     filtros2 = request.body
     filtros = json.loads(filtros2)  
     secciones_json = {}
     lista_sectores= []
     
     lista_circunscripcion = filtros['circunscripcion']
     lista_sector = filtros['sector']

     if len(lista_circunscripcion) > 0:
           circunscripciones= Circunscripcion.objects.all()
           circunscripciones_json = list(circunscripciones.values('nombre')) 

           sectores= Sector.objects.filter(circunscripcion__nombre__in=lista_circunscripcion)
           sectores_json = list(sectores.values('nombre'))
           
           for x in sectores_json:
                lista_sectores.append(x['nombre'])
             
           secciones = Seccion.objects.filter(sector__nombre__in=lista_sectores) 
           secciones_json = list(secciones.values('nombre')) 

     else:  
           circunscripciones= Circunscripcion.objects.all()
           circunscripciones_json = list(circunscripciones.values('nombre')) 
           sectores= Sector.objects.all()
           sectores_json = list(sectores.values('nombre'))     
           secciones = Seccion.objects.all()
           secciones_json = list(secciones.values()) 

     if len(lista_sector) > 0:
      secciones = Seccion.objects.filter(sector__nombre__in=lista_sector) 
      secciones_json = list(secciones.values('nombre')) 

    
     return JsonResponse({"circunscripcion":circunscripciones_json,"sector":sectores_json,"seccion":secciones_json}, safe=False)


@csrf_exempt
def secciones_form(request):
     filtros2 = request.body
     filtros = json.loads(filtros2)  
     secciones_json = {}
     lista_sectores= []
     
     lista_circunscripcion = filtros['circunscripcion']
     lista_sector = filtros['sector']

     if lista_circunscripcion != None:
           circunscripciones= Circunscripcion.objects.all()
           circunscripciones_json = list(circunscripciones.values('nombre')) 
           circunscripcionesid_json = list(circunscripciones.values('id')) 

           sectores= Sector.objects.filter(circunscripcion__id=lista_circunscripcion)
           sectores_json = list(sectores.values('nombre'))
           sectoresid_json = list(sectores.values('id'))
         
           
           for x in sectores_json:
                lista_sectores.append(x['nombre'])     
             
           secciones = Seccion.objects.filter(sector__nombre__in=lista_sectores) 
           secciones_json = list(secciones.values('nombre')) 
           seccionesid_json = list(secciones.values('id')) 
           
     else:  
           circunscripciones= Circunscripcion.objects.all()
           circunscripciones_json = list(circunscripciones.values('nombre')) 
           circunscripcionesid_json = list(circunscripciones.values('id')) 

           sectores= Sector.objects.all()
           sectores_json = list(sectores.values('nombre')) 
           sectoresid_json = list(sectores.values('id'))

           secciones = Seccion.objects.all()
           secciones_json = list(secciones.values()) 
           seccionesid_json = list(secciones.values('id')) 


     if lista_sector != None:
        secciones = Seccion.objects.filter(sector__id=lista_sector) 
        secciones_json = list(secciones.values('nombre')) 
        seccionesid_json = list(secciones.values('id')) 
    
     return JsonResponse({"circunscripcion":circunscripciones_json,"circunscripcionid":circunscripcionesid_json,"sector":sectores_json,"sectorid":sectoresid_json,"seccion":secciones_json,"seccionid":seccionesid_json}, safe=False)


@csrf_exempt
def post_create(request):
        fecha = request.POST['fecha_nacimiento']
        anual = fecha[-4:]
        mes = fecha[15:17]
        dia = fecha[5:7]
        fecha = anual+"-"+mes+"-"+dia
        request.POST._mutable = True
        request.POST['fecha_nacimiento'] = fecha
        request.POST['id_coordinador'] = request.user.id
        request.POST._mutable = False
        
        id_votante = request.POST['id_votante']
        if id_votante == "":
          form = PostForm(request.POST or None) 
        else:     
          p = Votante.objects.get(pk=id_votante)
          form = PostForm(request.POST,instance=p)
        print(form)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            # converts Post instance to dictionary so JsonResponse can serialize it to Json
            return JsonResponse(model_to_dict(instance, fields=['nombre','id_votante']), status=201)
        else:
            print(form)
            return JsonResponse(form.errors, safe=False, status=200)
        

@csrf_exempt    
def eliminar(request):    
    id_2 = request.body
    id_0 = json.loads(id_2)  
    try:
       p = Votante.objects.get(pk=id_0['id_votante'])
       p.delete()
       estado = 'eliminado'
    except: estado = 'error'   
    return JsonResponse({'estado':estado}, safe=False)

def total_votantes(request):
       lista = []
       lista.append(request.user.id)

       lista_2 = Coordinador.objects.filter(id_coordinador=request.user.id)
       lista_1 = serializers.serialize("json",lista_2)
       lista_ = json.loads(lista_1)
       for i in lista_:
           lista.append(i['pk'])
           
           lista__2 = Coordinador.objects.filter(id_coordinador=i['pk'])
           lista__1 = serializers.serialize("json",lista__2)
           lista__ = json.loads(lista__1)
           for x in lista__:
                lista.append(x['pk'])
           
                lista___2 = Coordinador.objects.filter(id_coordinador=x['pk'])
                lista___1 = serializers.serialize("json",lista___2)
                lista___ = json.loads(lista___1)
                for y in lista___:
                    lista.append(y['pk'])
            
   
       data3 = Votante.objects.filter(id_coordinador__in=lista)
       data2 = serializers.serialize("json",data3)
       data = json.loads(data2)
       return data

@csrf_exempt    
def table(request):
       data = total_votantes(request)

       for i in data:
            cir_nombre3 = Circunscripcion.objects.filter(id=i['fields']['circunscripcion'])
            cir_nombre2 = serializers.serialize("json",cir_nombre3)
            cir_nombre = json.loads(cir_nombre2)
            i['fields']['circunscripcion_nombre'] =  cir_nombre[0]['fields']['nombre']

            sector_nombre3 = Sector.objects.filter(id=i['fields']['sector'])
            sector_nombre2 = serializers.serialize("json",sector_nombre3)
            sector_nombre = json.loads(sector_nombre2)
            i['fields']['sector_nombre'] =  sector_nombre[0]['fields']['nombre']

            seccion_nombre3 = Seccion.objects.filter(id=i['fields']['seccion'])
            seccion_nombre2 = serializers.serialize("json",seccion_nombre3)
            seccion_nombre = json.loads(seccion_nombre2)
            i['fields']['seccion_nombre'] =  seccion_nombre[0]['fields']['nombre']

            ocu_nombre3 = Ocupacion.objects.filter(id=i['fields']['ocupacion'])
            ocu_nombre2 = serializers.serialize("json",ocu_nombre3)
            ocu_nombre = json.loads(ocu_nombre2)
            i['fields']['ocupacion_nombre'] =  ocu_nombre[0]['fields']['nombre']

            coord_nombre3 = Coordinador.objects.filter(id=i['fields']['id_coordinador'])
            coord_nombre2 = serializers.serialize("json",coord_nombre3)
            coord_nombre = json.loads(coord_nombre2)
            i['fields']['coord_username'] =  coord_nombre[0]['fields']['username']

            fecha = i['fields']['fecha_nacimiento']
            dia = fecha[-2:]
            mes = fecha[5:7]
            anual = fecha[0:4]
            edad = relativedelta(datetime.now(), datetime(int(anual), int(mes), int(dia)))
            i['fields']['edad'] =  str(edad.years)
              
       return JsonResponse({"user":data})

def coordinadores(request):
    
    def meta (n):  
        metas = 40 
        if n == '0': metas = 5000
        if n == '1': metas = 1000
        if n == '2': metas = 200
        if n == '3': metas = 40
       
        return metas
    
    total_final = 0
    coordinadores2 =  Coordinador.objects.filter(id_coordinador=request.user.id)
    coordinadores1 = serializers.serialize("json",coordinadores2)
    coordinadores = json.loads(coordinadores1)
    me2 =  Coordinador.objects.filter(id=request.user.id)
    me1 = serializers.serialize("json",me2)
    me = json.loads(me1)
    total = Votante.objects.filter(id_coordinador=request.user.id)
    for i in me:
        i['fields']['total'] = len(total)
        total_final = total_final + len(total)

    for i in coordinadores:
        total_final_n1 = 0
        total = Votante.objects.filter(id_coordinador=i['pk'])
        i['fields']['total'] = len(total)
        i['fields']['meta'] = meta(i['fields']['nivel'])

        total_final_n1 = total_final_n1 + len(total)
        i['fields']['total_final_n1'] = total_final_n1
        i['fields']['total_porciento_n1'] = int(((total_final_n1 * 100) / meta(i['fields']['nivel'])))

        total_final = total_final + len(total)

        coord2 =  Coordinador.objects.filter(id_coordinador=i['pk'])
        coord1 = serializers.serialize("json",coord2)
        coord = json.loads(coord1)
        i['fields']['nivel2'] = coord

        for x in coord:
            total_final_n2 = 0
            total = Votante.objects.filter(id_coordinador=x['pk'])
            x['fields']['total'] = len(total)
            total_final_n1 = total_final_n1 + len(total)
            i['fields']['total_final_n1'] = total_final_n1
            i['fields']['total_porciento_n1'] = int(((total_final_n1 * 100) / meta(i['fields']['nivel'])))
            total_final = total_final + len(total)

            total_final_n2 = total_final_n2 + len(total)
            x['fields']['total_final_n2'] = total_final_n2
            x['fields']['total_porciento_n2'] = int(((total_final_n2 * 100) /meta(x['fields']['nivel'])))
            x['fields']['meta'] = meta(x['fields']['nivel'])

            coord_2 =  Coordinador.objects.filter(id_coordinador=x['pk'])
            coord_1 = serializers.serialize("json",coord_2)
            coord_ = json.loads(coord_1)
            x['fields']['nivel3'] = coord_

            for y in coord_:
                total = Votante.objects.filter(id_coordinador=y['pk'])
                y['fields']['total'] = len(total)
                y['fields']['porciento'] = int(((len(total) * 100) / meta(y['fields']['nivel'])))
                y['fields']['meta'] = meta(y['fields']['nivel'])

                total_final_n1 = total_final_n1 + len(total)
                i['fields']['total_final_n1'] = total_final_n1
                i['fields']['total_porciento_n1'] = int(((total_final_n1 * 100) / meta(i['fields']['nivel'])))

                total_final_n2 = total_final_n2 + len(total)
                x['fields']['total_final_n2'] = total_final_n2
                x['fields']['total_porciento_n2'] = int(((total_final_n2 * 100) / meta(x['fields']['nivel'])))

                total_final = total_final + len(total)

    masculino = 0
    femenino = 0
    jovenes = 0
    adultos = 0
    mayores = 0
    m_joven = 0
    f_joven = 0
    m_adulto = 0
    f_adulto = 0
    m_mayor = 0 
    f_mayor = 0
    c1 = 0
    c2 = 0
    c3 = 0
    a1= 0 
    a2= 0 
    a3 = 0 
    a4 = 0 
    a5 = 0 
    a6 = 0 
    a7 = 0 
    a8 = 0 
    a9 = 0 
    a10 = 0 
    a11 = 0 
    a12 = 0 
    a13 = 0 
    a14 = 0 
    a15 = 0 
    a16= 0 
    a17 = 0 
    a18 = 0 
    a19= 0 
    a20 = 0 
    a21 = 0 
    a22 = 0 
    a23 = 0 

    fecha_actual = datetime.now()
    data = total_votantes(request)
    for i in data:
        if i['fields']['genero'] == 'M': masculino = masculino + 1
        if i['fields']['genero'] == 'F': femenino = femenino + 1
            
        fecha = i['fields']['fecha_nacimiento']
        dia = fecha[-2:]
        mes = fecha[5:7]
        anual = fecha[0:4]
        edad = relativedelta(fecha_actual, datetime(int(anual), int(mes), int(dia)))

        if edad.years <= 35:
            jovenes = jovenes + 1
            if i['fields']['genero'] == 'M': m_joven =  m_joven + 1
            if i['fields']['genero'] == 'F': f_joven = f_joven + 1
        if edad.years >= 36 and edad.years <= 60: 
            adultos = adultos + 1
            if i['fields']['genero'] == 'M': m_adulto =  m_adulto + 1
            if i['fields']['genero'] == 'F': f_adulto = f_adulto + 1
        if edad .years>= 61: 
            mayores = mayores + 1
            if i['fields']['genero'] == 'M': m_mayor =  m_mayor + 1
            if i['fields']['genero'] == 'F': f_mayor = f_mayor + 1
         
        if i['fields']['circunscripcion'] == 1: c1 = c1 + 1
        if i['fields']['circunscripcion'] == 2: c2 = c2 + 1 
        if i['fields']['circunscripcion'] == 3: c3 = c3 + 1 
   ######################grafico sector #############################
           
        if i['fields']['sector'] == 1: a1 = a1 + 1
        if i['fields']['sector'] == 2: a2 = a2 + 1
        if i['fields']['sector'] == 3: a3 = a3 + 1
        if i['fields']['sector'] == 4: a4 = a4 + 1
        if i['fields']['sector'] == 5: a5 = a5 + 1
        if i['fields']['sector'] == 6: a6 = a6 + 1
        if i['fields']['sector'] == 7: a7 = a7 + 1
        if i['fields']['sector'] == 8: a8 = a8 + 1
        if i['fields']['sector'] == 9: a9 = a9 + 1
        if i['fields']['sector'] == 10: a10 = a10 + 1
        if i['fields']['sector'] == 11: a11 = a11 + 1
        if i['fields']['sector'] == 12: a12 = a12 + 1
        if i['fields']['sector'] == 13: a13 = a13 + 1
        if i['fields']['sector'] == 14: a14 = a14 + 1
        if i['fields']['sector'] == 15: a15 = a15 + 1
        if i['fields']['sector'] == 16: a16 = a16 + 1
        if i['fields']['sector'] == 17: a17 = a17 + 1
        if i['fields']['sector'] == 18: a18 = a18 + 1
        if i['fields']['sector'] == 19: a19 = a19 + 1
        if i['fields']['sector'] == 20: a20 = a20 + 1
        if i['fields']['sector'] == 21: a21 = a21 + 1
        if i['fields']['sector'] == 22: a22 = a22 + 1
        if i['fields']['sector'] == 23: a23 = a23 + 1

    for i in me:
        
            i['fields']['total_final'] = total_final
           
            i['fields']['meta'] =  meta(request.user.nivel)

            i['fields']['masculino'] =  masculino
            i['fields']['femenino'] =  femenino

            i['fields']['c1'] =  c1
            i['fields']['c2'] =  c2
            i['fields']['c3'] =  c3
            i['fields']['a1'] =  a1
            i['fields']['a2'] =  a2
            i['fields']['a3'] =  a3
            i['fields']['a4'] =  a4
            i['fields']['a5'] =  a5
            i['fields']['a6'] =  a6
            i['fields']['a7'] =  a7
            i['fields']['a8'] =  a8
            i['fields']['a9'] =  a9
            i['fields']['a10'] =  a10
            i['fields']['a11'] =  a11
            i['fields']['a12'] =  a12
            i['fields']['a13'] =  a13
            i['fields']['a14'] =  a14
            i['fields']['a15'] =  a15
            i['fields']['a16'] =  a16
            i['fields']['a17'] =  a17
            i['fields']['a18'] =  a18
            i['fields']['a19'] =  a19
            i['fields']['a20'] =  a20
            i['fields']['a21'] =  a21
            i['fields']['a22'] =  a22
            i['fields']['a23'] =  a23
            
            i['fields']['jovenes'] =  jovenes
            i['fields']['adultos'] =  adultos
            i['fields']['mayores'] =  mayores

            i['fields']['m_jovenes'] =  m_joven
            i['fields']['m_adultos'] =  m_adulto
            i['fields']['m_mayores'] =  m_mayor
            i['fields']['f_jovenes'] =  f_joven
            i['fields']['f_adultos'] =  f_adulto
            i['fields']['f_mayores'] =  f_mayor

            if total_final == 0:
                i['fields']['masculino_porciento'] =  0
                i['fields']['femenino_porciento'] =  0
                i['fields']['porciento_final'] = 0
                i['fields']['jovenes_porciento'] = 0
                i['fields']['adultos_porciento'] = 0
                i['fields']['mayores_porciento'] = 0
            else:    
                i['fields']['masculino_porciento'] =  int(((masculino * 100) / total_final))
                i['fields']['femenino_porciento'] =  int(((femenino * 100) / total_final))
                i['fields']['porciento_final'] = int(((total_final * 100) / meta(request.user.nivel)))
                i['fields']['jovenes_porciento'] = int(((jovenes * 100) / total_final))
                i['fields']['adultos_porciento'] = int(((adultos * 100) / total_final))
                i['fields']['mayores_porciento'] = int(((mayores * 100) / total_final))


    return JsonResponse({"coordinadores":coordinadores, 'me':me})


def register(request):
    if request.method == 'GET':
        form = RegisterForm()
    if request.method == 'POST':
         form = RegisterForm(request.POST)
         if form.is_valid:
             form.save

             redirect('unete')     



def salir(request):
    logout(request)
    return redirect("/unete")      
