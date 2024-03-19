from django.http import JsonResponse
from django.shortcuts import render, redirect
from iqoptionapi.stable_api import IQ_Option
from .forms import CustomAuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
import time, json
import threading
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from bot.models import Foro, Respuesta, Voto, Cliente, Historial
#################################################################################
from django.contrib.auth import get_user
from django.contrib.auth.models import User
from .forms import ForoForm, RespuestaForm, VotoForm
from datetime import datetime
from .models import Configuracion
from datetime import timedelta
from django.utils import timezone
from .forms import SubscriptionForm
from django.db.models import Sum, F
from django.http import HttpResponse
####################################################################################
from django.contrib.sessions.models import Session 
from django.utils import timezone
from .models import Configuracion, Catalogo, Catalogo1, Catalogo2, Catalogo3, Catalogo4, Catalogo5, Catalogo6, Senal
from bot.catalogo import catalogo


global modo_cuenta
global api
global ganadas
global perdidas
global n77
n77 = 0
global stop_all
global stop_gain_advice
global stop_loss_advice
global num_advice
global current_user
global current_id
global plan_usuario

global martingala
global cuadrante
global lista_general2
global lista_indicadores

lista_indicadores = []


stop_loss_advice = "none"
stop_gain_advice = "none"
num_advice = "none"
stop_advice = "none"
ganadas = 0
perdidas = 0
stop_all = False
plan_usuario = ""


####################################################################################

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            contador = 0
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
            user_data = []
            for session in active_sessions:
                session_data = session.get_decoded()
                user_id = session_data.get('_auth_user_id')
                if user_id == str(request.user.id):
                    contador += 1
                user_data.append({'user_id': user_id, 'session_data': session_data})

            if contador > 3:   
                      messages.error(request, 'Se ha alcanzado la cantidad máxima de sesiones permitidas.')       
                      return redirect("/logout")
            else:
               return redirect('/catalogo/bot')  
            
        else: messages.error(request, 'Por favor, ingresa un usuario y contraseña válidos.') 
    else:
        form = CustomAuthenticationForm()
    if request.user.is_authenticated:  
         return redirect('/catalogo/bot')
    else:       
         return render(request, 'registration/login.html', {'form': form})

def clear_historial(request):
    global modo_cuenta
    historiales_a_eliminar = Historial.objects.filter(user=request.user, modo=modo_cuenta)
    historiales_a_eliminar.delete()
    data = {'mensaje':'Historial borrado con exito'}
    return JsonResponse(data, safe=False)

@login_required
def historial(request):
    global modo_cuenta
    historiales = Historial.objects.filter(user=request.user,modo=modo_cuenta).order_by('-fecha')
    
    try:
            ganancias_win = Historial.objects.filter(user=request.user, estado="Win", modo=modo_cuenta).aggregate(Sum('ganancia'))['ganancia__sum'] or 0
            ganancias_loose = -Historial.objects.filter(user=request.user, estado="Loose", modo=modo_cuenta).aggregate(Sum('ganancia'))['ganancia__sum'] or 0
            resultado_total = ganancias_win + ganancias_loose
    except:
       resultado_total = 0.00

    data = [{
    'amount': "{:.2f}".format(float(resultado_total)),
    'divisa': historial.divisa,
    'ganancia': "{:.2f}".format(float(historial.ganancia)),
    'martingala': historial.martingala,
    'estado': historial.estado,
    'fecha': historial.fecha.strftime("%m-%d %H:%M"), 
    'estrategia': historial.estrategia
    } for historial in historiales]
    
    return JsonResponse(data, safe=False)

def stop(_request):
   global stop_all
   stop_all = True
   return JsonResponse({"none":"none"})

def index(request):
    return render(request, 'index.html')

@login_required
def senales(request):
    return render(request, 'senales.html') 

from django.core.serializers import serialize

@login_required
def senales2(request): 
    senal = Senal.objects.first() 
    try:
        
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        if current_time > senal.senales[0]['hora']:
             return JsonResponse(senal.senales, safe=False)
        else:
             return JsonResponse({"error": f"Error al decodificar JSON: {str(e)}"}, status=500)    

    except json.JSONDecodeError as e:
        return JsonResponse({"error": f"Error al decodificar JSON: {str(e)}"}, status=500)               

######################### BUY SENALES ####################################
        
def buy_senales_run(request):
    global api
    api = IQ_Option("juanerodriguez23@gmail.com", "Jamil171120")
    api.connect()

    while True:
        now = datetime.now()
        s = now.second

        if s == 0:
            senal = Senal.objects.first()

            if senal:
                for i in senal.senales:
                    fecha_senal_str = i['hora']  
                    fecha_senal_datetime = datetime.strptime(fecha_senal_str, "%Y-%m-%d %H:%M:%S")
                    fecha_senal = fecha_senal_datetime.strftime("%Y-%m-%d %H:%M")


                    fecha_actual = now.strftime("%Y-%m-%d %H:%M")

                    if fecha_senal == fecha_actual:
                        accion = i['accion']
                        if i['periodo'] == 1:
                           if accion in ['call', 'put']:
                              hilo_mhi_turbo = threading.Thread(target=turbo_mhi, args=(5, i['divisa'], accion, 0, "double", 85, "señales", 1))
                              hilo_mhi_turbo.start()

            time.sleep(50)
        else:
            time.sleep(1)

@login_required
def buy_senales(request):
       hilo_run = threading.Thread(target=buy_senales_run, args=(request,))
       hilo_run.start()
       return JsonResponse({'none':'none'}, safe=False)

######################### BUY SENALES ####################################




@login_required
def manual(request):
    return render(request, 'manual.html')

@login_required
def catalogo(request,plan):
    global current_user
    global current_id
    global plan_user
    current_id = request.user.id
    current_user = request.user
    global api
    votos = 0
    estrategias = Foro.objects.filter(estado='true')
    name = request.user.username
    context = {'name':name}

    if request.user.plan == "premium":
      return render(request, 'catalogo.html',{'estrategias':estrategias})
    else:
       if request.user.plan == "regular":
            email = "juanerodriguez23@gmail.com"
            password = "Jamil171120"
            api = IQ_Option(email, password)
            api.connect()
            return render(request, 'catalogo.html',{'estrategias':estrategias})
       else:
         if request.user.plan == "free":
            email = "juanerodriguez23@gmail.com"
            password = "Jamil171120"
            api = IQ_Option(email, password)
            api.connect()
            return render(request, 'catalogo.html', {'estrategias':estrategias})
         else:
            return redirect("plans")




         
from django.shortcuts import render
def handler403(request, exception, template_name='403.html'):
    return render(request, 'plans.html')

@csrf_exempt
def operaciones2(request):
    user = request.user
    config2 = request.body
    config = json.loads(config2)

    try:
        configuracion = Configuracion.objects.get(user=user)
    except Configuracion.DoesNotExist:
        configuracion = Configuracion(user=user)

    configuracion.martingala = config["martingala"]
    configuracion.cuadrante = config["cuadrante"]
    configuracion.save()

    data = catalogo_operaciones(request)
    try:
        configuracion = Configuracion.objects.get(user=user)
    except Configuracion.DoesNotExist:
        configuracion = Configuracion(user=user)

    configuracion.datos = data
    configuracion.save()
    
    configuracion2 = Configuracion.objects.get(user=user)
    divisa = config["divisa"]
    if divisa != "none":
            try:      
                            tecnicos = []
                            asset= divisa
                            indicators = api.get_technical_indicators(asset)
                            for indicator in indicators:
                                if indicator['name'] == 'Simple Moving Average (10)' or indicator['name'] == 'Relative Strength Index (14)' or indicator['name'] == 'Stochastic %K (14, 3, 3)' or indicator['name'] == 'Exponential Moving Average (5)':   
                                     tecnicos.append(indicator['action']) 

                            conteo_sell = tecnicos.count('sell')
                            conteo_buy = tecnicos.count('buy')
                            conteo_hold = tecnicos.count('hold') 
                         
                            if conteo_sell >= 14 and conteo_buy <= 5:                            
                                  analisis_tecnico = 17
                            else:        
                                    if conteo_buy >= 14 and conteo_sell <= 5:
                                            analisis_tecnico = 73 
                                    else:  analisis_tecnico = 50
                   
            except: analisis_tecnico = 1 

    else: analisis_tecnico = 1 

    return JsonResponse({"data":configuracion2.datos,"tecnico":analisis_tecnico})

@csrf_exempt
def buy_sell(request):
  if request.user.plan == "premium": 

    global stop
    global ganadas
    global perdidas
    stop = False
    datos_buy2 = request.body
    datos_buy = json.loads(datos_buy2) 

    money = int(datos_buy['importe'])
    martingala = int(datos_buy['martingala'])
    tipo_martingala = datos_buy['tipo_martingala']
    ntime = int(datos_buy['num'])
    modo_entrada = int(datos_buy['modo_entrada'])
    after_loss = int(datos_buy['after_loss'])
    martingala_al = int(datos_buy['martingala_al'])
    buy_sell = datos_buy['datos_buy']
    indicador = datos_buy['tecnico']
    
    if datos_buy['operaciones_al'] == "": operaciones_al = 0
    else: operaciones_al = int(datos_buy['operaciones_al'])

    if datos_buy['stop_loss'] == "": stop_loss = 0
    else: 
       stop_loss = int(datos_buy['stop_loss'])
       stop_loss = stop_loss + perdidas

    if datos_buy['stop_gain'] == "": stop_gain = 0
    else: 
       stop_gain = int(datos_buy['stop_gain']) 
       stop_gain = stop_gain + ganadas
    

    mhi_count = 0
    mhi2_count = 0
    mhi3_count = 0
    torres_count = 0
    mhi_milhao = []
    mhi2_padrao = []
    mhi3_melhor= []
    torres_padrao = []
    pares0_5 = []
    pares1_6 = []
    pares2_7 = []
    pares4_9 = []
 
    for x in buy_sell: 
      if x['estrategia'] == "MHI" or x['estrategia'] == "MHI Mayoría" or x['estrategia'] == "Milhão Mayoría" or x['estrategia'] == "Milhão Minoría": 
        if x['divisa'] not in pares0_5:
           pares0_5.append(x['divisa'])
           
        mhi_milhao_dict = {   
        'estrategia': x['estrategia'], 
        'divisa': x['divisa']
        }

        mhi_milhao.append(mhi_milhao_dict)

      if x['estrategia'] == "MHI2" or x['estrategia'] == "MHI2 Mayoría" or x['estrategia'] == "Padrão 23":   
        if x['divisa'] not in pares1_6:
           pares1_6.append(x['divisa'])
           
        mhi2_padrao_dict = {   
         'estrategia': x['estrategia'], 
         'divisa': x['divisa']
           } 
        mhi2_padrao.append(mhi2_padrao_dict) 


      if x['estrategia'] == "MHI3" or x['estrategia'] == "MHI3 Mayoría" or x['estrategia'] == "Melhor de 3":   
        if x['divisa'] not in pares2_7:
           pares2_7.append(x['divisa'])

        mhi3_melhor_dict = {   
        'estrategia': x['estrategia'], 
        'divisa': x['divisa']
        }
        mhi3_melhor.append(mhi3_melhor_dict)
      
      if x['estrategia'] == "Torres Gemelas" or x['estrategia'] == "Padrão 3x1":   
        if x['divisa'] not in pares4_9:
           pares4_9.append(x['divisa'])

        torres_padrao_dict = {   
        'estrategia': x['estrategia'], 
        'divisa': x['divisa']
        }
        torres_padrao.append(torres_padrao_dict)


    for x in buy_sell: 
        comision = int(x['comision'])
        money2 = float("{:.2f}".format(money))

        #def minuto0_5(pares,divisa,money,comision,martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al):
        if x['estrategia'] == "MHI" or x['estrategia'] == "MHI Mayoría" or x['estrategia'] == "Milhão Mayoría" or x['estrategia'] == "Milhão Minoría":  
            mhi_count = mhi_count + 1     
            if mhi_count == 1:
              mhi= threading.Thread(target= minuto0_5,  args=(pares0_5,mhi_milhao,money2,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador)) 
              mhi.start()

        if x['estrategia'] == "MHI2" or x['estrategia'] == "MHI2 Mayoría" or x['estrategia'] == "Padrão 23":  
            mhi2_count = mhi2_count + 1     
            if mhi2_count == 1:
              mhi2= threading.Thread(target= minuto1_6,  args=(pares1_6,mhi2_padrao,money2,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador)) 
              mhi2.start() 
         
        if x['estrategia'] == "MHI3" or x['estrategia'] == "MHI3 Mayoría" or x['estrategia'] == "Melhor de 3":         
            mhi3_count = mhi3_count + 1     
            if mhi3_count == 1:
              mhi3= threading.Thread(target= minuto2_7,  args=(pares2_7,mhi3_melhor,money2,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador)) 
              mhi3.start()

        if x['estrategia'] == "Torres Gemelas" or x['estrategia'] == "Padrão 3x1":  
            torres_count = torres_count + 1     
            if torres_count == 1:
              torres= threading.Thread(target= minuto4_9,  args=(pares4_9,torres_padrao,money2,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador)) 
              torres.start() 

    return JsonResponse({"resultado":"hola"})
  else: 
    return JsonResponse({"resultado":"hola"})

#################################################################################################################################################################################################################################

@csrf_exempt
@login_required
def operaciones(request):
    user = request.user
    tipo_opciones = ""
    lista_general = []
    
    config2 = request.body
    config = json.loads(config2)

    global martingala
    global cuadrante
    global lista_general2
    
    lista_general2 = []
    martingala = int(config["martingala"])
    cuadrante = int(config["cuadrante"])
    #destino = config["destino"]
    tipo_mercado = config["tipo_mercado"]
    
    tiempo_actual = datetime.now() 
    n2 = 0

    while True:
        catalogo = Catalogo.objects.first()
        if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                lista_general = catalogo.lista 
                break  
        n2 = n2 + 1
        time.sleep(0.5)
        if n2 == 6:
            data = []
            return data


    lista_general = catalogo.lista
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24

    n = 0
    for i in lista_general:
        hit_count = 0
        lista = {}
        catalogos = lista_general[n]["catalogo"]
       
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': lista_general[n]["nombre"],
           'divisa': lista_general[n]["divisa"],
           "comision": lista_general[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }    
            
     
        n = n + 1
        lista_general2.append(lista)

    try:
       
        
      
        if 'OTC' in lista_general2[0]['divisa']:
            
            lista_general2 = [d for d in lista_general2 if "OTC" in d.get("divisa", "")]
        else:    
            lista_general2 = [d for d in lista_general2 if not "OTC" in d.get("divisa", "")]  
            
        if user.plan == "free":
            nueva_lista = [d for d in lista_general2 if d.get("divisa") in ["EURUSD", "EURUSD-OTC"]]
        else: nueva_lista = lista_general2    
        
        if tipo_mercado == 'binaria':
                nueva_lista = [d for d in nueva_lista if d.get("comision") in ["turbo", "ambos"]] 
                tipo_opciones = "Bin."
        if tipo_mercado == 'digital':
                nueva_lista = [d for d in nueva_lista if d.get("comision") in ["digital", "ambos"]]
                tipo_opciones = "Dig."
        data = sorted(nueva_lista, key=lambda i: i['porciento'], reverse=True)
   
    except:
        pass    

    try:
        return JsonResponse({"data":data,"type":tipo_opciones})
    except:  

        return JsonResponse({"data":"hola","type":tipo_opciones})



def catalogo_operaciones(request):
  
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
  
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo.objects.first()
    if destino == "allow":
            print("dentro")
            tiempo_actual = datetime.now()
            catalogo = Catalogo.objects.first()
            print("hola: ",catalogo)
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
                    print(catalogo2)
    else: 
      if destino == "block": 
            
            tiempo_actual = datetime.now() 
            n2 = 0
            while True:
                catalogo = Catalogo.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    print("sobrepaso")
                    lista_general = []
                    return lista_general
                    
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }    
            
    
        n = n + 1
        lista_general.append(lista)
       
    return lista_general
  

def catalogo_operaciones2(request):
  try: 
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo1.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo1.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            n2=0
            while True:
                catalogo = Catalogo1.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general      
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }        
    
        n = n + 1
        lista_general.append(lista)
    
    return lista_general
  except:   
      lista_general = []
      return lista_general
  
def catalogo_operaciones3(request):
  try:  
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo2.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo2.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            n2 = 0
            while True:
                catalogo = Catalogo2.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general      
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }       
    
        n = n + 1
        lista_general.append(lista)
    print("ok")
    return lista_general
  except: 
      print("error")  
      lista_general = []
      return lista_general

def catalogo_operaciones4(request):
  try:   
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo3.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo3.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            while True:
                n2 = 0
                catalogo = Catalogo3.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general    
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }        
    
        n = n + 1
        lista_general.append(lista)

    return lista_general
  except:   
      lista_general = []
      return lista_general

def catalogo_operaciones5(request):
  try:  
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo4.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo4.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            while True:
                n2 = 0
                catalogo = Catalogo4.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general    
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }        
    
        n = n + 1
        lista_general.append(lista)

    return lista_general
  except:   
      lista_general = []
      return lista_general

def catalogo_operaciones6(request):
  try:  
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo5.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo5.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            while True:
                n2 = 0
                catalogo = Catalogo5.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general    
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }        
    
        n = n + 1
        lista_general.append(lista)

    return lista_general
  except:   
      lista_general = []
      return lista_general
  
def catalogo_operaciones7(request):
  try:  
    lista_general = []
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    destino = configuracion.destino
    
    if user.plan == "free":
       if martingala == 0 or martingala == 1 or martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    catalogo = Catalogo6.objects.first()
    if destino == "allow":
            tiempo_actual = datetime.now()
            catalogo = Catalogo6.objects.first()
            if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                    catalogo2 = catalogo.mercado
    else:
      if destino == "block": 
            tiempo_actual = datetime.now() 
            while True:
                n2 = 0
                catalogo = Catalogo6.objects.first()
                if catalogo.fecha_y_hora.minute == tiempo_actual.minute:
                       catalogo2 = catalogo.mercado 
                       break  
                n2 = n2 + 1
                time.sleep(0.5)
                if n2 == 6:
                    lista_general = []
                    return lista_general    
   
    n = 0
    for i in catalogo2:
        hit_count = 0
        lista = {}
        catalogos = catalogo2[n]["catalogo"]
        if martingala == 0: elementos_a_reemplazar = ["p1","p2", "p3", "p4","p5","g1","g2","g3","g4","g5"] 
        if martingala == 1: elementos_a_reemplazar = ["p2", "p3", "p4","p5","g2","g3","g4","g5"]
        if martingala == 2: elementos_a_reemplazar = ["p3", "p4","p5","g3","g4","g5"]
        if martingala == 3: elementos_a_reemplazar = ["p4","p5","g4","g5"]
        if martingala == 4: elementos_a_reemplazar = ["p5","g5"]
        if martingala == 5: elementos_a_reemplazar = []
           

        for i in range(len(catalogos)):
            if catalogos[i] in elementos_a_reemplazar:
                catalogos[i] = "hit"

        catalogos = catalogos[-cuadrante:]        
        
        catalogo_filtrado = [elemento for elemento in catalogos if not elemento.startswith('p')]

        for i in catalogo_filtrado:
            if (i == "hit"): 
                  hit_count = hit_count + 1     
        porcentaje = (((hit_count * 100)/(len(catalogo_filtrado)))-100)*-1 
        porcentaje = round(porcentaje,2) 


        lista = {
           'nombre': catalogo2[n]["nombre"],
           'divisa': catalogo2[n]["divisa"],
           "comision": catalogo2[n]["comision"],
           "porciento": porcentaje,
           'catalogo':catalogos 
        }        
    
        n = n + 1
        lista_general.append(lista)

    return lista_general
  except:   
      lista_general = []
      return lista_general


############################################################################################3


'''def catalogo_operaciones(request):
    user = request.user
    configuracion = Configuracion.objects.get(user=user)
    martingala = int(configuracion.martingala)
    cuadrante = int(configuracion.cuadrante)
    if user.plan == "free":
       if martingala == 3 or martingala == 4 or martingala == 5: martingala = 2   
       if cuadrante == 96 or cuadrante == 192: cuadrante = 24
    
    num_velas = 0
    lista_general = []

    global velas
    global velas_mhi2
    global velas_mhi3
    global velas_mhimai
    global velas_mhi2mai
    global velas_mhi3mai
    global velas_milhaomin
    global velas_milhaomai
    global velas_torres
    global velas_padrao23
    global velas_padrao3x1
    global velas_mosqueteros
    global velas_melhor
    global velas_r7
    global velas_seven
    
    divisas, comision = llamar_divisas()
    n = 0
    for x in divisas:
        mhi_ciento = 0
        mhi2_ciento = 0
        mhi3_ciento = 0
        mhimai_ciento = 0
        mhi2mai_ciento = 0
        mhi3mai_ciento = 0
        milhaomin_ciento = 0
        milhaomai_ciento = 0
        torres_ciento = 0
        padrao23_ciento = 0
        padrao3x1_ciento = 0
        mosqueteros_ciento = 0
        melhor_ciento = 0
        r7_ciento = 0
        seven_ciento = 0

        lista_mhi = {}
        lista_mhi2 = {}
        lista_mhi3 = {}
        lista_mhimai = {}
        lista_mhi2mai = {}
        lista_mhi3mai = {}
        lista_milhaomin = {}
        lista_milhaomai = {}
        lista_torres = {}
        lista_padrao23 = {}
        lista_padrao3x1 = {}
        lista_melhor = {}
        lista_mosqueteros = {}
        lista_r7 = {}
        lista_seven = {}
        
        if cuadrante == 24: num_velas = 245
        if cuadrante == 48: num_velas = 485
        if cuadrante == 96: num_velas = 965
        if cuadrante == 192: num_velas = 975
        
        llamar_velas(num_velas,x)

        velas_ = threading.Thread(target=mhi_catalogo, args=(martingala, cuadrante))
        velas__mhi2 = threading.Thread(target= mhi2_catalogo, args=(martingala, cuadrante))
        velas__mhi3= threading.Thread(target= mhi3_catalogo, args=(martingala, cuadrante))
        velas__mhimai = threading.Thread(target= mhimai_catalogo, args=(martingala, cuadrante))
        velas__mhi2mai= threading.Thread(target= mhi2mai_catalogo, args=(martingala, cuadrante))
        velas__mhi3mai = threading.Thread(target= mhi3mai_catalogo, args=(martingala, cuadrante))
        velas__milhaomin= threading.Thread(target= milhaomin_catalogo, args=(martingala, cuadrante))
        velas__milhaomai = threading.Thread(target= milhaomai_catalogo, args=(martingala, cuadrante))
        velas__torres = threading.Thread(target= torres_catalogo, args=(martingala, cuadrante))
        velas__padrao23 = threading.Thread( target=padrao23_catalogo, args=(martingala, cuadrante))
        velas__padrao3x1= threading.Thread(target= padrao3x1_catalogo, args=(martingala, cuadrante))
        velas__melhor = threading.Thread(target= melhor_catalogo, args=(martingala, cuadrante))
      
        velas_.start()
        velas__mhi2.start()
        velas__mhi3.start()
        velas__mhimai.start()
        velas__mhi2mai.start()
        velas__mhi3mai.start()
        velas__milhaomin.start()
        velas__milhaomai.start()
        velas__torres.start()
        velas__padrao23.start()
        velas__padrao3x1.start()
        velas__melhor.start()

        
        velas_.join()
        velas__mhi2.join()
        velas__mhi3.join()
        velas__mhimai.join()
        velas__mhi2mai.join()
        velas__mhi3mai.join()
        velas__milhaomin.join()
        velas__milhaomai.join()
        velas__torres.join()
        velas__padrao23.join()
        velas__padrao3x1.join()
        velas__melhor.join()
      

        for mhi_porciento in velas:
            if (mhi_porciento == "hit"): 
                mhi_ciento = mhi_ciento + 1     
        porcentaje_mhi = (((mhi_ciento * 100)/(len(velas)))-100)*-1 
        porcentaje_mhi = round(porcentaje_mhi,2)

        for mhi2_porciento in velas_mhi2:
            if (mhi2_porciento == "hit"):
                mhi2_ciento = mhi2_ciento + 1
        porcentaje_mhi2 = (((mhi2_ciento * 100)/(len(velas_mhi2)))-100)*-1
        porcentaje_mhi2 = round(porcentaje_mhi2,2)

        for mhi3_porciento in velas_mhi3:
            if (mhi3_porciento == "hit"):
                mhi3_ciento = mhi3_ciento + 1
        porcentaje_mhi3 = (((mhi3_ciento * 100)/(len(velas_mhi3)))-100)*-1
        porcentaje_mhi3 = round(porcentaje_mhi3,2)

        for mhimai_porciento in velas_mhimai:
            if (mhimai_porciento == "hit"):
                mhimai_ciento = mhimai_ciento + 1
        porcentaje_mhimai = (((mhimai_ciento * 100)/(len(velas_mhimai)))-100)*-1
        porcentaje_mhimai = round(porcentaje_mhimai,2)

        for mhi2mai_porciento in velas_mhi2mai:
            if (mhi2mai_porciento == "hit"):
                mhi2mai_ciento = mhi2mai_ciento + 1
        porcentaje_mhi2mai = (((mhi2mai_ciento * 100)/(len(velas_mhi2mai)))-100)*-1
        porcentaje_mhi2mai = round(porcentaje_mhi2mai,2)

        for mhi3mai_porciento in velas_mhi3mai:
            if (mhi3mai_porciento == "hit"):
                mhi3mai_ciento = mhi3mai_ciento + 1
        porcentaje_mhi3mai = (((mhi3mai_ciento * 100)/(len(velas_mhi3mai)))-100)*-1
        porcentaje_mhi3mai = round(porcentaje_mhi3mai,2)

        for milhaomin_porciento in velas_milhaomin:
            if (milhaomin_porciento == "hit"):
                milhaomin_ciento = milhaomin_ciento + 1
        porcentaje_milhaomin = (((milhaomin_ciento * 100)/(len(velas_milhaomin)))-100)*-1
        porcentaje_milhaomin = round(porcentaje_milhaomin,2)

        for milhaomai_porciento in velas_milhaomai:
            if (milhaomai_porciento == "hit"):
                milhaomai_ciento = milhaomai_ciento + 1
        porcentaje_milhaomai = (((milhaomai_ciento * 100)/(len(velas_milhaomai)))-100)*-1
        porcentaje_milhaomai = round(porcentaje_milhaomai,2)

        for padrao23_porciento in velas_padrao23:
            if (padrao23_porciento == "hit"):
                padrao23_ciento = padrao23_ciento + 1
        porcentaje_padrao23 = (((padrao23_ciento * 100)/(len(velas_padrao23)))-100)*-1
        porcentaje_padrao23 = round(porcentaje_padrao23,2)

        for torres_porciento in velas_torres:
            if (torres_porciento == "hit"):
                torres_ciento = torres_ciento + 1
        porcentaje_torres = (((torres_ciento * 100)/(len(velas_torres)))-100)*-1
        porcentaje_torres = round(porcentaje_torres,2)

        for padrao3x1_porciento in velas_padrao3x1:
            if (padrao3x1_porciento == "hit"):
                padrao3x1_ciento = padrao3x1_ciento + 1
        porcentaje_padrao3x1 = (((padrao3x1_ciento * 100)/(len(velas_padrao3x1)))-100)*-1
        porcentaje_padrao3x1 = round(porcentaje_padrao3x1,2)

        for melhor_porciento in velas_melhor:
            if (melhor_porciento == "hit"):
                melhor_ciento = melhor_ciento + 1
        porcentaje_melhor = (((melhor_ciento * 100)/(len(velas_melhor)))-100)*-1
        porcentaje_melhor = round(porcentaje_melhor,2)

       

        lista_mhi['nombre'] = "MHI"
        lista_mhi['divisa'] = x 
        lista_mhi['comision'] = comision[n]
        lista_mhi['porciento'] = porcentaje_mhi 
        lista_mhi['catalogo'] = velas

        lista_mhi2['nombre'] = "MHI2"
        lista_mhi2['divisa'] = x 
        lista_mhi2['comision'] = comision[n]
        lista_mhi2['porciento'] = porcentaje_mhi2 
        lista_mhi2['catalogo'] = velas_mhi2

        lista_mhi3['nombre'] = "MHI3"
        lista_mhi3['divisa'] = x 
        lista_mhi3['comision'] = comision[n]
        lista_mhi3['porciento'] = porcentaje_mhi3
        lista_mhi3['catalogo'] = velas_mhi3

        lista_mhimai['nombre'] = "MHI Mayoría"
        lista_mhimai['divisa'] = x 
        lista_mhimai['comision'] = comision[n]
        lista_mhimai['porciento'] = porcentaje_mhimai
        lista_mhimai['catalogo'] = velas_mhimai

        lista_mhi2mai['nombre'] = "MHI2 Mayoría"
        lista_mhi2mai['divisa'] = x 
        lista_mhi2mai['comision'] = comision[n]
        lista_mhi2mai['porciento'] = porcentaje_mhi2mai
        lista_mhi2mai['catalogo'] = velas_mhi2mai

        lista_mhi3mai['nombre'] = "MHI3 Mayoría"
        lista_mhi3mai['divisa'] = x 
        lista_mhi3mai['comision'] = comision[n]
        lista_mhi3mai['porciento'] = porcentaje_mhi3mai
        lista_mhi3mai['catalogo'] = velas_mhi3mai

        lista_milhaomin['nombre'] = "Milhão Minoría"
        lista_milhaomin['divisa'] = x 
        lista_milhaomin['comision'] = comision[n]
        lista_milhaomin['porciento'] = porcentaje_milhaomin
        lista_milhaomin['catalogo'] = velas_milhaomin

        lista_milhaomai['nombre'] = "Milhão Mayoría"
        lista_milhaomai['divisa'] = x 
        lista_milhaomai['comision'] = comision[n]
        lista_milhaomai['porciento'] = porcentaje_milhaomai
        lista_milhaomai['catalogo'] = velas_milhaomai

        lista_padrao23['nombre'] = "Padrão 23"
        lista_padrao23['divisa'] = x 
        lista_padrao23['comision'] = comision[n]
        lista_padrao23['porciento'] = porcentaje_padrao23
        lista_padrao23['catalogo'] = velas_padrao23

        lista_torres['nombre'] = "Torres Gemelas"
        lista_torres['divisa'] = x 
        lista_torres['comision'] = comision[n]
        lista_torres['porciento'] = porcentaje_torres
        lista_torres['catalogo'] = velas_torres

        lista_padrao3x1['nombre'] = "Padrão 3x1"
        lista_padrao3x1['divisa'] = x 
        lista_padrao3x1['comision'] = comision[n]
        lista_padrao3x1['porciento'] = porcentaje_padrao3x1
        lista_padrao3x1['catalogo'] = velas_padrao3x1

        lista_melhor['nombre'] = "Melhor de 3"
        lista_melhor['divisa'] = x
        lista_melhor['comision'] = comision[n]
        lista_melhor['porciento'] = porcentaje_melhor
        lista_melhor['catalogo'] = velas_melhor

       

        lista_general.append(lista_mhi)
        lista_general.append(lista_mhi2)
        lista_general.append(lista_mhi3)
        lista_general.append(lista_mhimai)
        lista_general.append(lista_mhi2mai)
        lista_general.append(lista_mhi3mai)
        lista_general.append(lista_milhaomin)
        lista_general.append(lista_milhaomai)
        lista_general.append(lista_padrao23)
        lista_general.append(lista_torres)
        lista_general.append(lista_padrao3x1)
        lista_general.append(lista_melhor)
       
        
        n = n + 1
   
    data = sorted(lista_general, key=lambda i: i['porciento'], reverse=True)
    return data'''

def llamar_velas(divisa):
            try: 
                now = datetime.now()
                min = format(now.minute)  
                min2 = int(min)
                min3 = min2 % 10

                if min3 == 1 or min3 == 6:  num_velas = 966
                
                if min3 == 2 or min3 == 7:  num_velas = 967
            
                if min3 == 3 or min3 == 8:  num_velas = 968
                
                if min3 == 4 or min3 == 9:  num_velas = 964

                if min3 == 5 or min3 == 0:  num_velas = 965
                    
                minuto_antes = datetime.now() - timedelta(seconds=30)
                velas = api.get_candles(divisa,60,num_velas,datetime.timestamp(minuto_antes))
                return velas,min3
            except:pass

def llamar_divisas():
            try:  
                lista = []
                assets = {}
                ALL_Asset=api.get_all_open_time()

                for type_name, data in ALL_Asset.items():
                    for Asset,value in data.items():
                        if type_name == 'turbo' and value["open"] == True:
                            if Asset != "USDZAR-OTC" and Asset != "USDINR-OTC" and Asset != "USDHKD-OTC" and Asset != "USDSGD-OTC" and Asset != "USDZAR" and Asset != "USDINR" and Asset != "USDHKD" and Asset != "USDSGD":    
                                assets = {
                                        "type": type_name,
                                        "divisa": Asset
                                        }
                                
                                lista.append(assets)
                        if type_name == 'digital' and value["open"] == True: 
                            if Asset != "USDZAR-OTC" and Asset != "USDINR-OTC" and Asset != "USDHKD-OTC" and Asset != "USDSGD-OTC" and Asset != "USDZAR" and Asset != "USDINR" and Asset != "USDHKD" and Asset != "USDSGD":     
                                assets = {
                                        "type": type_name,
                                        "divisa": Asset
                                        }
                                
                                lista.append(assets)  

                divisa_dict = {}

                result = []
                for item in lista:
                    divisa = item['divisa']
                    if divisa in divisa_dict:
                        if divisa_dict[divisa] != 'ambos':
                            divisa_dict[divisa] = 'ambos'
                    else:
                        divisa_dict[divisa] = item['type']


                unique_data = [{'type': value, 'divisa': key} for key, value in divisa_dict.items()]
                unique_data_sorted = sorted(unique_data, key=lambda x: x['divisa'])
                return unique_data_sorted 
        
            except:pass


@csrf_exempt 
def porcentaje(request):
  
    global lista_general2
    porcentaje2 = request.body
    porcentaje = json.loads(porcentaje2)
 
    data = lista_general2

    estadistica = {}
    win = 0
    g1 = 0
    g2 = 0
    g3 = 0
    g4 = 0
    g5 = 0
    hit = 0
    none = 0
    hit2 = 0
    doshit = 0
    treshit = 0
    cuatrohit = 0
    cincohit = 0
    seishit = 0
    sietehit = 0
    ochohit = 0
    nuevehit = 0
    diezhit = 0
    
    for a in data:
       hit2 = 0
       for b in porcentaje:
          if a["nombre"] == b["estrategia"] and a["divisa"] == b["par"]:
            for c in a["catalogo"]:
               if c == "win":
                  win = win + 1
                  if b['modo_entrada'] == "1": hit2 = 0
               if c == "g1": 
                  g1 = g1 + 1
                  if b['modo_entrada'] == "1" or b['modo_entrada'] == "2": hit2 = 0
               if c == "g2":
                  g2 = g2 + 1
                  if b['modo_entrada'] == "1" or b['modo_entrada'] == "2" or b['modo_entrada'] == "3": hit2 = 0
               if c == "g3": 
                  g3 = g3 + 1
                  if b['modo_entrada'] == "1" or b['modo_entrada'] == "2" or b['modo_entrada'] == "3" or b['modo_entrada'] == "4": hit2 = 0
               if c == "g4": 
                  g4 = g4 + 1
                  if b['modo_entrada'] == "1" or b['modo_entrada'] == "2" or b['modo_entrada'] == "3" or b['modo_entrada'] == "4" or b['modo_entrada'] == "5": hit2 = 0
               if c == "g5": 
                  g5 = g5 + 1
                  hit2 = 0

               if c == "none": 
                  none = none + 1
                  
               if c == "hit":
                  hit = hit + 1
                  hit2 = hit2 + 1
               
               if b['modo_entrada'] == '1':
                 if hit2 == 2 and c != "none":
                   doshit = doshit + 1

                 if hit2 == 3 and c != "none": 
                    treshit = treshit + 1
                
                 if hit2 == 4 and c != "none": 
                    cuatrohit = cuatrohit + 1

                 if hit2 == 5 and c != "none": 
                    cincohit = cincohit + 1

                 if hit2 == 6 and c != "none": 
                    seishit = seishit + 1

                 if hit2 == 7 and c != "none": 
                    sietehit = sietehit + 1

                 if hit2 == 8 and c != "none": 
                    ochohit = ochohit + 1

                 if hit2 == 9 and c != "none": 
                    nuevehit = nuevehit + 1

                 if hit2 == 10 and c != "none": 
                    diezhit = diezhit + 1
                    
                  
               if b['modo_entrada'] == '2':
                 if hit2 == 2 and c != "none" and c != "win":
                   doshit = doshit + 1

                 if hit2 == 3 and c != "none" and c != "win": 
                    treshit = treshit + 1
                
                 if hit2 == 4 and c != "none" and c != "win": 
                    cuatrohit = cuatrohit + 1

                 if hit2 == 5 and c != "none" and c != "win": 
                    cincohit = cincohit + 1

                 if hit2 == 6 and c != "none" and c != "win": 
                    seishit = seishit + 1

                 if hit2 == 7 and c != "none" and c != "win": 
                    sietehit = sietehit + 1

                 if hit2 == 8 and c != "none" and c != "win": 
                    ochohit = ochohit + 1

                 if hit2 == 9 and c != "none" and c != "win": 
                    nuevehit = nuevehit + 1

                 if hit2 == 10 and c != "none" and c != "win": 
                    diezhit = diezhit + 1 

               if b['modo_entrada'] == '3':
                 if hit2 == 2 and c != "none" and c != "win" and c != "g1":
                   doshit = doshit + 1

                 if hit2 == 3 and c != "none" and c != "win" and c != "g1": 
                    treshit = treshit + 1
                
                 if hit2 == 4 and c != "none" and c != "win" and c != "g1": 
                    cuatrohit = cuatrohit + 1

                 if hit2 == 5 and c != "none" and c != "win" and c != "g1": 
                    cincohit = cincohit + 1

                 if hit2 == 6 and c != "none" and c != "win" and c != "g1": 
                    seishit = seishit + 1

                 if hit2 == 7 and c != "none" and c != "win" and c != "g1": 
                    sietehit = sietehit + 1

                 if hit2 == 8 and c != "none" and c != "win" and c != "g1": 
                    ochohit = ochohit + 1

                 if hit2 == 9 and c != "none" and c != "win" and c != "g1": 
                    nuevehit = nuevehit + 1

                 if hit2 == 10 and c != "none" and c != "win" and c != "g1" : 
                    diezhit = diezhit + 1 

               if b['modo_entrada'] == '4':
                 if hit2 == 2 and c != "none" and c != "win" and c != "g1" and c != "g2":
                   doshit = doshit + 1

                 if hit2 == 3 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    treshit = treshit + 1
                
                 if hit2 == 4 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    cuatrohit = cuatrohit + 1

                 if hit2 == 5 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    cincohit = cincohit + 1

                 if hit2 == 6 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    seishit = seishit + 1

                 if hit2 == 7 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    sietehit = sietehit + 1

                 if hit2 == 8 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    ochohit = ochohit + 1

                 if hit2 == 9 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    nuevehit = nuevehit + 1

                 if hit2 == 10 and c != "none" and c != "win" and c != "g1" and c != "g2": 
                    diezhit = diezhit + 1  
                  
               if b['modo_entrada'] == '5':
                 if hit2 == 2 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3":
                   doshit = doshit + 1

                 if hit2 == 3 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    treshit = treshit + 1
                
                 if hit2 == 4 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    cuatrohit = cuatrohit + 1

                 if hit2 == 5 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    cincohit = cincohit + 1

                 if hit2 == 6 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    seishit = seishit + 1

                 if hit2 == 7 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    sietehit = sietehit + 1

                 if hit2 == 8 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    ochohit = ochohit + 1

                 if hit2 == 9 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    nuevehit = nuevehit + 1

                 if hit2 == 10 and c != "none" and c != "win" and c != "g1" and c != "g2" and c != "g3": 
                    diezhit = diezhit + 1 
                
               
    estadistica['win'] = win
    estadistica['g1'] = g1
    estadistica['g2'] = g2
    estadistica['g3'] = g3
    estadistica['g4'] = g4
    estadistica['g5'] = g5
    estadistica['hit'] = hit
    estadistica['none'] = none
    estadistica['doshit'] = doshit
    estadistica['treshit'] = treshit
    estadistica['cuatrohit'] = cuatrohit
    estadistica['cincohit'] = cincohit
    estadistica['seishit'] = seishit
    estadistica['sietehit'] = sietehit
    estadistica['ochohit'] = ochohit
    estadistica['nuevehit'] = nuevehit
    estadistica['diezhit'] = diezhit

    return JsonResponse({"estadistica":estadistica})

def resultados(request):
        global modo_cuenta
        global api
        global stop_gain_advice
        global stop_loss_advice
        global num_advice
        global stop_advice
        global stop
        
        while True:
                now = datetime.now()
                s = format(now.second)
                s_ = int(s) 
                if s_ >= 3:
                   break
                time.sleep(2)

        usuario = Cliente.objects.get(id=request.user.id)
        fecha_ultimo_login = usuario.last_login      
         
        ganadas = Historial.objects.filter(
            modo=modo_cuenta,
            user=request.user,
            estado="Win",  # Condición "Win"
            fecha__gt= fecha_ultimo_login  # Fecha más reciente que `login_pasado`
        ).count()

        # Realiza la consulta para contar objetos que cumplen con la condición "Loose"
        perdidas = Historial.objects.filter(
            modo=modo_cuenta,
            user=request.user,
            estado="Loose",  # Condición "Loose"
            fecha__gt= fecha_ultimo_login  # Fecha más reciente que `login_pasado`
        ).count()  
        


        balance = api.get_balance()
        pizarras = {"ganadas":ganadas,"perdidas":perdidas, "balance":balance, "stop_gain_advice":stop_gain_advice, "stop_loss_advice":stop_loss_advice, "num_advice":num_advice, "stop_advice":stop_advice}
        return JsonResponse(pizarras)
        

def minuto0_5(pares,divisa,money,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador_tecnico):

 global stop_all
 global api
 stop_all = False
 global estatus_lista
 estatus_lista = []
 global stop_gain_advice
 global stop_loss_advice
 global num_advice
 global stop_advice
 global ganadas
 global perdidas
 global n77
 global date
 stop_gain_advice = "none"
 stop_loss_advice = "none"
 num_advice = "none"
 stop_advice = "none"
 n77 = 0
 add = 0
 add2 = 0
 count_mhi = 0
 paso_mhi = False
 if modo_entrada == 0 or modo_entrada == 1: add = 0
 if modo_entrada == 2: 
     add = 1
     add2 = 9
 if modo_entrada == 3: 
     add = 2
     add2 = 8
 if modo_entrada == 4:
     add = 3
     add2 = 7
 if modo_entrada == 5: 
     add = 4
     add2 = 6

 if after_loss == 0: add_al = 0
 if after_loss == 1: add_al = 5
 if after_loss == 2: add_al = 10
 if after_loss == 3: add_al = 15

 while n77 < ntime:
    option_mhi = "none"
    option_mhimai = "none"
    option_milhaomin = "none"
    option_milhaomai = "none"

    conteo_sell = 0
    conteo_buy = 0
    conteo_hold = 0

    after_mhi = "stop" 
    after_mhi_2 = "stop"
    after_mhi_3 = "stop"
    enter_mhi = "stop"
    after_mhimai = "stop" 
    after_mhimai_2 = "stop"
    after_mhimai_3 = "stop"
    enter_mhimai = "stop"
    after_milhao = "stop" 
    after_milhao_2 = "stop"
    after_milhao_3 = "stop"
    enter_milhao = "stop"
    after_milhaomai = "stop" 
    after_milhaomai_2 = "stop"
    after_milhaomai_3 = "stop"
    enter_milhaomai = "stop"

    mhi_entrada = 'stop'
    mhimai_entrada = 'stop'
    milhaomin_entrada = 'stop'
    milhaomai_entrada = 'stop'   

    while True:
            now = datetime.now()
            s = format(now.second)
            m = format(now.minute)
            m_ = int(m)
            ultimo_digito = m_ % 10
            if ultimo_digito == 4 + add  or ultimo_digito == 9 - add2: 
                if s == "50": 
                    if indicador_tecnico == "on":   
                        try:      
                                tecnicos = []
                                asset= pares[0]
                                indicators = api.get_technical_indicators(asset)
                                for indicator in indicators:
                                    if indicator['name'] == 'Simple Moving Average (10)' or indicator['name'] == 'Relative Strength Index (14)' or indicator['name'] == 'Stochastic %K (14, 3, 3)' or indicator['name'] == 'Exponential Moving Average (5)':   
                                        tecnicos.append(indicator['action']) 

                                conteo_sell = tecnicos.count('sell')
                                conteo_buy = tecnicos.count('buy')
                                conteo_hold = tecnicos.count('hold') 
                        except:pass           
                    break  

            if stop_all == True:
               break  
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break   
            time.sleep(0.3)

    while True:
            now = datetime.now()
            s = format(now.second)
            if s == "0": 
               break 
            if stop_all == True:
               break 
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break        
            time.sleep(0.1)  
  
    if stop_all == True:
         break
    if stop_loss <= perdidas and stop_loss > 0:
               stop_loss_advice = 'active'  
               break   
    if stop_gain <= ganadas and stop_gain > 0:
               stop_gain_advice = 'active'  
               break

    for par in pares:  
     minuto_antes = datetime.now() - timedelta(minutes=1)
     data = api.get_candles(par,60,5 + add + add_al,datetime.timestamp(minuto_antes))

     if data[0]['open'] < data[0]['close']: 
      vela0 = 1 
     else:
        if data[0]['open'] > data[0]['close']: 
          vela0 = -1
        else: vela0 = 0  
    
     if data[1]['open'] < data[1]['close']: 
      vela1 = 1 
     else:
        if data[1]['open'] > data[1]['close']: 
           vela1 = -1
        else: vela1 = 0   

     if data[2]['open'] < data[2]['close']: 
      vela2 = 1 
     else:
        if data[2]['open'] > data[2]['close']:
           vela2 = -1
        else: vela2 = 0  

     if data[3]['open'] < data[3]['close']: 
         vela3 = 1 
     else:
            if data[3]['open'] > data[3]['close']: 
             vela3 = -1
            else: vela3 = 0  

     if data[4]['open'] < data[4]['close']: 
           vela4 = 1 
     else:
            if data[4]['open'] > data[4]['close']: 
             vela4 = -1
            else: vela4 = 0   
  ################################### MODO ENTRADA AL= 0##################################
     if after_loss == 0:
       if modo_entrada >= 2:         
            if data[5]['open'] < data[5]['close']: 
                    vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                    vela5 = -1
                else: vela5 = 0 
       if modo_entrada >= 3:         
            if data[6]['open'] < data[6]['close']: 
                    vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                    vela6 = -1
                else: vela6 = 0
       if modo_entrada >= 4:         
            if data[7]['open'] < data[7]['close']: 
                    vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                    vela7 = -1
                else: vela7 = 0
       if modo_entrada == 5:         
            if data[8]['open'] < data[8]['close']: 
                    vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']:
                    vela8 = -1
                else: vela8 = 0                           

     if after_loss == 1 or after_loss == 2 or after_loss == 3:  
            if data[5]['open'] < data[5]['close']: 
              vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                  vela5 = -1
                else: vela5 = 0 
            
            if data[6]['open'] < data[6]['close']: 
              vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                  vela6 = -1
                else: vela6 = 0
   
            if data[7]['open'] < data[7]['close']: 
              vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                  vela7 = -1
                else: vela7 = 0
     
            if data[8]['open'] < data[8]['close']: 
              vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']: 
                  vela8 = -1
                else: vela8 = 0  
            
            if data[9]['open'] < data[9]['close']: 
              vela9 = 1 
            else:
                if data[9]['open'] > data[9]['close']: 
                  vela9 = -1
                else: vela9 = 0 
               
     if after_loss == 1:
       if modo_entrada >= 2:  
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 

       if modo_entrada >= 3: 
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0
        
       if modo_entrada >= 4: 
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0

       if modo_entrada == 5:
         if data[13]['open'] < data[13]['close']: 
           vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
               vela13 = -1
            else: vela13 = 0 
     
     if after_loss == 2 or after_loss == 3:     
            
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 

        
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0
        
        
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0

       
         if data[13]['open'] < data[13]['close']: 
           vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
               vela13 = -1
            else: vela13 = 0

         if data[14]['open'] < data[14]['close']: 
              vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']: 
              vela14 = -1
            else: vela14 = 0  

     if after_loss == 2:
       if modo_entrada >= 2:   
         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
       if modo_entrada >= 3: 
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
       if modo_entrada >= 4: 
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
       if modo_entrada == 5:
         if data[18]['open'] < data[18]['close']: 
            vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
               vela18 = -1
            else: vela18 = 0

     if after_loss == 3:
  
         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
        
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
        
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
        
         if data[18]['open'] < data[18]['close']: 
            vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
               vela18 = -1
            else: vela18 = 0
         
         if data[19]['open'] < data[19]['close']: 
               vela19 = 1 
         else:
                if data[19]['open'] > data[19]['close']:
                   vela19 = -1
                else: vela19 = 0 

         if modo_entrada >= 2:       
             if data[20]['open'] < data[20]['close']: 
                vela20 = 1 
             else:
                if data[20]['open'] > data[20]['close']:
                    vela20 = -1
                else: vela20 = 0 

         if modo_entrada >= 3:  
             if data[21]['open'] < data[21]['close']: 
                vela21 = 1 
             else:
                if data[21]['open'] > data[21]['close']:
                    vela21 = -1
                else: vela21 = 0

         if modo_entrada >= 4:  
             if data[22]['open'] < data[22]['close']: 
                vela22 = 1 
             else:
                if data[22]['open'] > data[22]['close']:
                    vela22 = -1
                else: vela22 = 0

         if modo_entrada == 5:   
             if data[23]['open'] < data[23]['close']: 
                vela23 = 1 
             else:
                if data[23]['open'] > data[23]['close']:
                    velas23 = -1
                else: vela23 = 0
    


     if modo_entrada == 0:
            mhi_entrada = 'go'    
            mhimai_entrada = 'go'
            milhaomin_entrada = 'go'
            milhaomai_entrada = 'go'

     if after_loss == 0:   
        if vela2 == 0 or vela3 == 0 or vela4 == 0:
           mhi_clave = 404
        else:   
           mhi_clave = vela2 + vela3 + vela4
        
        if vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0:
           milhao_clave = 404
        else:   
           milhao_clave = vela0 + vela1 + vela2 + vela3 + vela4
    
     if after_loss == 1:  
        
        mhi_af1 = vela2 + vela3 + vela4
        milhao_af1 = vela0 + vela1 + vela2 + vela3 + vela4

        if vela7 == 0 or vela8 == 0 or vela9 == 0:
           mhi_clave = 404
        else:   
           mhi_clave = vela7 + vela8 + vela9
        
        if vela5 == 0 or vela6 == 0 or vela7 == 0 or vela8 == 0 or vela9 == 0:
           milhao_clave = 404
        else:   
           milhao_clave = vela5 + vela6 + vela7 + vela8 + vela9

     if after_loss == 2:  

        mhi_af1 = vela2 + vela3 + vela4
        milhao_af1 = vela0 + vela1 + vela2 + vela3 + vela4

        mhi_af2 = vela7 + vela8 + vela9
        milhao_af2 = vela5 + vela6 + vela7 + vela8 + vela9

        if vela12 == 0 or vela13 == 0 or vela14 == 0:
           mhi_clave = 404
        else:   
           mhi_clave = vela12 + vela13 + vela14
        
        if vela10 == 0 or vela11 == 0 or vela12 == 0 or vela13 == 0 or vela14 == 0:
           milhao_clave = 404
        else:   
           milhao_clave = vela10 + vela11 + vela12 + vela13 + vela14

     if after_loss == 3:  

        mhi_af1 = vela2 + vela3 + vela4
        milhao_af1 = vela0 + vela1 + vela2 + vela3 + vela4

        mhi_af2 = vela7 + vela8 + vela9
        milhao_af2 = vela5 + vela6 + vela7 + vela8 + vela9

        mhi_af3 = vela12 + vela13 + vela14
        milhao_af3 = vela10 + vela11 + vela12 + vela13 + vela14

        if vela17 == 0 or vela18 == 0 or vela19 == 0:
           mhi_clave = 404
        else:   
           mhi_clave = vela17 + vela18 + vela19
        
        if vela15 == 0 or vela16 == 0 or vela17 == 0 or vela18 == 0 or vela19 == 0:
           milhao_clave = 404
        else:   
           milhao_clave = vela15 + vela16 + vela17 + vela18 + vela19

    
     if mhi_clave > 0: 
            option_mhi = 'put'
            option_mhimai = 'call'
     if mhi_clave < 0: 
            option_mhi = 'call'
            option_mhimai = 'put'
     if mhi_clave == 404: 
            option_mhi = 'none' 
            option_mhimai = 'none'
     if milhao_clave > 0: 
            option_milhaomin = 'put'
            option_milhaomai = 'call'
     if milhao_clave < 0: 
            option_milhaomin = 'call'
            option_milhaomai = 'put'
     if milhao_clave == 404: 
            option_milhaomin = 'none'
            option_milhaomai = 'none'

     if modo_entrada == 2:
       if after_loss == 0:
            if option_mhi == 'put' and vela5 > 0: mhi_entrada = 'go'
            if option_mhi == 'call' and vela5 < 0: mhi_entrada = 'go' 
            if option_milhaomin == 'put' and vela5 > 0: milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela5 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela5 > 0: mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela5 < 0: mhimai_entrada = 'go' 
            if option_milhaomai == 'put' and vela5 > 0: milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela5 < 0: milhaomai_entrada = 'go'     
            if vela5 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

       if after_loss == 1:
            if option_mhi == 'put' and vela10 > 0: mhi_entrada = 'go'
            if option_mhi == 'call' and vela10 < 0: mhi_entrada = 'go' 
            if option_milhaomin == 'put' and vela10 > 0: milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela10 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela10 > 0: mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela10 < 0: mhimai_entrada = 'go' 
            if option_milhaomai == 'put' and vela10 > 0: milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela10 < 0: milhaomai_entrada = 'go'        
            if vela10 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

       if after_loss == 2:
            if option_mhi == 'put' and vela15 > 0: mhi_entrada = 'go'
            if option_mhi == 'call' and vela15 < 0: mhi_entrada = 'go' 
            if option_milhaomin == 'put' and vela15 > 0: milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela15 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela15 > 0: mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela15 < 0: mhimai_entrada = 'go' 
            if option_milhaomai == 'put' and vela15 > 0: milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela15 < 0: milhaomai_entrada = 'go'        
            if vela15 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

       if after_loss == 3:
            if option_mhi == 'put' and vela20 > 0: mhi_entrada = 'go'
            if option_mhi == 'call' and vela20 < 0: mhi_entrada = 'go' 
            if option_milhaomin == 'put' and vela20 > 0: milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela20 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela20 > 0: mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela20< 0: mhimai_entrada = 'go' 
            if option_milhaomai == 'put' and vela20 > 0: milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela20 < 0: milhaomai_entrada = 'go'        
            if vela20 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'        


     if modo_entrada == 3:
        if after_loss == 0:    
            if option_mhi == 'put' and vela5 > 0 and vela6 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela5 < 0 and vela6 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela5 > 0 and vela6 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela5 < 0 and vela6 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela5 > 0 and vela6 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela5 < 0 and vela6 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela5 > 0 and vela6 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela5 < 0 and vela6 < 0: milhaomai_entrada = 'go'
            if vela5 == 0 or vela6 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 1:    
            if option_mhi == 'put' and vela10 > 0 and vela11 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela10 < 0 and vela11 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela10 > 0 and vela11 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela10 < 0 and vela11 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela10 > 0 and vela11 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela10 < 0 and vela11 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela10 > 0 and vela11 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela10 < 0 and vela11 < 0: milhaomai_entrada = 'go'
            if vela10 == 0 or vela11 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'   

        if after_loss == 2:    
            if option_mhi == 'put' and vela15 > 0 and vela16 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela15 < 0 and vela16 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela15 > 0 and vela16 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela15 < 0 and vela16 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela15 > 0 and vela16 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela15 < 0 and vela16 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela15 > 0 and vela16 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela15 < 0 and vela16 < 0: milhaomai_entrada = 'go'
            if vela15 == 0 or vela16 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 3:    
            if option_mhi == 'put' and vela20 > 0 and vela21 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela20 < 0 and vela21 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela20 > 0 and vela21 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela20 < 0 and vela21 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela20 > 0 and vela21 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela20 < 0 and vela21 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela20 > 0 and vela21 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela20 < 0 and vela21 < 0: milhaomai_entrada = 'go'
            if vela20 == 0 or vela21 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'       

 
     if modo_entrada == 4:
        if after_loss == 0:    
            if option_mhi == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0: milhaomai_entrada = 'go' 
            if vela5 == 0 or vela6 == 0 or vela7 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 1:    
            if option_mhi == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0: milhaomai_entrada = 'go' 
            if vela10 == 0 or vela11 == 0 or vela12 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop' 

        if after_loss == 2:    
            if option_mhi == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela15 < 0 and vela16 < 0 and vela7 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0: milhaomai_entrada = 'go' 
            if vela15 == 0 or vela16 == 0 or vela17 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'  

        if after_loss == 3:    
            if option_mhi == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0: milhaomai_entrada = 'go' 
            if vela20 == 0 or vela21 == 0 or vela22 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'                  


     if modo_entrada == 5:
        if after_loss == 0:    
            if option_mhi == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0 and vela8 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0 and vela8 > 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0 and vela8 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0 and vela8 > 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0 and vela8 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0 and vela8 > 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela5 > 0 and vela6 > 0 and vela7 > 0 and vela8 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela5 < 0 and vela6 < 0 and vela7 < 0 and vela8 > 0: milhaomai_entrada = 'go'
            if vela5 == 0 or vela6 == 0 or vela7 == 0 or vela8 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 1:    
            if option_mhi == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0 and vela13 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0 and vela13 > 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0 and vela13 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0 and vela13 > 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0 and vela13 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0 and vela13 > 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela10 > 0 and vela11 > 0 and vela12 > 0 and vela13 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela10 < 0 and vela11 < 0 and vela12 < 0 and vela13 > 0: milhaomai_entrada = 'go'
            if vela10 == 0 or vela11 == 0 or vela12 == 0 or vela13 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 2:    
            if option_mhi == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0 and vela18 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0 and vela18 > 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0 and vela18 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0 and vela18 > 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0 and vela18 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0 and vela18 > 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela15 > 0 and vela16 > 0 and vela17 > 0 and vela18 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela15 < 0 and vela16 < 0 and vela17 < 0 and vela18 > 0: milhaomai_entrada = 'go'
            if vela15 == 0 or vela16 == 0 or vela17 == 0 or vela18 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 3:    
            if option_mhi == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0 and vela23 > 0:  mhi_entrada = 'go'
            if option_mhi == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0 and vela23 > 0: mhi_entrada = 'go'
            if option_milhaomin == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0 and vela23 > 0:  milhaomin_entrada = 'go'
            if option_milhaomin == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0 and vela23 > 0: milhaomin_entrada = 'go'
            if option_mhimai == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0 and vela23 > 0:  mhimai_entrada = 'go'
            if option_mhimai == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0 and vela23 > 0: mhimai_entrada = 'go'
            if option_milhaomai == 'put' and vela20 > 0 and vela21 > 0 and vela22 > 0 and vela23 > 0:  milhaomai_entrada = 'go'
            if option_milhaomai == 'call' and vela20 < 0 and vela21 < 0 and vela22 < 0 and vela23 > 0: milhaomai_entrada = 'go'
            if vela20 == 0 or vela21 == 0 or vela22 == 0 or vela23 == 0:
               mhi_entrada = 'stop'
               mhimai_entrada = 'stop'
               milhaomin_entrada = 'stop'
               milhaomai_entrada = 'stop'                     

     if after_loss > 0:
        if martingala_al == 0:
         if after_loss == 1 or after_loss == 2 or after_loss == 3:
            if mhi_af1 > 0 and vela5 == 1: after_mhi = "go"
            if mhi_af1 < 0 and vela5 == -1: after_mhi = "go"
            if mhi_af1 < 0 and vela5 == 1: after_mhimai = "go"
            if mhi_af1 > 0 and vela5 == -1: after_mhimai = "go"
            if milhao_af1 > 0 and vela5 == 1: after_milhao = "go"
            if milhao_af1 < 0 and vela5 == -1: after_milhao = "go"
            if milhao_af1 < 0 and vela5 == 1: after_milhaomai = "go"
            if milhao_af1 > 0 and vela5 == -1: after_milhaomai = "go"
         if after_loss == 2 or after_loss == 3:
            if mhi_af2 > 0 and vela10 == 1: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 == -1: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 == 1: after_mhimai_2 = "go"
            if mhi_af2 > 0 and vela10 == -1: after_mhimai_2 = "go"
            if milhao_af2 > 0 and vela10 == 1: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 == -1: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 == 1: after_milhaomai_2 = "go"
            if milhao_af2 > 0 and vela10 == -1: after_milhaomai_2 = "go"
         if after_loss == 3:
            if mhi_af3 > 0 and vela15 == 1: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 == -1: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 == 1: after_mhimai_3 = "go"
            if mhi_af3 > 0 and vela15 == -1: after_mhimai_3 = "go"
            if milhao_af3 > 0 and vela15 == 1: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 == -1: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 == 1: after_milhaomai_3 = "go"
            if milhao_af3 > 0 and vela15 == -1: after_milhaomai_3 = "go"   
        
        if martingala_al == 1:
         if after_loss == 1 or after_loss == 2 :
            if mhi_af1 > 0 and vela5 + vela6 == 2: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6== -2: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6== 2: after_mhimai = "go"
            if mhi_af1 > 0 and vela5 + vela6== -2: after_mhimai = "go"
            if milhao_af1 > 0 and vela5 + vela6== 2: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6== -2: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6== 2: after_milhaomai = "go"
            if milhao_af1 > 0 and vela5 + vela6== -2: after_milhaomai = "go"
         if after_loss == 2 or after_loss == 3:
            if mhi_af2 > 0 and vela10 + vela11 == 2: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11== -2: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11== 2: after_mhimai_2 = "go"
            if mhi_af2 > 0 and vela10 + vela11== -2: after_mhimai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11== 2: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11== -2: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11== 2: after_milhaomai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11== -2: after_milhaomai_2 = "go"
         if after_loss == 3:
            if mhi_af3 > 0 and vela15 + vela16== 2: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16== -2: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 == 2: after_mhimai_3 = "go"
            if mhi_af3 > 0 and vela15 + vela16 == -2: after_mhimai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 == 2: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 == -2: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 == 2: after_milhaomai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 == -2: after_milhaomai_3 = "go"    
        
        if martingala_al == 2:
          if after_loss == 1 or after_loss == 2 :
            if mhi_af1 > 0 and vela5 + vela6 + vela7 == 3: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7== -3: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7== 3: after_mhimai = "go"
            if mhi_af1 > 0 and vela5 + vela6 + vela7== -3: after_mhimai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7== 3: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7== -3: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7== 3: after_milhaomai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7== -3: after_milhaomai = "go"
          if after_loss == 2 or after_loss == 3:
            if mhi_af2 > 0 and vela10 + vela11 + vela12 == 3: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12== -3: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12== 3: after_mhimai_2 = "go"
            if mhi_af2 > 0 and vela10 + vela11 + vela12== -3: after_mhimai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12== 3: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12== -3: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12== 3: after_milhaomai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12== -3: after_milhaomai_2 = "go"
          if after_loss == 3:
            if mhi_af3 > 0 and vela15 + vela16 + vela17== 3: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17== -3: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17== 3: after_mhimai_3 = "go"
            if mhi_af3 > 0 and vela15 + vela16 + vela17== -3: after_mhimai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17 == 3: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17== -3: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17== 3: after_milhaomai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17== -3: after_milhaomai_3 = "go"   

        if martingala_al == 3:
          if after_loss == 1 or after_loss == 2 :
            if mhi_af1 > 0 and vela5 + vela6 + vela7 + vela8 == 4: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7 + vela8== -4: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7 + vela8== 4: after_mhimai = "go"
            if mhi_af1 > 0 and vela5 + vela6 + vela7 + vela8== -4: after_mhimai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7 + vela8== 4: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7 + vela8== -4: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7 + vela8== 4: after_milhaomai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7 + vela8== -4: after_milhaomai = "go"
          if after_loss == 2 or after_loss == 3:
            if mhi_af2 > 0 and vela10 + vela11 + vela12 + vela13 == 4: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12 + vela13== -4: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12 + vela13== 4: after_mhimai_2 = "go"
            if mhi_af2 > 0 and vela10 + vela11 + vela12 + vela13== -4: after_mhimai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12 + vela13== 4: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12 + vela13== -4: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12 + vela13== 4: after_milhaomai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12 + vela13== -4: after_milhaomai_2 = "go" 
          if after_loss == 3:
            if mhi_af3 > 0 and vela15 + vela16 + vela17 + vela18== 4: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17 + vela18== -4: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17 + vela18== 4: after_mhimai_3 = "go"
            if mhi_af3 > 0 and vela15 + vela16 + vela17 + vela18== -4: after_mhimai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17 + vela18 == 4: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17 + vela18== -4: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17 + vela18== 4: after_milhaomai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17 + vela18== -4: after_milhaomai_3 = "go"

        if martingala_al == 4:
         if after_loss == 1 or after_loss == 2 :
            if mhi_af1 > 0 and vela5 + vela6 + vela7 + vela8 + vela9 == 5: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7 + vela8 + vela9== -5: after_mhi = "go"
            if mhi_af1 < 0 and vela5 + vela6 + vela7 + vela8 + vela9== 5: after_mhimai = "go"
            if mhi_af1 > 0 and vela5 + vela6 + vela7 + vela8 + vela9== -5: after_mhimai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7 + vela8 + vela9== 5: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7 + vela8 + vela9== -5: after_milhao = "go"
            if milhao_af1 < 0 and vela5 + vela6 + vela7 + vela8 + vela9== 5: after_milhaomai = "go"
            if milhao_af1 > 0 and vela5 + vela6 + vela7 + vela8 + vela9== -5: after_milhaomai = "go"
         if after_loss == 2 or after_loss == 3:
            if mhi_af2 > 0 and vela10 + vela11 + vela12 + vela13 + vela14 == 5: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12 + vela13 + vela14== -5: after_mhi_2 = "go"
            if mhi_af2 < 0 and vela10 + vela11 + vela12 + vela13 + vela14== 5: after_mhimai_2 = "go"
            if mhi_af2 > 0 and vela10 + vela11 + vela12 + vela13 + vela14== -5: after_mhimai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12 + vela13 + vela14== 5: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12 + vela13 + vela14== -5: after_milhao_2 = "go"
            if milhao_af2 < 0 and vela10 + vela11 + vela12 + vela13 + vela14== 5: after_milhaomai_2 = "go"
            if milhao_af2 > 0 and vela10 + vela11 + vela12 + vela13 + vela14== -5: after_milhaomai_2 = "go"  
         if after_loss == 3:
            if mhi_af3 > 0 and vela15 + vela16 + vela17 + vela18 + vela19== 5: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17 + vela18 + vela19== -5: after_mhi_3 = "go"
            if mhi_af3 < 0 and vela15 + vela16 + vela17 + vela18 + vela19== 5: after_mhimai_3 = "go"
            if mhi_af3 > 0 and vela15 + vela16 + vela17 + vela18 + vela19== -5: after_mhimai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17 + vela18 + vela19 == 5: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17 + vela18 + vela19== -5: after_milhao_3 = "go"
            if milhao_af3 < 0 and vela15 + vela16 + vela17 + vela18 + vela19== 5: after_milhaomai_3 = "go"
            if milhao_af3 > 0 and vela15 + vela16 + vela17 + vela18 + vela19== -5: after_milhaomai_3 = "go"   

        
     if after_loss == 0: 
        enter_mhi = "go"  
        enter_mhimai = "go" 
        enter_milhao = "go" 
        enter_milhaomai = "go"   
     if after_loss == 1:  
        if after_mhi == "go": enter_mhi = "go"
        if after_mhimai == "go": enter_mhimai = "go"
        if after_milhao == "go": enter_milhao = "go"
        if after_milhaomai == "go": enter_milhaomai = "go"
     if after_loss == 2:  
        if after_mhi == "go" and after_mhi_2 == "go": enter_mhi = "go"
        if after_mhimai == "go" and after_mhimai_2 == "go": enter_mhimai = "go"
        if after_milhao == "go" and after_milhao_2 == "go": enter_milhao = "go"
        if after_milhaomai == "go" and after_milhaomai_2 == "go": enter_milhaomai = "go"
     if after_loss == 3:  
        if after_mhi == "go" and after_mhi_2 == "go" and after_mhi_3 == "go": enter_mhi = "go"
        if after_mhimai == "go" and after_mhimai_2 == "go" and after_mhimai_3 == "go": enter_mhimai = "go"
        if after_milhao == "go" and after_milhao_2 == "go" and after_milhao_3 == "go": enter_milhao = "go"
        if after_milhaomai == "go" and after_milhaomai_2 == "go" and after_milhaomai_3 == "go": enter_milhaomai = "go"   
     
     if after_loss > 0 and operaciones_al > 0:
        if paso_mhi == True:
           enter_mhi = 'go'
        if enter_mhi == 'go':
           paso_mhi = True
           count_mhi = count_mhi + 1
        if count_mhi > operaciones_al:
           paso_mhi = False
           enter_mhi = 'none' 
           count_mhi = 0  

     ######################################################################################################## 
    if indicador_tecnico == "on": 
        try:
                if conteo_sell >= 14 and conteo_buy <= 5:
                        if option_mhi == "call": option_mhi = "none"
                        if option_mhimai == "call": option_mhimai = "none"
                        if option_milhaomin == "call": option_milhaomin = "none"
                        if option_milhaomai == "call": option_milhaomai = "none"
                else:        

                    if conteo_buy >= 14 and conteo_sell <= 5:
                            if option_mhi == "put": option_mhi = "none"
                            if option_mhimai == "put": option_mhimai = "none"
                            if option_milhaomin == "put": option_milhaomin = "none"
                            if option_milhaomai == "put": option_milhaomai = "none" 
                    else:
                            option_mhi = "none" 
                            option_mhimai = "none" 
                            option_milhaomin = "none"  
                            option_milhaomai = "none"  
        except: pass                                 


    for i in divisa:                                             
            if i['estrategia'] == "MHI" and enter_mhi == 'go' and option_mhi != 'none' and mhi_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhi_turbo = threading.Thread(target=turbo_mhi, args=(money,i['divisa'], option_mhi,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhi_turbo.start() 
                                           
            if i['estrategia'] == "MHI Mayoría" and enter_mhimai == 'go' and option_mhimai != 'none' and mhimai_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhimai_turbo = threading.Thread(target=turbo_mhimai, args=(money,i['divisa'], option_mhimai,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhimai_turbo.start() 
                         
            if i['estrategia'] == "Milhão Minoría" and enter_milhao == 'go' and option_milhaomin != 'none' and milhaomin_entrada == 'go' and n77 < ntime: 
                            n77 = n77 + 1
                            hilo_milhao_turbo = threading.Thread(target=turbo_milhao, args=(money,i['divisa'], option_milhaomin,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_milhao_turbo.start() 
                   
            if i['estrategia'] == "Milhão Mayoría" and enter_milhaomai == 'go' and option_milhaomai != 'none' and milhaomai_entrada == 'go' and n77 < ntime: 
                            n77 = n77 + 1           
                            hilo_milhaomai_turbo = threading.Thread(target=turbo_milhaomai, args=(money,i['divisa'], option_milhaomai,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_milhaomai_turbo.start() 
           
    if ntime <= n77:
       stop_advice = 'active'    
 ##################################################################################################################################################################################

def minuto1_6(pares,divisa,money,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador_tecnico):
 global stop_all
 stop_all = False
 global estatus_lista
 estatus_lista = []
 global stop_gain_advice
 global stop_loss_advice
 global num_advice
 global stop_advice
 global ganadas
 global perdidas
 global n77
 stop_gain_advice = "none"
 stop_loss_advice = "none"
 num_advice = "none"
 stop_advice = "none"
 n77 = 0
 add = 0
 add2 = 0
 count_mhi2 = 0
 paso_mhi2 = False
 if modo_entrada == 0 or modo_entrada == 1: add = 0
 if modo_entrada == 2: 
     add = 1
     add2 = 9
 if modo_entrada == 3: 
     add = 2
     add2 = 8
 if modo_entrada == 4:
     add = 3
     add2 = 7
 if modo_entrada == 5: 
     add = 4
     add2 = 6

 if after_loss == 0: add_al = 0
 if after_loss == 1: add_al = 5
 if after_loss == 2: add_al = 10
 if after_loss == 3: add_al = 15

 while n77 < ntime:
   
    opcion_mhi2 = "none"
    opcion_mhi2mai = "none"
    opcion_padrao23 = "none"

    after_mhi2 = "stop" 
    after_mhi2_2 = "stop"
    after_mhi2_3 = "stop"
    enter_mhi2 = "stop"
    after_mhi2mai = "stop" 
    after_mhi2mai_2 = "stop"
    after_mhi2mai_3 = "stop"
    enter_mhi2mai = "stop"
    after_padrao23 = "stop" 
    after_padrao23_2 = "stop"
    after_padrao23_3 = "stop"
    enter_padrao23 = "stop"
    

    mhi2_entrada = 'stop'
    mhi2mai_entrada = 'stop'
    padrao23_entrada = 'stop'
    

    while True:
            now = datetime.now()
            s = format(now.second)
            m = format(now.minute)
            m_ = int(m)
            ultimo_digito = m_ % 10
            if ultimo_digito == 0 + add  or ultimo_digito == 5 + add: 
                if s == "50": 
                    if indicador_tecnico == "on":   
                        try:      
                                tecnicos = []
                                asset= pares[0]
                                indicators = api.get_technical_indicators(asset)
                                for indicator in indicators:
                                    if indicator['name'] == 'Simple Moving Average (10)' or indicator['name'] == 'Relative Strength Index (14)' or indicator['name'] == 'Stochastic %K (14, 3, 3)' or indicator['name'] == 'Exponential Moving Average (5)':   
                                        tecnicos.append(indicator['action']) 

                                conteo_sell = tecnicos.count('sell')
                                conteo_buy = tecnicos.count('buy')
                                conteo_hold = tecnicos.count('hold') 
                        except:pass           
                    break  
            if stop_all == True:
               break  
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break   
            time.sleep(0.3)

    while True:
            now = datetime.now()
            s = format(now.second)
            if s == "0": 
               break 
            if stop_all == True:
               break 
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break        
            time.sleep(0.1)  
  
    if stop_all == True:
        break
    if stop_loss <= perdidas and stop_loss > 0:
               stop_loss_advice = 'active'  
               break   
    if stop_gain <= ganadas and stop_gain > 0:
               stop_gain_advice = 'active'  
               break

    for par in pares:  
     minuto_antes = datetime.now() - timedelta(minutes=1)
     data = api.get_candles(par,60,4 + add + add_al,datetime.timestamp(minuto_antes))

     if data[0]['open'] < data[0]['close']: 
      vela0 = 1 
     else:
        if data[0]['open'] > data[0]['close']: 
          vela0 = -1
        else: vela0 = 0  
    
     if data[1]['open'] < data[1]['close']: 
      vela1 = 1 
     else:
        if data[1]['open'] > data[1]['close']: 
           vela1 = -1
        else: vela1 = 0   

     if data[2]['open'] < data[2]['close']: 
      vela2 = 1 
     else:
        if data[2]['open'] > data[2]['close']:
           vela2 = -1
        else: vela2 = 0  

     if data[3]['open'] < data[3]['close']: 
         vela3 = 1 
     else:
            if data[3]['open'] > data[3]['close']: 
             vela3 = -1
            else: vela3 = 0  
  
  ################################### MODO ENTRADA AL= 0##################################
     if after_loss == 0:
       if modo_entrada >= 2:   
            if data[4]['open'] < data[4]['close']: 
               vela4 = 1 
            else:
                if data[4]['open'] > data[4]['close']: 
                    vela4 = -1
                else: vela4 = 0       
             
       if modo_entrada >= 3:         
            if data[5]['open'] < data[5]['close']: 
                    vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                    vela5 = -1
                else: vela5 = 0
       if modo_entrada >= 4:         
            if data[6]['open'] < data[6]['close']: 
                    vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                    vela6 = -1
                else: vela6 = 0
       if modo_entrada == 5:         
            if data[7]['open'] < data[7]['close']: 
                    vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                    vela7 = -1
                else: vela7 = 0                           

     if after_loss == 1 or after_loss == 2 or after_loss == 3: 
            if data[4]['open'] < data[4]['close']: 
               vela4 = 1 
            else:
                if data[4]['open'] > data[4]['close']: 
                    vela4 = -1
                else: vela4 = 0

            if data[5]['open'] < data[5]['close']: 
              vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                  vela5 = -1
                else: vela5 = 0 
            
            if data[6]['open'] < data[6]['close']: 
              vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                  vela6 = -1
                else: vela6 = 0
   
            if data[7]['open'] < data[7]['close']: 
              vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                  vela7 = -1
                else: vela7 = 0
     
            if data[8]['open'] < data[8]['close']: 
              vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']: 
                  vela8 = -1
                else: vela8 = 0  
         
               
     if after_loss == 1:
       if modo_entrada >= 2:  
         if data[9]['open'] < data[9]['close']: 
            vela9 = 1 
         else:
            if data[9]['open'] > data[9]['close']:
             vela9 = -1
            else: vela9 = 0

       if modo_entrada >= 3:  
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 

       if modo_entrada >= 4: 
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0
        
       if modo_entrada >= 5: 
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0
 
     
     if after_loss == 2 or after_loss == 3: 
         if data[9]['open'] < data[9]['close']: 
            vela9 = 1 
         else:
            if data[9]['open'] > data[9]['close']:
             vela9 = -1
            else: vela9 = 0    
            
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 
        
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0

         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0
       
         if data[13]['open'] < data[13]['close']: 
           vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
               vela13 = -1
            else: vela13 = 0
  

     if after_loss == 2:
       if modo_entrada >= 2:   
         if data[14]['open'] < data[14]['close']: 
           vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
              vela14 = -1
            else: vela14 = 0

       if modo_entrada >= 3:   
         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
       if modo_entrada >= 4: 
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
       if modo_entrada >= 5: 
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
       
     if after_loss == 3:
         if data[14]['open'] < data[14]['close']: 
           vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
              vela14 = -1
            else: vela14 = 0

         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
        
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
        
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
        
         if data[18]['open'] < data[18]['close']: 
            vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
               vela18 = -1
            else: vela18 = 0
         
         if modo_entrada >= 2: 
            if data[19]['open'] < data[19]['close']: 
                vela19 = 1 
            else:
                if data[19]['open'] > data[19]['close']:
                    vela19 = -1
                else: vela19 = 0
         if modo_entrada >= 3:       
             if data[20]['open'] < data[20]['close']: 
                vela20 = 1 
             else:
                if data[20]['open'] > data[20]['close']:
                    vela20 = -1
                else: vela20 = 0 

         if modo_entrada >= 4:  
             if data[21]['open'] < data[21]['close']: 
                vela21 = 1 
             else:
                if data[21]['open'] > data[21]['close']:
                    vela21 = -1
                else: vela21 = 0

         if modo_entrada >= 5:  
             if data[22]['open'] < data[22]['close']: 
                vela22 = 1 
             else:
                if data[22]['open'] > data[22]['close']:
                    vela22 = -1
                else: vela22 = 0

         
    

     if modo_entrada == 0:
            mhi2_entrada = 'go'    
            mhi2mai_entrada = 'go'
            padrao23_entrada = 'go'

     if after_loss == 0:   
        if vela0 == 0 or vela1 == 0 or vela2 == 0:
           mhi2_clave = 404
        else:   
           mhi2_clave = vela0 + vela1 + vela2
        
        if vela3 == 0:
           padrao23_clave = 404
        else:   
           padrao23_clave = vela3
    
     if after_loss == 1:  
        
        mhi2_af1 = vela0 + vela1 + vela2
        padrao23_af1 = vela3

        if vela5 == 0 or vela6 == 0 or vela7 == 0:
           mhi2_clave = 404
        else:   
           mhi2_clave = vela5 + vela6 + vela7
        
        if vela8 == 0:
           padrao23_clave = 404
        else:   
           padrao23_clave = vela8

     if after_loss == 2:  

        mhi2_af1 = vela0 + vela1 + vela2
        padrao23_af1 = vela3

        mhi2_af2 = vela5 + vela6 + vela7
        padrao23_af2 = vela8

        if vela10 == 0 or vela11 == 0 or vela12 == 0:
           mhi2_clave = 404
        else:   
           mhi2_clave = vela10 + vela11 + vela12
        
        if vela13 == 0:
           padrao23_clave = 404
        else:   
           padrao23_clave = vela13

     if after_loss == 3:  

        mhi2_af1 = vela0 + vela1 + vela2
        padrao23_af1 = vela3

        mhi2_af2 = vela5 + vela6 + vela7
        padrao23_af2 = vela8 

        mhi2_af3 = vela10 + vela11 + vela12
        padrao23_af3 = vela13

        if vela15 == 0 or vela16 == 0 or vela17 == 0:
           mhi2_clave = 404
        else:   
           mhi2_clave = vela15 + vela16 + vela17
        
        if vela18 == 0:
           padrao23_clave = 404
        else:   
           padrao23_clave = vela18

    
     if mhi2_clave > 0: 
            option_mhi2 = 'put'
            option_mhi2mai = 'call'
     if mhi2_clave < 0: 
            option_mhi2 = 'call'
            option_mhi2mai = 'put'
     if mhi2_clave == 404: 
            option_mhi2 = 'none' 
            option_mhi2mai = 'none'
     if padrao23_clave > 0: 
            option_padrao23 = 'call'
     if padrao23_clave < 0: 
            option_padrao23 = 'put'
     if padrao23_clave == 404: 
            option_padrao23 = 'none'
         

     if modo_entrada == 2:
       if after_loss == 0:
            if option_mhi2 == 'put' and vela4 > 0: mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela4 < 0: mhi2_entrada = 'go' 
            if option_padrao23 == 'put' and vela4 > 0: padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela4 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela4 > 0: mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela4 < 0: mhi2mai_entrada = 'go' 
               
            if vela3 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
               

       if after_loss == 1:
            if option_mhi2 == 'put' and vela9 > 0: mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela9 < 0: mhi2_entrada = 'go' 
            if option_padrao23 == 'put' and vela9 > 0: padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela9 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela9 > 0: mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela9 < 0: mhi2mai_entrada = 'go' 
               
            if vela9 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
          

       if after_loss == 2:
            if option_mhi2 == 'put' and vela14 > 0: mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela14 < 0: mhi2_entrada = 'go' 
            if option_padrao23 == 'put' and vela14 > 0: padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela14 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela14 > 0: mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela14 < 0: mhi2mai_entrada = 'go' 
                  
            if vela14 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
             

       if after_loss == 3:
            if option_mhi2 == 'put' and vela19> 0: mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela19 < 0: mhi2_entrada = 'go' 
            if option_padrao23 == 'put' and vela19 > 0: padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela19 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela19 > 0: mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela19 < 0: mhi2mai_entrada = 'go' 
                
            if vela19 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
                

     if modo_entrada == 3:
        if after_loss == 0:    
            if option_mhi2 == 'put' and vela4 > 0 and vela5 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela4 < 0 and vela5 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela4 > 0 and vela5 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela4 < 0 and vela5 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela4 > 0 and vela5 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela4 < 0 and vela5 < 0: mhi2mai_entrada = 'go'
        
            if vela4 == 0 or vela5 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
              

        if after_loss == 1:    
            if option_mhi2 == 'put' and vela9 > 0 and vela10 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela9 < 0 and vela10 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela9 > 0 and vela10 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela9 < 0 and vela10 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela9 > 0 and vela10 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela9 < 0 and vela10 < 0: mhi2mai_entrada = 'go'
       
            if vela9 == 0 or vela10 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
        

        if after_loss == 2:    
            if option_mhi2 == 'put' and vela14 > 0 and vela15 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela14 < 0 and vela15 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela14 > 0 and vela15 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela14 < 0 and vela15 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela14 > 0 and vela15 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela14 < 0 and vela15 < 0: mhi2mai_entrada = 'go'
     
            if vela14 == 0 or vela15 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 3:    
            if option_mhi2 == 'put' and vela19 > 0 and vela20 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela19 < 0 and vela20 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela19 > 0 and vela20 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela19 < 0 and vela20 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela19 > 0 and vela20 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela19 < 0 and vela20 < 0: mhi2mai_entrada = 'go'
            
            if vela19 == 0 or vela20 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
               milhaomai_entrada = 'stop'       

 
     if modo_entrada == 4:
        if after_loss == 0:    
            if option_mhi2 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela4 < 0 and vela5 < 0 and vela6 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela4 < 0 and vela5 < 0 and vela6 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela4 < 0 and vela5 < 0 and vela6 < 0: mhi2mai_entrada = 'go'
         
            if vela4 == 0 or vela5 == 0 or vela6 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'

        if after_loss == 1:    
            if option_mhi2 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0: mhi2mai_entrada = 'go'
          
            if vela9 == 0 or vela10 == 0 or vela11 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
           

        if after_loss == 2:    
            if option_mhi2 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0: mhi2mai_entrada = 'go'
           
            if vela14 == 0 or vela15 == 0 or vela16 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
                 

        if after_loss == 3:    
            if option_mhi2 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0: mhi2mai_entrada = 'go'
            
            if vela19 == 0 or vela20 == 0 or vela21 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
               milhaomai_entrada = 'stop'                  


     if modo_entrada == 5:
        if after_loss == 0:    
            if option_mhi2 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0 and vela7 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela4 > 0 and vela5 < 0 and vela6 < 0 and vela7 < 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0 and vela7 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela4 > 0 and vela5 < 0 and vela6 < 0 and vela7 < 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0 and vela7 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call'  and vela4 > 0 and vela5 < 0 and vela6 < 0 and vela7 < 0: mhi2mai_entrada = 'go'
           
            if vela4 == 0 or vela5 == 0 or vela6 == 0 or vela7 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
             

        if after_loss == 1:    
            if option_mhi2 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0 and vela12 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0 and vela12 > 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0 and vela12 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0 and vela12 > 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0 and vela12 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0 and vela12 > 0: mhi2mai_entrada = 'go'
        
            if vela9 == 0 or vela10 == 0 or vela11 == 0 or vela12 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
          

        if after_loss == 2:    
            if option_mhi2 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0 and vela17 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0 and vela17 > 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0 and vela17 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0 and vela17 > 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0 and vela17 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0 and vela17 > 0: mhi2mai_entrada = 'go'
     
            if vela14 == 0 or vela15 == 0 or vela16 == 0 or vela17 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
          

        if after_loss == 3:    
            if option_mhi2 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0 and vela22 > 0:  mhi2_entrada = 'go'
            if option_mhi2 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0 and vela22 > 0: mhi2_entrada = 'go'
            if option_padrao23 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0 and vela22 > 0:  padrao23_entrada = 'go'
            if option_padrao23 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0 and vela22 > 0: padrao23_entrada = 'go'
            if option_mhi2mai == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0 and vela22 > 0:  mhi2mai_entrada = 'go'
            if option_mhi2mai == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0 and vela22 > 0: mhi2mai_entrada = 'go'
            
            if vela19 == 0 or vela20 == 0 or vela21 == 0 or vela22 == 0:
               mhi2_entrada = 'stop'
               mhi2mai_entrada = 'stop'
               padrao23_entrada = 'stop'
      ########################################################################################################                       

     if after_loss > 0:
        if martingala_al == 0:
         if after_loss == 1 or after_loss == 2 or after_loss == 3:
            if mhi2_af1 > 0 and vela4 == 1: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 == -1: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 == 1: after_mhi2mai = "go"
            if mhi2_af1 > 0 and vela4 == -1: after_mhi2mai = "go"
            if padrao23_af1 > 0 and vela4 == -1: after_padrao23 = "go"
            if padrao23_af1 < 0 and vela4 == 1: after_padrao23 = "go"
       
         if after_loss == 2 or after_loss == 3:
            if mhi2_af2 > 0 and vela9 == 1: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 == -1: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 == 1: after_mhi2mai_2 = "go"
            if mhi2_af2 > 0 and vela9 == -1: after_mhi2mai_2 = "go"
            if padrao23_af2 > 0 and vela9 == -1: after_padrao23_2 = "go"
            if padrao23_af2 < 0 and vela9== 1: after_padrao23_2 = "go"
            
         if after_loss == 3:
            if mhi2_af3 > 0 and vela14 == 1: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 == -1: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 == 1: after_mhi2mai_3 = "go"
            if mhi2_af3 > 0 and vela14 == -1: after_mhi2mai_3 = "go"
            if padrao23_af3 > 0 and vela14 == -1: after_padrao23_3 = "go"
            if padrao23_af3 < 0 and vela14 == 1: after_padrao23_3 = "go"
             
        
        if martingala_al == 1:
         if after_loss == 1 or after_loss == 2 :
            if mhi2_af1 > 0 and vela4 + vela5 == 2: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5== -2: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5== 2: after_mhi2mai = "go"
            if mhi2_af1 > 0 and vela4 + vela5== -2: after_mhi2mai = "go"
            if padrao23_af1 > 0 and vela4 + vela5== -2: after_padrao23 = "go"
            if padrao23_af1 < 0 and vela4 + vela5== 2: after_padrao23 = "go"
         
         if after_loss == 2 or after_loss == 3:
            if mhi2_af2 > 0 and vela10 + vela11 == 2: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela10 + vela11== -2: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela10 + vela11== 2: after_mhi2mai_2 = "go"
            if mhi2_af2 > 0 and vela10 + vela11== -2: after_mhi2mai_2 = "go"
            if padrao23_af2 > 0 and vela10 + vela11== -2: after_padrao23 = "go"
            if padrao23_af2 < 0 and vela10 + vela11== 2: after_padrao23 = "go"
            
         if after_loss == 3:
            if mhi2_af3 > 0 and vela14 + vela15== 2: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15== -2: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 == 2: after_mhi2mai_3 = "go"
            if mhi2_af3 > 0 and vela14 + vela15 == -2: after_mhi2mai_3 = "go"
            if padrao23_af3 > 0 and vela14 + vela15 == -2: after_padrao23 = "go"
            if padrao23_af3 < 0 and vela14 + vela15 == 2: after_padrao23 = "go"
              
        
        if martingala_al == 2:
          if after_loss == 1 or after_loss == 2 :
            if mhi2_af1 > 0 and vela4 + vela5 + vela6 == 3: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6== -3: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6== 3: after_mhi2mai = "go"
            if mhi2_af1 > 0 and vela4 + vela5 + vela6== -3: after_mhi2mai = "go"
            if padrao23_af1 > 0 and vela4 + vela5 + vela6== -3: after_padrao23 = "go"
            if padrao23_af1 < 0 and vela4 + vela5 + vela6== 3: after_padrao23 = "go"
            
          if after_loss == 2 or after_loss == 3:
            if mhi2_af2 > 0 and vela9 + vela10 + vela11 == 3: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11== -3: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11== 3: after_mhi2mai_2 = "go"
            if mhi2_af2 > 0 and vela9 + vela10 + vela11== -3: after_mhi2mai_2 = "go"
            if padrao23_af2 > 0 and vela9 + vela10 + vela11== -3: after_padrao23 = "go"
            if padrao23_af2 < 0 and vela9 + vela10 + vela11== 3: after_padrao23 = "go"
          
          if after_loss == 3:
            if mhi2_af3 > 0 and vela14 + vela15 + vela16== 3: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16== -3: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16== 3: after_mhi2mai_3 = "go"
            if mhi2_af3 > 0 and vela14 + vela15 + vela16== -3: after_mhi2mai_3 = "go"
            if padrao23_af3 > 0 and vela14 + vela15 + vela16 == -3: after_padrao23 = "go"
            if padrao23_af3 < 0 and vela14 + vela15 + vela16== 3: after_padrao23 = "go"
         

        if martingala_al == 3:
          if after_loss == 1 or after_loss == 2 :
            if mhi2_af1 > 0 and vela4 + vela5 + vela6 + vela7 == 4: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6 + vela7== -4: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6 + vela7== 4: after_mhi2mai = "go"
            if mhi2_af1 > 0 and vela4 + vela5 + vela6 + vela7== -4: after_mhi2mai = "go"
            if padrao23_af1 > 0 and vela4 + vela5 + vela6 + vela7== -4: after_padrao23 = "go"
            if padrao23_af1 < 0 and vela4 + vela5 + vela6 + vela7== 4: after_padrao23 = "go"
        
          if after_loss == 2 or after_loss == 3:
            if mhi2_af2 > 0 and vela9 + vela10 + vela11 + vela12 == 4: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11 + vela12== -4: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11 + vela12== 4: after_mhi2mai_2 = "go"
            if mhi2_af2 > 0 and vela9 + vela10 + vela11 + vela12== -4: after_mhi2mai_2 = "go"
            if padrao23_af2 > 0 and vela9 + vela10 + vela11 + vela12== -4: after_padrao23 = "go"
            if padrao23_af2 < 0 and vela9 + vela10 + vela11 + vela12== 4: after_padrao23 = "go"
           
          if after_loss == 3:
            if mhi2_af3 > 0 and vela14 + vela15 + vela16 + vela17== 4: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16 + vela17== -4: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16 + vela17== 4: after_mhi2mai_3 = "go"
            if mhi2_af3 > 0 and vela14 + vela15 + vela16 + vela17== -4: after_mhi2mai_3 = "go"
            if padrao23_af3 > 0 and vela14 + vela15 + vela16 + vela17 == -4: after_padrao23 = "go"
            if padrao23_af3 < 0 and vela14 + vela15 + vela16 + vela17== 4: after_padrao23 = "go"
           

        if martingala_al == 4:
         if after_loss == 1 or after_loss == 2 :
            if mhi2_af1 > 0 and vela4 + vela5 + vela6 + vela7 + vela8 == 5: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6 + vela7 + vela8== -5: after_mhi2 = "go"
            if mhi2_af1 < 0 and vela4 + vela5 + vela6 + vela7 + vela8== 5: after_mhi2mai = "go"
            if mhi2_af1 > 0 and vela4 + vela5 + vela6 + vela7 + vela8== -5: after_mhi2mai = "go"
            if padrao23_af1 > 0 and vela4 + vela5 + vela6 + vela7 + vela8== -5: after_padrao23 = "go"
            if padrao23_af1 < 0 and vela4 + vela5 + vela6 + vela7 + vela8== 5: after_padrao23 = "go"
     
         if after_loss == 2 or after_loss == 3:
            if mhi2_af2 > 0 and vela9 + vela10 + vela11 + vela12 + vela13 == 5: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11 + vela12 + vela13== -5: after_mhi2_2 = "go"
            if mhi2_af2 < 0 and vela9 + vela10 + vela11 + vela12 + vela13== 5: after_mhi2mai_2 = "go"
            if mhi2_af2 > 0 and vela9 + vela10 + vela11 + vela12 + vela13== -5: after_mhi2mai_2 = "go"
            if padrao23_af2 > 0 and vela9 + vela10 + vela11 + vela12 + vela13== -5: after_padrao23 = "go"
            if padrao23_af2 < 0 and vela9 + vela10 + vela11 + vela12 + vela13== 5: after_padrao23 = "go"
            
         if after_loss == 3:
            if mhi2_af3 > 0 and vela14 + vela15 + vela16 + vela17 + vela18== 5: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16 + vela17 + vela18== -5: after_mhi2_3 = "go"
            if mhi2_af3 < 0 and vela14 + vela15 + vela16 + vela17 + vela18== 5: after_mhi2mai_3 = "go"
            if mhi2_af3 > 0 and vela14 + vela15 + vela16 + vela17 + vela18== -5: after_mhi2mai_3 = "go"
            if padrao23_af3 > 0 and vela14 + vela15 + vela16 + vela17 + vela18 == -5: after_padrao23 = "go"
            if padrao23_af3 < 0 and vela14 + vela15 + vela16 + vela17 + vela18== 5: after_padrao23 = "go"
          

        
     if after_loss == 0: 
        enter_mhi2 = "go"  
        enter_mhi2mai = "go" 
        enter_padrao23 = "go" 
       
     if after_loss == 1:  
        if after_mhi2 == "go": enter_mhi2 = "go"
        if after_mhi2mai == "go": enter_mhi2mai = "go"
        if after_padrao23== "go": enter_padrao23 = "go"
      
     if after_loss == 2:  
        if after_mhi2 == "go" and after_mhi2_2 == "go": enter_mhi2 = "go"
        if after_mhi2mai == "go" and after_mhi2mai_2 == "go": enter_mhi2mai = "go"
        if after_padrao23 == "go" and after_padrao23_2 == "go": enter_padrao23 = "go"

     if after_loss == 3:  
        if after_mhi2 == "go" and after_mhi2_2 == "go" and after_mhi2_3 == "go": enter_mhi2 = "go"
        if after_mhi2mai == "go" and after_mhi2mai_2 == "go" and after_mhi2mai_3 == "go": enter_mhi2mai = "go"
        if after_padrao23 == "go" and after_padrao23_2 == "go" and after_padrao23_3 == "go": enter_padrao23 = "go"
 
     
     if after_loss > 0 and operaciones_al > 0:
        if paso_mhi2 == True:
           enter_mhi2 = 'go'
        if enter_mhi2 == 'go':
           paso_mhi2 = True
           count_mhi2 = count_mhi2 + 1
        if count_mhi2 > operaciones_al:
           paso_mhi2 = False
           enter_mhi2 = 'none' 
           count_mhi2 = 0  

     ######################################################################################################## 
    if indicador_tecnico == "on": 
        try:
                if conteo_sell >= 14 and conteo_buy <= 5:
                        if option_mhi2 == "call": option_mhi2 = "none"
                        if option_mhi2mai == "call": option_mhi2mai = "none"
                        if option_padrao23 == "call": option_padrao23 = "none"
  
                else:        

                    if conteo_buy >= 14 and conteo_sell <= 5:
                            if option_mhi2 == "put": option_mhi2 = "none"
                            if option_mhi2mai == "put": option_mhi2mai = "none"
                            if option_padrao23 == "put": option_padrao23 = "none" 
                    else:
                            option_mhi2 = "none" 
                            option_mhi2mai = "none" 
                            option_padrao23 = "none"  
                            
        except: pass

    for i in divisa:                                             
            if i['estrategia'] == "MHI2" and enter_mhi2 == 'go' and option_mhi2 != 'none' and mhi2_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhi2_turbo = threading.Thread(target=turbo_mhi2, args=(money,i['divisa'], option_mhi2,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhi2_turbo.start() 
                                           
            if i['estrategia'] == "MHI2 Mayoría" and enter_mhi2mai == 'go' and option_mhi2mai != 'none' and mhi2mai_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhi2mai_turbo = threading.Thread(target=turbo_mhimai2, args=(money,i['divisa'], option_mhi2mai,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhi2mai_turbo.start() 
                         
            if i['estrategia'] == "Padrão 23" and enter_padrao23 == 'go' and option_padrao23 != 'none' and padrao23_entrada == 'go' and n77 < ntime: 
                            n77 = n77 + 1
                            hilo_padrao23_turbo = threading.Thread(target=turbo_milhao2, args=(money,i['divisa'], option_padrao23,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_padrao23_turbo.start() 
                   
           
    if ntime <= n77:
       stop_advice = 'active'    
 ##################################################################################################################################################################################

def minuto2_7(pares,divisa,money,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador_tecnico):
 global stop_all
 stop_all = False
 global estatus_lista
 estatus_lista = []
 global stop_gain_advice
 global stop_loss_advice
 global num_advice
 global stop_advice
 global ganadas
 global perdidas
 global n77
 stop_gain_advice = "none"
 stop_loss_advice = "none"
 num_advice = "none"
 stop_advice = "none"
 n77 = 0
 add = 0
 add2 = 0
 count_mhi3 = 0
 paso_mhi3 = False
 if modo_entrada == 0 or modo_entrada == 1: add = 0
 if modo_entrada == 2: 
     add = 1
     add2 = 9
 if modo_entrada == 3: 
     add = 2
     add2 = 8
 if modo_entrada == 4:
     add = 3
     add2 = 7
 if modo_entrada == 5: 
     add = 4
     add2 = 6

 if after_loss == 0: add_al = 0
 if after_loss == 1: add_al = 5
 if after_loss == 2: add_al = 10
 if after_loss == 3: add_al = 15

 while n77 < ntime:
   
    opcion_mhi3 = "none"
    opcion_mhi3mai = "none"
    opcion_melhor = "none"

    after_mhi3 = "stop" 
    after_mhi3_2 = "stop"
    after_mhi3_3 = "stop"
    enter_mhi3 = "stop"
    after_mhi3mai = "stop" 
    after_mhi3mai_2 = "stop"
    after_mhi3mai_3 = "stop"
    enter_mhi3mai = "stop"
    after_melhor = "stop" 
    after_melhor_2 = "stop"
    after_melhor_3 = "stop"
    enter_melhor = "stop"
    

    mhi3_entrada = 'stop'
    mhi3mai_entrada = 'stop'
    melhor_entrada = 'stop'
    

    while True:
            now = datetime.now()
            s = format(now.second)
            m = format(now.minute)
            m_ = int(m)
            ultimo_digito = m_ % 10
            if ultimo_digito == 1 + add  or ultimo_digito == 6 + add: 
                if s == "50": 
                    if indicador_tecnico == "on":   
                        try:      
                                tecnicos = []
                                asset= pares[0]
                                indicators = api.get_technical_indicators(asset)
                                for indicator in indicators:
                                    if indicator['name'] == 'Simple Moving Average (10)' or indicator['name'] == 'Relative Strength Index (14)' or indicator['name'] == 'Stochastic %K (14, 3, 3)' or indicator['name'] == 'Exponential Moving Average (5)':   
                                        tecnicos.append(indicator['action']) 

                                conteo_sell = tecnicos.count('sell')
                                conteo_buy = tecnicos.count('buy')
                                conteo_hold = tecnicos.count('hold') 
                        except:pass           
                    break  
            if stop_all == True:
               break  
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break   
            time.sleep(0.3)

    while True:
            now = datetime.now()
            s = format(now.second)
            if s == "0": 
               break 
            if stop_all == True:
               break 
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break        
            time.sleep(0.1)  
  
    if stop_all == True:
        break
    if stop_loss <= perdidas and stop_loss > 0:
               stop_loss_advice = 'active'  
               break   
    if stop_gain <= ganadas and stop_gain > 0:
               stop_gain_advice = 'active'  
               break

    for par in pares:  
     minuto_antes = datetime.now() - timedelta(minutes=1)
     data = api.get_candles(par,60,6 + add + add_al,datetime.timestamp(minuto_antes))

     if data[0]['open'] < data[0]['close']: 
      vela0 = 1 
     else:
        if data[0]['open'] > data[0]['close']: 
          vela0 = -1
        else: vela0 = 0  
    
     if data[1]['open'] < data[1]['close']: 
      vela1 = 1 
     else:
        if data[1]['open'] > data[1]['close']: 
           vela1 = -1
        else: vela1 = 0   

     if data[2]['open'] < data[2]['close']: 
      vela2 = 1 
     else:
        if data[2]['open'] > data[2]['close']:
           vela2 = -1
        else: vela2 = 0  

     if data[3]['open'] < data[3]['close']: 
         vela3 = 1 
     else:
        if data[3]['open'] > data[3]['close']: 
            vela3 = -1
        else: vela3 = 0  
     
     if data[4]['open'] < data[4]['close']: 
               vela6 = 1 
     else:
        if data[4]['open'] > data[4]['close']: 
            vela6 = -1
        else: vela6 = 0


     if data[5]['open'] < data[5]['close']: 
                    vela5 = 1 
     else:
        if data[5]['open'] > data[5]['close']:
            vela5 = -1
        else: vela5 = 0 

  ################################### MODO ENTRADA AL= 0##################################
     if after_loss == 0:
       if modo_entrada >= 2:   
            if data[6]['open'] < data[6]['close']: 
                    vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                    vela6 = -1
                else: vela6 = 0       
             
       if modo_entrada >= 3:         
            if data[7]['open'] < data[7]['close']: 
                    vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                    vela7 = -1
                else: vela7 = 0
       if modo_entrada >= 4:         
            if data[8]['open'] < data[8]['close']: 
              vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']: 
                  vela8 = -1
                else: vela8 = 0
       if modo_entrada == 5:         
            if data[9]['open'] < data[9]['close']: 
                    vela9 = 1 
            else:
                if data[9]['open'] > data[9]['close']:
                    vela9 = -1
                else: vela9 = 0                           

     if after_loss == 1 or after_loss == 2 or after_loss == 3:  
            
            if data[6]['open'] < data[6]['close']: 
              vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                  vela6 = -1
                else: vela6 = 0
   
            if data[7]['open'] < data[7]['close']: 
              vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                  vela7 = -1
                else: vela7 = 0
     
            if data[8]['open'] < data[8]['close']: 
              vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']: 
                  vela8 = -1
                else: vela8 = 0  

            if data[9]['open'] < data[9]['close']: 
               vela9 = 1 
            else:
                if data[9]['open'] > data[9]['close']: 
                    vela9 = -1
                else: vela9 = 0

            if data[10]['open'] < data[10]['close']: 
              vela10 = 1 
            else:
                if data[10]['open'] > data[10]['close']:
                  vela10 = -1
                else: vela10 = 0    
         
               
     if after_loss == 1:
       if modo_entrada >= 2:  
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
             vela11 = -1
            else: vela11 = 0

       if modo_entrada >= 3:  
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
             vela12 = -1
            else: vela12 = 0 

       if modo_entrada >= 4: 
         if data[13]['open'] < data[13]['close']: 
            vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
              vela13 = -1
            else: vela13 = 0
        
       if modo_entrada >= 5: 
         if data[14]['open'] < data[14]['close']: 
            vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
               vela14 = -1
            else: vela14 = 0
 
    
     if after_loss == 2 or after_loss == 3:  
        
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0

        
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0

       
         if data[13]['open'] < data[13]['close']: 
           vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
               vela13 = -1
            else: vela13 = 0

         if data[14]['open'] < data[14]['close']: 
            vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
             vela14 = -1
            else: vela14 = 0    
            
         if data[15]['open'] < data[15]['close']: 
            vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
             vela15 = -1
            else: vela15 = 0   
  

     if after_loss == 2:
       
       if modo_entrada >= 2: 
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0

       if modo_entrada >= 3: 
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0

       if modo_entrada >= 4:   
         if data[18]['open'] < data[18]['close']: 
           vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
              vela18 = -1
            else: vela18 = 0

       if modo_entrada >= 5:   
         if data[19]['open'] < data[19]['close']: 
           vela19 = 1 
         else:
            if data[19]['open'] > data[19]['close']:
              vela19 = -1
            else: vela19 = 0      
       

     if after_loss == 3: 
        
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
        
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
        
         if data[18]['open'] < data[18]['close']: 
            vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
               vela18 = -1
            else: vela18 = 0
         
         if data[19]['open'] < data[19]['close']: 
               vela19 = 1 
         else:
                if data[19]['open'] > data[19]['close']:
                   vela19 = -1
                else: vela19 = 0 

         if data[20]['open'] < data[20]['close']: 
           vela20 = 1 
         else:
            if data[20]['open'] > data[20]['close']:
              vela20 = -1
            else: vela20 = 0 

         if modo_entrada >= 4:  
             if data[21]['open'] < data[21]['close']: 
                vela21 = 1 
             else:
                if data[21]['open'] > data[21]['close']:
                    vela21 = -1
                else: vela21 = 0

         if modo_entrada >= 5:  
             if data[22]['open'] < data[22]['close']: 
                vela22 = 1 
             else:
                if data[22]['open'] > data[22]['close']:
                    vela22 = -1
                else: vela22 = 0

         if modo_entrada >= 2: 
            if data[23]['open'] < data[23]['close']: 
                vela23 = 1 
            else:
                if data[23]['open'] > data[23]['close']:
                    vela23 = -1
                else: vela23 = 0

         if modo_entrada >= 3:       
             if data[24]['open'] < data[24]['close']: 
                vela24 = 1 
             else:
                if data[24]['open'] > data[24]['close']:
                    vela24 = -1
                else: vela24 = 0
    

     if modo_entrada == 0:
            mhi3_entrada = 'go'    
            mhi3mai_entrada = 'go'
            melhor_entrada = 'go'

     if after_loss == 0:   
        if vela1 == 0 or vela2 == 0 or vela3 == 0:
           mhi3_clave = 404
        else:   
           mhi3_clave = vela1 + vela2 + vela3
        
        if vela0 == 0 or vela1 == 0 or vela2 == 0:
           melhor_clave = 404
        else:   
           melhor_clave = vela0 + vela1 + vela2
    
     if after_loss == 1:  
        
        mhi3_af1 = vela1 + vela2 + vela3
        melhor_af1 = vela0 + vela1 + vela2

        if vela6 == 0 or vela7 == 0 or vela8 == 0:
           mhi3_clave = 404
        else:   
           mhi3_clave = vela6 + vela7 + vela8
        
        if vela5 == 0 or vela6 == 0 or vela7 == 0:
           melhor_clave = 404
        else:   
           melhor_clave = vela5 + vela6 + vela7

     if after_loss == 2:  

        mhi3_af1 = vela1 + vela2 + vela3
        melhor_af1 = vela0 + vela1 + vela2

        mhi3_af2 = vela6 + vela7 + vela8
        melhor_af2 = vela5 + vela6 + vela7

        if vela11 == 0 or vela12 == 0 or vela13 == 0:
           mhi3_clave = 404
        else:   
           mhi3_clave = vela11 + vela12 + vela13
        
        if vela10 + vela11 + vela12 == 0:
           melhor_clave = 404
        else:   
           melhor_clave = vela10 + vela11 + vela12

     if after_loss == 3:  

        mhi3_af1 = vela1 + vela2 + vela3
        melhor_af1 = vela0 + vela1 + vela2

        mhi3_af2 = vela6 + vela7 + vela8
        melhor_af2 = vela5 + vela6 + vela7 

        mhi3_af3 = vela11 + vela12 + vela13
        melhor_af3 = vela10 + vela11 + vela12

        if vela16 == 0 or vela17 == 0 or vela18 == 0:
           mhi3_clave = 404
        else:   
           mhi3_clave = vela16 + vela17 + vela18
        
        if vela15 == 0 or vela16 == 0 or vela17 == 0:
           melhor_clave = 404
        else:   
           melhor_clave = vela15 + vela16 + vela17

    
     if mhi3_clave > 0: 
            option_mhi3 = 'put'
            option_mhi3mai = 'call'
     if mhi3_clave < 0: 
            option_mhi3 = 'call'
            option_mhi3mai = 'put'
     if mhi3_clave == 404: 
            option_mhi3 = 'none' 
            option_mhi3mai = 'none'
     if melhor_clave > 0: 
            option_melhor = 'call'
     if melhor_clave < 0: 
            option_melhor = 'put'
     if melhor_clave == 404: 
            option_melhor = 'none'
         

     if modo_entrada == 2:
       if after_loss == 0:
            if option_mhi3 == 'put' and vela6 > 0: mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela6 < 0: mhi3_entrada = 'go' 
            if option_melhor == 'put' and vela6 > 0: melhor_entrada = 'go'
            if option_melhor == 'call' and vela6 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela6 > 0: mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela6 < 0: mhi3mai_entrada = 'go' 
               
            if vela1 == 0 or vela2 == 0 or vela3 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
            if vela0 == 0 or vela1 == 0 or vela2 == 0:   
               melhor_entrada = 'stop'
               

       if after_loss == 1:
            if option_mhi3 == 'put' and vela11 > 0: mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela11 < 0: mhi3_entrada = 'go' 
            if option_melhor == 'put' and vela11 > 0: melhor_entrada = 'go'
            if option_melhor == 'call' and vela11 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela11 > 0: mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela11 < 0: mhi3mai_entrada = 'go' 
               
            if vela11 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
          

       if after_loss == 2:
            if option_mhi3 == 'put' and vela16 > 0: mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela16 < 0: mhi3_entrada = 'go' 
            if option_melhor == 'put' and vela16 > 0: melhor_entrada = 'go'
            if option_melhor == 'call' and vela16 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela16 > 0: mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela16 < 0: mhi3mai_entrada = 'go' 
                  
            if vela16 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
             

       if after_loss == 3:
            if option_mhi3 == 'put' and vela21> 0: mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela21 < 0: mhi3_entrada = 'go' 
            if option_melhor == 'put' and vela21 > 0: melhor_entrada = 'go'
            if option_melhor == 'call' and vela21 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela21 > 0: mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela21 < 0: mhi3mai_entrada = 'go' 
                
            if vela19 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
                

     if modo_entrada == 3:
        if after_loss == 0:    
            if option_mhi3 == 'put' and vela6 > 0 and vela7 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela6 < 0 and vela7 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela6 > 0 and vela7 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela6 < 0 and vela7 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela6 > 0 and vela7 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela6 < 0 and vela7 < 0: mhi3mai_entrada = 'go'
        
            if vela6 == 0 or vela7 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
              

        if after_loss == 1:    
            if option_mhi3 == 'put' and vela11 > 0 and vela12 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela11 < 0 and vela12 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela11 > 0 and vela12 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela11 < 0 and vela12 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela11 > 0 and vela12 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela11 < 0 and vela12 < 0: mhi3mai_entrada = 'go'
       
            if vela11 == 0 or vela12 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
        

        if after_loss == 2:    
            if option_mhi3 == 'put' and vela16 > 0 and vela17 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela16 < 0 and vela17 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela16 > 0 and vela17 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela16 < 0 and vela17 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela16 > 0 and vela17 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela16 < 0 and vela17 < 0: mhi3mai_entrada = 'go'
     
            if vela16 == 0 or vela17 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 3:    
            if option_mhi3 == 'put' and vela21 > 0 and vela22 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela21 < 0 and vela22 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela21 > 0 and vela22 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela21 < 0 and vela22 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela21 > 0 and vela22 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela21 < 0 and vela22 < 0: mhi3mai_entrada = 'go'
            
            if vela21 == 0 or vela22 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
               milhaomai_entrada = 'stop'       

 
     if modo_entrada == 4:
        if after_loss == 0:    
            if option_mhi3 == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela6 < 0 and vela7 < 0 and vela8 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela6 < 0 and vela7 < 0 and vela8 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela6 < 0 and vela7 < 0 and vela8 < 0: mhi3mai_entrada = 'go'
         
            if vela6 == 0 or vela7 == 0 or vela8 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'

        if after_loss == 1:    
            if option_mhi3 == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0: mhi3mai_entrada = 'go'
          
            if vela11 == 0 or vela12 == 0 or vela13 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
           

        if after_loss == 2:    
            if option_mhi3 == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0: mhi3mai_entrada = 'go'
           
            if vela16 == 0 or vela17 == 0 or vela18 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
                 

        if after_loss == 3:    
            if option_mhi3 == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0: mhi3mai_entrada = 'go'
            
            if vela21 == 0 or vela22 == 0 or vela23 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
               milhaomai_entrada = 'stop'                  


     if modo_entrada == 5:
        if after_loss == 0:    
            if option_mhi3 == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0 and vela9 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela6 > 0 and vela7 < 0 and vela8 < 0 and vela9 < 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0 and vela9 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela6 > 0 and vela7 < 0 and vela8 < 0 and vela9 < 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela6 > 0 and vela7 > 0 and vela8 > 0 and vela9 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call'  and vela6 > 0 and vela7 < 0 and vela8 < 0 and vela9 < 0: mhi3mai_entrada = 'go'
           
            if vela6 == 0 or vela7 == 0 or vela8 == 0 or vela9 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
             

        if after_loss == 1:    
            if option_mhi3 == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0 and vela14 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0 and vela14 > 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0 and vela14 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0 and vela14 > 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela11 > 0 and vela12 > 0 and vela13 > 0 and vela14 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela11 < 0 and vela12 < 0 and vela13 < 0 and vela14 > 0: mhi3mai_entrada = 'go'
        
            if vela11 == 0 or vela12 == 0 or vela13 == 0 or vela14 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
          

        if after_loss == 2:    
            if option_mhi3 == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0 and vela19 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0 and vela19 > 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0 and vela19 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0 and vela19 > 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela16 > 0 and vela17 > 0 and vela18 > 0 and vela19 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela16 < 0 and vela17 < 0 and vela18 < 0 and vela19 > 0: mhi3mai_entrada = 'go'
     
            if vela16 == 0 or vela17 == 0 or vela18 == 0 or vela19 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
          

        if after_loss == 3:    
            if option_mhi3 == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0 and vela24 > 0:  mhi3_entrada = 'go'
            if option_mhi3 == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0 and vela24 > 0: mhi3_entrada = 'go'
            if option_melhor == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0 and vela24 > 0:  melhor_entrada = 'go'
            if option_melhor == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0 and vela24 > 0: melhor_entrada = 'go'
            if option_mhi3mai == 'put' and vela21 > 0 and vela22 > 0 and vela23 > 0 and vela24 > 0:  mhi3mai_entrada = 'go'
            if option_mhi3mai == 'call' and vela21 < 0 and vela22 < 0 and vela23 < 0 and vela24 > 0: mhi3mai_entrada = 'go'
            
            if vela21 == 0 or vela22 == 0 or vela23 == 0 or vela24 == 0:
               mhi3_entrada = 'stop'
               mhi3mai_entrada = 'stop'
               melhor_entrada = 'stop'
      ########################################################################################################                       

     if after_loss > 0:
        if martingala_al == 0:
         if after_loss == 1 or after_loss == 2 or after_loss == 3:
            if mhi3_af1 > 0 and vela6 == 1: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 == -1: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 == 1: after_mhi3mai = "go"
            if mhi3_af1 > 0 and vela6 == -1: after_mhi3mai = "go"
            if melhor_af1 > 0 and vela6 == -1: after_melhor = "go"
            if melhor_af1 < 0 and vela6 == 1: after_melhor = "go"
       
         if after_loss == 2 or after_loss == 3:
            if mhi3_af2 > 0 and vela11 == 1: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 == -1: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 == 1: after_mhi3mai_2 = "go"
            if mhi3_af2 > 0 and vela11 == -1: after_mhi3mai_2 = "go"
            if melhor_af2 > 0 and vela11 == -1: after_melhor_2 = "go"
            if melhor_af2 < 0 and vela11== 1: after_melhor_2 = "go"
            
         if after_loss == 3:
            if mhi3_af3 > 0 and vela16 == 1: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 == -1: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 == 1: after_mhi3mai_3 = "go"
            if mhi3_af3 > 0 and vela16 == -1: after_mhi3mai_3 = "go"
            if melhor_af3 > 0 and vela16 == -1: after_melhor_3 = "go"
            if melhor_af3 < 0 and vela16 == 1: after_melhor_3 = "go"
             
        
        if martingala_al == 1:
         if after_loss == 1 or after_loss == 2 :
            if mhi3_af1 > 0 and vela6 + vela7 == 2: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7== -2: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7== 2: after_mhi3mai = "go"
            if mhi3_af1 > 0 and vela6 + vela7== -2: after_mhi3mai = "go"
            if melhor_af1 > 0 and vela6 + vela7== -2: after_melhor = "go"
            if melhor_af1 < 0 and vela6 + vela7== 2: after_melhor = "go"
         
         if after_loss == 2 or after_loss == 3:
            if mhi3_af2 > 0 and vela12 + vela13 == 2: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela12 + vela13== -2: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela12 + vela13== 2: after_mhi3mai_2 = "go"
            if mhi3_af2 > 0 and vela12 + vela13== -2: after_mhi3mai_2 = "go"
            if melhor_af2 > 0 and vela12 + vela13== -2: after_melhor = "go"
            if melhor_af2 < 0 and vela12 + vela13== 2: after_melhor = "go"
            
         if after_loss == 3:
            if mhi3_af3 > 0 and vela16 + vela17== 2: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17== -2: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 == 2: after_mhi3mai_3 = "go"
            if mhi3_af3 > 0 and vela16 + vela17 == -2: after_mhi3mai_3 = "go"
            if melhor_af3 > 0 and vela16 + vela17 == -2: after_melhor = "go"
            if melhor_af3 < 0 and vela16 + vela17 == 2: after_melhor = "go"
              
        
        if martingala_al == 2:
          if after_loss == 1 or after_loss == 2 :
            if mhi3_af1 > 0 and vela6 + vela7 + vela8 == 3: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8== -3: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8== 3: after_mhi3mai = "go"
            if mhi3_af1 > 0 and vela6 + vela7 + vela8== -3: after_mhi3mai = "go"
            if melhor_af1 > 0 and vela6 + vela7 + vela8== -3: after_melhor = "go"
            if melhor_af1 < 0 and vela6 + vela7 + vela8== 3: after_melhor = "go"
            
          if after_loss == 2 or after_loss == 3:
            if mhi3_af2 > 0 and vela11 + vela12 + vela13 == 3: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13== -3: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13== 3: after_mhi3mai_2 = "go"
            if mhi3_af2 > 0 and vela11 + vela12 + vela13== -3: after_mhi3mai_2 = "go"
            if melhor_af2 > 0 and vela11 + vela12 + vela13== -3: after_melhor = "go"
            if melhor_af2 < 0 and vela11 + vela12 + vela13== 3: after_melhor = "go"
          
          if after_loss == 3:
            if mhi3_af3 > 0 and vela16 + vela17 + vela18== 3: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18== -3: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18== 3: after_mhi3mai_3 = "go"
            if mhi3_af3 > 0 and vela16 + vela17 + vela18== -3: after_mhi3mai_3 = "go"
            if melhor_af3 > 0 and vela16 + vela17 + vela18 == -3: after_melhor = "go"
            if melhor_af3 < 0 and vela16 + vela17 + vela18== 3: after_melhor = "go"
         

        if martingala_al == 3:
          if after_loss == 1 or after_loss == 2 :
            if mhi3_af1 > 0 and vela6 + vela7 + vela8 + vela9 == 4: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8 + vela9== -4: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8 + vela9== 4: after_mhi3mai = "go"
            if mhi3_af1 > 0 and vela6 + vela7 + vela8 + vela9== -4: after_mhi3mai = "go"
            if melhor_af1 > 0 and vela6 + vela7 + vela8 + vela9== -4: after_melhor = "go"
            if melhor_af1 < 0 and vela6 + vela7 + vela8 + vela9== 4: after_melhor = "go"
        
          if after_loss == 2 or after_loss == 3:
            if mhi3_af2 > 0 and vela11 + vela12 + vela13 + vela14 == 4: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13 + vela14== -4: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13 + vela14== 4: after_mhi3mai_2 = "go"
            if mhi3_af2 > 0 and vela11 + vela12 + vela13 + vela14== -4: after_mhi3mai_2 = "go"
            if melhor_af2 > 0 and vela11 + vela12 + vela13 + vela14== -4: after_melhor = "go"
            if melhor_af2 < 0 and vela11 + vela12 + vela13 + vela14== 4: after_melhor = "go"
           
          if after_loss == 3:
            if mhi3_af3 > 0 and vela16 + vela17 + vela18 + vela19== 4: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18 + vela19== -4: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18 + vela19== 4: after_mhi3mai_3 = "go"
            if mhi3_af3 > 0 and vela16 + vela17 + vela18 + vela19== -4: after_mhi3mai_3 = "go"
            if melhor_af3 > 0 and vela16 + vela17 + vela18 + vela19 == -4: after_melhor = "go"
            if melhor_af3 < 0 and vela16 + vela17 + vela18 + vela19== 4: after_melhor = "go"
           

        if martingala_al == 4:
         if after_loss == 1 or after_loss == 2 :
            if mhi3_af1 > 0 and vela6 + vela7 + vela8 + vela9 + vela10 == 5: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8 + vela9 + vela10== -5: after_mhi3 = "go"
            if mhi3_af1 < 0 and vela6 + vela7 + vela8 + vela9 + vela10== 5: after_mhi3mai = "go"
            if mhi3_af1 > 0 and vela6 + vela7 + vela8 + vela9 + vela10== -5: after_mhi3mai = "go"
            if melhor_af1 > 0 and vela6 + vela7 + vela8 + vela9 + vela10== -5: after_melhor = "go"
            if melhor_af1 < 0 and vela6 + vela7 + vela8 + vela9 + vela10== 5: after_melhor = "go"
     
         if after_loss == 2 or after_loss == 3:
            if mhi3_af2 > 0 and vela11 + vela12 + vela13 + vela14 + vela15 == 5: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13 + vela14 + vela15== -5: after_mhi3_2 = "go"
            if mhi3_af2 < 0 and vela11 + vela12 + vela13 + vela14 + vela15== 5: after_mhi3mai_2 = "go"
            if mhi3_af2 > 0 and vela11 + vela12 + vela13 + vela14 + vela15== -5: after_mhi3mai_2 = "go"
            if melhor_af2 > 0 and vela11 + vela12 + vela13 + vela14 + vela15== -5: after_melhor = "go"
            if melhor_af2 < 0 and vela11 + vela12 + vela13 + vela14 + vela15== 5: after_melhor = "go"
            
         if after_loss == 3:
            if mhi3_af3 > 0 and vela16 + vela17 + vela18 + vela19 + vela20== 5: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18 + vela19 + vela20== -5: after_mhi3_3 = "go"
            if mhi3_af3 < 0 and vela16 + vela17 + vela18 + vela19 + vela20== 5: after_mhi3mai_3 = "go"
            if mhi3_af3 > 0 and vela16 + vela17 + vela18 + vela19 + vela20== -5: after_mhi3mai_3 = "go"
            if melhor_af3 > 0 and vela16 + vela17 + vela18 + vela19 + vela20 == -5: after_melhor = "go"
            if melhor_af3 < 0 and vela16 + vela17 + vela18 + vela19 + vela20== 5: after_melhor = "go"
          

        
     if after_loss == 0: 
        enter_mhi3 = "go"  
        enter_mhi3mai = "go" 
        enter_melhor = "go" 
       
     if after_loss == 1:  
        if after_mhi3 == "go": enter_mhi3 = "go"
        if after_mhi3mai == "go": enter_mhi3mai = "go"
        if after_melhor== "go": enter_melhor = "go"
      
     if after_loss == 2:  
        if after_mhi3 == "go" and after_mhi3_2 == "go": enter_mhi3 = "go"
        if after_mhi3mai == "go" and after_mhi3mai_2 == "go": enter_mhi3mai = "go"
        if after_melhor == "go" and after_melhor_2 == "go": enter_melhor = "go"

     if after_loss == 3:  
        if after_mhi3 == "go" and after_mhi3_2 == "go" and after_mhi3_3 == "go": enter_mhi3 = "go"
        if after_mhi3mai == "go" and after_mhi3mai_2 == "go" and after_mhi3mai_3 == "go": enter_mhi3mai = "go"
        if after_melhor == "go" and after_melhor_2 == "go" and after_melhor_3 == "go": enter_melhor = "go"
 
     
     if after_loss > 0 and operaciones_al > 0:
        if paso_mhi3 == True:
           enter_mhi3 = 'go'
        if enter_mhi3 == 'go':
           paso_mhi3 = True
           count_mhi3 = count_mhi3 + 1
        if count_mhi3 > operaciones_al:
           paso_mhi3 = False
           enter_mhi3 = 'none' 
           count_mhi3 = 0  

     ######################################################################################################## 
    if indicador_tecnico == "on": 
        try:
                if conteo_sell >= 14 and conteo_buy <= 5:
                        if option_mhi3 == "call": option_mhi3 = "none"
                        if option_mhi3mai == "call": option_mhi3mai = "none"
                        if option_melhor == "call": option_melhor = "none"
                   
                else:        

                    if conteo_buy >= 14 and conteo_sell <= 5:
                            if option_mhi3 == "put": option_mhi3 = "none"
                            if option_mhi3mai == "put": option_mhi3mai = "none"
                            if option_melhor == "put": option_melhor = "none"
                        
                    else:
                            option_mhi3 = "none" 
                            option_mhi3mai = "none" 
                            option_melhor = "none"  
                            
        except: pass

    for i in divisa:                                             
            if i['estrategia'] == "MHI3" and enter_mhi3 == 'go' and option_mhi3 != 'none' and mhi3_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhi3_turbo = threading.Thread(target=turbo_mhi3, args=(money,i['divisa'], option_mhi3,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhi3_turbo.start() 
                                           
            if i['estrategia'] == "MHI3 Mayoría" and enter_mhi3mai == 'go' and option_mhi3mai != 'none' and mhi3mai_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_mhi3mai_turbo = threading.Thread(target=turbo_mhimai3, args=(money,i['divisa'], option_mhi3mai,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_mhi3mai_turbo.start() 
                         
            if i['estrategia'] == "Melhor de 3" and enter_melhor == 'go' and option_melhor != 'none' and melhor_entrada == 'go' and n77 < ntime: 
                            n77 = n77 + 1
                            hilo_melhor_turbo = threading.Thread(target=turbo_milhao3, args=(money,i['divisa'], option_melhor,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_melhor_turbo.start() 
                   
    if ntime <= n77:
       stop_advice = 'active'

                               
 ###########################################################################################################################################################################   

def minuto4_9(pares,divisa,money,comision,martingala,tipo_martingala,modo_entrada,after_loss,martingala_al,ntime,operaciones_al,stop_gain,stop_loss,indicador_tecnico):
 global stop_all
 stop_all = False
 global estatus_lista
 estatus_lista = []
 global stop_gain_advice
 global stop_loss_advice
 global num_advice
 global stop_advice
 global ganadas
 global perdidas
 global n77
 stop_gain_advice = "none"
 stop_loss_advice = "none"
 num_advice = "none"
 stop_advice = "none"
 n77 = 0
 add = 0
 add2 = 0
 count_torres = 0
 paso_torres = False
 if modo_entrada == 0 or modo_entrada == 1: add = 0
 if modo_entrada == 2: 
     add = 1
     add2 = 9
 if modo_entrada == 3: 
     add = 2
     add2 = 8
 if modo_entrada == 4:
     add = 3
     add2 = 7
 if modo_entrada == 5: 
     add = 4
     add2 = 6

 if after_loss == 0: add_al = 0
 if after_loss == 1: add_al = 5
 if after_loss == 2: add_al = 10
 if after_loss == 3: add_al = 15

 while n77 < ntime:
   
    opcion_torres = "none"
    opcion_padrao3x1 = "none"

    after_torres = "stop" 
    after_torres_2 = "stop"
    after_torres_3 = "stop"
    enter_torres = "stop"

    after_padrao3x1 = "stop" 
    after_padrao3x1_2 = "stop"
    after_padrao3x1_3 = "stop"
    enter_padrao3x1 = "stop"
    

    torres_entrada = 'stop'
    padrao3x1_entrada = 'stop'
    

    while True:
            now = datetime.now()
            s = format(now.second)
            m = format(now.minute)
            m_ = int(m)
            ultimo_digito = m_ % 10
            if ultimo_digito == 3 + add  or ultimo_digito == 8 + add: 
                if s == "50": 
                    if indicador_tecnico == "on":   
                        try:      
                                tecnicos = []
                                asset= pares[0]
                                indicators = api.get_technical_indicators(asset)
                                for indicator in indicators:
                                    if indicator['name'] == 'Simple Moving Average (10)' or indicator['name'] == 'Relative Strength Index (14)' or indicator['name'] == 'Stochastic %K (14, 3, 3)' or indicator['name'] == 'Exponential Moving Average (5)':   
                                        tecnicos.append(indicator['action']) 

                                conteo_sell = tecnicos.count('sell')
                                conteo_buy = tecnicos.count('buy')
                                conteo_hold = tecnicos.count('hold') 
                        except:pass           
                    break  
            if stop_all == True:
               break  
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break   
            time.sleep(0.3)

    while True:
            now = datetime.now()
            s = format(now.second)
            if s == "0": 
               break 
            if stop_all == True:
               break 
            if stop_loss <= perdidas and stop_loss > 0:
               break   
            if stop_gain <= ganadas and stop_gain > 0:
               break        
            time.sleep(0.1)  
  
    if stop_all == True:
        break
    if stop_loss <= perdidas and stop_loss > 0:
               stop_loss_advice = 'active'  
               break   
    if stop_gain <= ganadas and stop_gain > 0:
               stop_gain_advice = 'active'  
               break

    for par in pares:  
     minuto_antes = datetime.now() - timedelta(minutes=1)
     data = api.get_candles(par,60,4 + add + add_al,datetime.timestamp(minuto_antes))

     if data[0]['open'] < data[0]['close']: 
      vela0 = 1 
     else:
        if data[0]['open'] > data[0]['close']: 
          vela0 = -1
        else: vela0 = 0  
    
     if data[1]['open'] < data[1]['close']: 
      vela1 = 1 
     else:
        if data[1]['open'] > data[1]['close']: 
           vela1 = -1
        else: vela1 = 0   

     if data[2]['open'] < data[2]['close']: 
      vela2 = 1 
     else:
        if data[2]['open'] > data[2]['close']:
           vela2 = -1
        else: vela2 = 0  

     if data[3]['open'] < data[3]['close']: 
         vela3 = 1 
     else:
            if data[3]['open'] > data[3]['close']: 
             vela3 = -1
            else: vela3 = 0  
  
  ################################### MODO ENTRADA AL= 0##################################
     if after_loss == 0:
       if modo_entrada >= 2:   
            if data[4]['open'] < data[4]['close']: 
               vela4 = 1 
            else:
                if data[4]['open'] > data[4]['close']: 
                    vela4 = -1
                else: vela4 = 0       
             
       if modo_entrada >= 3:         
            if data[5]['open'] < data[5]['close']: 
                    vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                    vela5 = -1
                else: vela5 = 0
       if modo_entrada >= 4:         
            if data[6]['open'] < data[6]['close']: 
                    vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                    vela6 = -1
                else: vela6 = 0
       if modo_entrada == 5:         
            if data[7]['open'] < data[7]['close']: 
                    vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                    vela7 = -1
                else: vela7 = 0                           

     if after_loss == 1 or after_loss == 2 or after_loss == 3: 
            if data[4]['open'] < data[4]['close']: 
               vela4 = 1 
            else:
                if data[4]['open'] > data[4]['close']: 
                    vela4 = -1
                else: vela4 = 0

            if data[5]['open'] < data[5]['close']: 
              vela5 = 1 
            else:
                if data[5]['open'] > data[5]['close']:
                  vela5 = -1
                else: vela5 = 0 
            
            if data[6]['open'] < data[6]['close']: 
              vela6 = 1 
            else:
                if data[6]['open'] > data[6]['close']:
                  vela6 = -1
                else: vela6 = 0
   
            if data[7]['open'] < data[7]['close']: 
              vela7 = 1 
            else:
                if data[7]['open'] > data[7]['close']:
                  vela7 = -1
                else: vela7 = 0
     
            if data[8]['open'] < data[8]['close']: 
              vela8 = 1 
            else:
                if data[8]['open'] > data[8]['close']: 
                  vela8 = -1
                else: vela8 = 0  
         
               
     if after_loss == 1:
       if modo_entrada >= 2:  
         if data[9]['open'] < data[9]['close']: 
            vela9 = 1 
         else:
            if data[9]['open'] > data[9]['close']:
             vela9 = -1
            else: vela9 = 0

       if modo_entrada >= 3:  
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 

       if modo_entrada >= 4: 
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0
        
       if modo_entrada >= 5: 
         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0
 
     
     if after_loss == 2 or after_loss == 3: 
         if data[9]['open'] < data[9]['close']: 
            vela9 = 1 
         else:
            if data[9]['open'] > data[9]['close']:
             vela9 = -1
            else: vela9 = 0    
            
         if data[10]['open'] < data[10]['close']: 
            vela10 = 1 
         else:
            if data[10]['open'] > data[10]['close']:
             vela10 = -1
            else: vela10 = 0 
        
         if data[11]['open'] < data[11]['close']: 
            vela11 = 1 
         else:
            if data[11]['open'] > data[11]['close']:
              vela11 = -1
            else: vela11 = 0

         if data[12]['open'] < data[12]['close']: 
            vela12 = 1 
         else:
            if data[12]['open'] > data[12]['close']:
               vela12 = -1
            else: vela12 = 0
       
         if data[13]['open'] < data[13]['close']: 
           vela13 = 1 
         else:
            if data[13]['open'] > data[13]['close']:
               vela13 = -1
            else: vela13 = 0
  

     if after_loss == 2:
       if modo_entrada >= 2:   
         if data[14]['open'] < data[14]['close']: 
           vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
              vela14 = -1
            else: vela14 = 0

       if modo_entrada >= 3:   
         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
       if modo_entrada >= 4: 
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
       if modo_entrada >= 5: 
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
       
     if after_loss == 3:
         if data[14]['open'] < data[14]['close']: 
           vela14 = 1 
         else:
            if data[14]['open'] > data[14]['close']:
              vela14 = -1
            else: vela14 = 0

         if data[15]['open'] < data[15]['close']: 
           vela15 = 1 
         else:
            if data[15]['open'] > data[15]['close']:
              vela15 = -1
            else: vela15 = 0 
        
         if data[16]['open'] < data[16]['close']: 
           vela16 = 1 
         else:
            if data[16]['open'] > data[16]['close']:
               vela16 = -1
            else: vela16 = 0
        
         if data[17]['open'] < data[17]['close']: 
            vela17 = 1 
         else:
            if data[17]['open'] > data[17]['close']:
                vela17 = -1
            else: vela17 = 0
        
         if data[18]['open'] < data[18]['close']: 
            vela18 = 1 
         else:
            if data[18]['open'] > data[18]['close']:
               vela18 = -1
            else: vela18 = 0
         
         if modo_entrada >= 2: 
            if data[19]['open'] < data[19]['close']: 
                vela19 = 1 
            else:
                if data[19]['open'] > data[19]['close']:
                    vela19 = -1
                else: vela19 = 0
         if modo_entrada >= 3:       
             if data[20]['open'] < data[20]['close']: 
                vela20 = 1 
             else:
                if data[20]['open'] > data[20]['close']:
                    vela20 = -1
                else: vela20 = 0 

         if modo_entrada >= 4:  
             if data[21]['open'] < data[21]['close']: 
                vela21 = 1 
             else:
                if data[21]['open'] > data[21]['close']:
                    vela21 = -1
                else: vela21 = 0

         if modo_entrada >= 5:  
             if data[22]['open'] < data[22]['close']: 
                vela22 = 1 
             else:
                if data[22]['open'] > data[22]['close']:
                    vela22 = -1
                else: vela22 = 0

         
    

     if modo_entrada == 0:
            torres_entrada = 'go'    
            padrao3x1_entrada = 'go'

     if after_loss == 0:   
        if vela0 == 0:
           torres_clave = 404
        else:   
           torres_clave = vela0
        
        if vela0 == 0 or vela1 == 0 or vela2 == 0:
           padrao3x1_clave = 404
        else:   
           padrao3x1_clave = vela0 + vela1 + vela2
    
     if after_loss == 1:  
        
        torres_af1 = vela0 
        padrao3x1_af1 = vela0 + vela1 + vela2

        if vela5 == 0:
           torres_clave = 404
        else:   
           torres_clave = vela5 
        
        if vela5 == 0 or vela6 == 0 or vela7 == 0:
           padrao3x1_clave = 404
        else:   
           padrao3x1_clave = vela5 + vela6 + vela7

     if after_loss == 2:  

        torres_af1 = vela0
        padrao3x1_af1 = vela0 + vela1 + vela2

        torres_af2 = vela5
        padrao3x1_af2 = vela5 + vela6 + vela7

        if vela10 == 0:
           torres_clave = 404
        else:   
           torres_clave = vela10 
        
        if vela10 == 0 or vela11 == 0 or vela12 == 0:
           padrao3x1_clave = 404
        else:   
           padrao3x1_clave = vela10 + vela11 + vela12

     if after_loss == 3:  

        torres_af1 = vela0
        padrao3x1_af1 = vela0 + vela1 + vela2

        torres_af2 = vela5
        padrao3x1_af2 = vela5 + vela6 + vela7 

        torres_af3 = vela10
        padrao3x1_af3 = vela10 + vela11 + vela12

        if vela15 == 0:
           torres_clave = 404
        else:   
           torres_clave = vela15 
        
        if vela15 == 0 or vela16 == 0 or vela17 == 0:
           padrao3x1_clave = 404
        else:   
           padrao3x1_clave = vela15 + vela16 + vela17

    
     if torres_clave > 0: 
            option_torres = 'call'
     if torres_clave < 0: 
            option_torres = 'put'
     if torres_clave == 404: 
            option_torres = 'none' 
     if padrao3x1_clave > 0: 
            option_padrao3x1 = 'put'
     if padrao3x1_clave < 0: 
            option_padrao3x1 = 'call'
     if padrao3x1_clave == 404: 
            option_padrao3x1 = 'none'
         

     if modo_entrada == 2:
       if after_loss == 0:
            if option_torres == 'put' and vela4 > 0: torres_entrada = 'go'
            if option_torres == 'call' and vela4 < 0: torres_entrada = 'go' 
            if option_padrao3x1 == 'put' and vela4 > 0: padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela4 < 0: padrao3x1_entrada = 'go'

               
            if vela3 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
               
       if after_loss == 1:
            if option_torres == 'put' and vela9 > 0: torres_entrada = 'go'
            if option_torres == 'call' and vela9 < 0: torres_entrada = 'go' 
            if option_padrao3x1 == 'put' and vela9 > 0: padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela9 < 0: padrao3x1_entrada = 'go'
               
            if vela9 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
          

       if after_loss == 2:
            if option_torres == 'put' and vela14 > 0: torres_entrada = 'go'
            if option_torres == 'call' and vela14 < 0: torres_entrada = 'go' 
            if option_padrao3x1 == 'put' and vela14 > 0: padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela14 < 0: padrao3x1_entrada = 'go'
           
                  
            if vela14 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'

       if after_loss == 3:
            if option_torres == 'put' and vela19> 0: torres_entrada = 'go'
            if option_torres == 'call' and vela19 < 0: torres_entrada = 'go' 
            if option_padrao3x1 == 'put' and vela19 > 0: padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela19 < 0: padrao3x1_entrada = 'go' 
                
            if vela19 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
                

     if modo_entrada == 3:
        if after_loss == 0:    
            if option_torres == 'put' and vela4 > 0 and vela5 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela4 < 0 and vela5 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela4 > 0 and vela5 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela4 < 0 and vela5 < 0: padrao3x1_entrada = 'go'

            if vela4 == 0 or vela5 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
              

        if after_loss == 1:    
            if option_torres == 'put' and vela9 > 0 and vela10 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela9 < 0 and vela10 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela9 > 0 and vela10 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela9 < 0 and vela10 < 0: padrao3x1_entrada = 'go'
       
            if vela9 == 0 or vela10 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
        

        if after_loss == 2:    
            if option_torres == 'put' and vela14 > 0 and vela15 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela14 < 0 and vela15 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela14 > 0 and vela15 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela14 < 0 and vela15 < 0: padrao3x1_entrada = 'go'

            if vela14 == 0 or vela15 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
               milhaomai_entrada = 'stop'

        if after_loss == 3:    
            if option_torres == 'put' and vela19 > 0 and vela20 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela19 < 0 and vela20 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela19 > 0 and vela20 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela19 < 0 and vela20 < 0: padrao3x1_entrada = 'go'

            if vela19 == 0 or vela20 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
               milhaomai_entrada = 'stop'       

 
     if modo_entrada == 4:
        if after_loss == 0:    
            if option_torres == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela4 < 0 and vela5 < 0 and vela6 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela4 < 0 and vela5 < 0 and vela6 < 0: padrao3x1_entrada = 'go'
         
            if vela4 == 0 or vela5 == 0 or vela6 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'

        if after_loss == 1:    
            if option_torres == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0: padrao3x1_entrada = 'go'
          
            if vela9 == 0 or vela10 == 0 or vela11 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
           

        if after_loss == 2:    
            if option_torres == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0: padrao3x1_entrada = 'go'
           
            if vela14 == 0 or vela15 == 0 or vela16 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
                 

        if after_loss == 3:    
            if option_torres == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0: padrao3x1_entrada = 'go'
            
            if vela19 == 0 or vela20 == 0 or vela21 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
               milhaomai_entrada = 'stop'                  


     if modo_entrada == 5:
        if after_loss == 0:    
            if option_torres == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0 and vela7 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela4 > 0 and vela5 < 0 and vela6 < 0 and vela7 < 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela4 > 0 and vela5 > 0 and vela6 > 0 and vela7 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela4 > 0 and vela5 < 0 and vela6 < 0 and vela7 < 0: padrao3x1_entrada = 'go'
           
            if vela4 == 0 or vela5 == 0 or vela6 == 0 or vela7 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
             

        if after_loss == 1:    
            if option_torres == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0 and vela12 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0 and vela12 > 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela9 > 0 and vela10 > 0 and vela11 > 0 and vela12 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela9 < 0 and vela10 < 0 and vela11 < 0 and vela12 > 0: padrao3x1_entrada = 'go'
        
            if vela9 == 0 or vela10 == 0 or vela11 == 0 or vela12 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
          

        if after_loss == 2:    
            if option_torres == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0 and vela17 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0 and vela17 > 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela14 > 0 and vela15 > 0 and vela16 > 0 and vela17 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela14 < 0 and vela15 < 0 and vela16 < 0 and vela17 > 0: padrao3x1_entrada = 'go'
     
            if vela14 == 0 or vela15 == 0 or vela16 == 0 or vela17 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
          

        if after_loss == 3:    
            if option_torres == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0 and vela22 > 0:  torres_entrada = 'go'
            if option_torres == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0 and vela22 > 0: torres_entrada = 'go'
            if option_padrao3x1 == 'put' and vela19 > 0 and vela20 > 0 and vela21 > 0 and vela22 > 0:  padrao3x1_entrada = 'go'
            if option_padrao3x1 == 'call' and vela19 < 0 and vela20 < 0 and vela21 < 0 and vela22 > 0: padrao3x1_entrada = 'go'
            
            if vela19 == 0 or vela20 == 0 or vela21 == 0 or vela22 == 0:
               torres_entrada = 'stop'
               torresmai_entrada = 'stop'
               padrao3x1_entrada = 'stop'
      ########################################################################################################                       

     if after_loss > 0:
        if martingala_al == 0:
         if after_loss == 1 or after_loss == 2 or after_loss == 3:
            if torres_af1 > 0 and vela4 == -1: after_torres = "go"
            if torres_af1 < 0 and vela4 == 1: after_torres = "go"
            if padrao3x1_af1 > 0 and vela4 == 1: after_padrao3x1 = "go"
            if padrao3x1_af1 < 0 and vela4 == -1: after_padrao3x1 = "go"
       
         if after_loss == 2 or after_loss == 3:
            if torres_af2 > 0 and vela9 == -1: after_torres_2 = "go"
            if torres_af2 < 0 and vela9 == 1: after_torres_2 = "go"
            if padrao3x1_af2 > 0 and vela9 == 1: after_padrao3x1_2 = "go"
            if padrao3x1_af2 < 0 and vela9== -1: after_padrao3x1_2 = "go"
            
         if after_loss == 3:
            if torres_af3 > 0 and vela14 == -1: after_torres_3 = "go"
            if torres_af3 < 0 and vela14 == 1: after_torres_3 = "go"
            if padrao3x1_af3 > 0 and vela14 == 1: after_padrao3x1_3 = "go"
            if padrao3x1_af3 < 0 and vela14 == -1: after_padrao3x1_3 = "go"
             
        
        if martingala_al == 1:
         if after_loss == 1 or after_loss == 2 :
            if torres_af1 > 0 and vela4 + vela5 == -2: after_torres = "go"
            if torres_af1 < 0 and vela4 + vela5== 2: after_torres = "go"
            if padrao3x1_af1 > 0 and vela4 + vela5== 2: after_padrao3x1 = "go"
            if padrao3x1_af1 < 0 and vela4 + vela5== -2: after_padrao3x1 = "go"
         
         if after_loss == 2 or after_loss == 3:
            if torres_af2 > 0 and vela9 + vela10 == -2: after_torres_2 = "go"
            if torres_af2 < 0 and vela9 + vela10== 2: after_torres_2 = "go"
            if padrao3x1_af2 > 0 and vela9 + vela10== 2: after_padrao3x1 = "go"
            if padrao3x1_af2 < 0 and vela9 + vela10== -2: after_padrao3x1 = "go"
            
         if after_loss == 3:
            if torres_af3 > 0 and vela14 + vela15== -2: after_torres_3 = "go"
            if torres_af3 < 0 and vela14 + vela15== 2: after_torres_3 = "go"
            if padrao3x1_af3 > 0 and vela14 + vela15 == 2: after_padrao3x1 = "go"
            if padrao3x1_af3 < 0 and vela14 + vela15 == -2: after_padrao3x1 = "go"
              
        
        if martingala_al == 2:
          if after_loss == 1 or after_loss == 2 :
            if torres_af1 > 0 and vela4 + vela5 + vela6 == -3: after_torres = "go"
            if torres_af1 < 0 and vela4 + vela5 + vela6== 3: after_torres = "go"
            if padrao3x1_af1 > 0 and vela4 + vela5 + vela6== 3: after_padrao3x1 = "go"
            if padrao3x1_af1 < 0 and vela4 + vela5 + vela6== -3: after_padrao3x1 = "go"
            
          if after_loss == 2 or after_loss == 3:
            if torres_af2 > 0 and vela9 + vela10 + vela11 == -3: after_torres_2 = "go"
            if torres_af2 < 0 and vela9 + vela10 + vela11== 3: after_torres_2 = "go"
            if padrao3x1_af2 > 0 and vela9 + vela10 + vela11== 3: after_padrao3x1 = "go"
            if padrao3x1_af2 < 0 and vela9 + vela10 + vela11== -3: after_padrao3x1 = "go"
          
          if after_loss == 3:
            if torres_af3 > 0 and vela14 + vela15 + vela16== -3: after_torres_3 = "go"
            if torres_af3 < 0 and vela14 + vela15 + vela16== 3: after_torres_3 = "go"
            if padrao3x1_af3 > 0 and vela14 + vela15 + vela16 == 3: after_padrao3x1 = "go"
            if padrao3x1_af3 < 0 and vela14 + vela15 + vela16== -3: after_padrao3x1 = "go"
         

        if martingala_al == 3:
          if after_loss == 1 or after_loss == 2 :
            if torres_af1 > 0 and vela4 + vela5 + vela6 + vela7 == -4: after_torres = "go"
            if torres_af1 < 0 and vela4 + vela5 + vela6 + vela7== 4: after_torres = "go"
            if padrao3x1_af1 > 0 and vela4 + vela5 + vela6 + vela7== 4: after_padrao3x1 = "go"
            if padrao3x1_af1 < 0 and vela4 + vela5 + vela6 + vela7== -4: after_padrao3x1 = "go"
        
          if after_loss == 2 or after_loss == 3:
            if torres_af2 > 0 and vela9 + vela10 + vela11 + vela12 == -4: after_torres_2 = "go"
            if torres_af2 < 0 and vela9 + vela10 + vela11 + vela12== 4: after_torres_2 = "go"
            if padrao3x1_af2 > 0 and vela9 + vela10 + vela11 + vela12== 4: after_padrao3x1 = "go"
            if padrao3x1_af2 < 0 and vela9 + vela10 + vela11 + vela12== -4: after_padrao3x1 = "go"
           
          if after_loss == 3:
            if torres_af3 > 0 and vela14 + vela15 + vela16 + vela17== -4: after_torres_3 = "go"
            if torres_af3 < 0 and vela14 + vela15 + vela16 + vela17== 4: after_torres_3 = "go"
            if padrao3x1_af3 > 0 and vela14 + vela15 + vela16 + vela17 == 4: after_padrao3x1 = "go"
            if padrao3x1_af3 < 0 and vela14 + vela15 + vela16 + vela17== -4: after_padrao3x1 = "go"
           

        if martingala_al == 4:
         if after_loss == 1 or after_loss == 2 :
            if torres_af1 > 0 and vela4 + vela5 + vela6 + vela7 + vela8 == -5: after_torres = "go"
            if torres_af1 < 0 and vela4 + vela5 + vela6 + vela7 + vela8== 5: after_torres = "go"
            if padrao3x1_af1 > 0 and vela4 + vela5 + vela6 + vela7 + vela8== 5: after_padrao3x1 = "go"
            if padrao3x1_af1 < 0 and vela4 + vela5 + vela6 + vela7 + vela8== -5: after_padrao3x1 = "go"
     
         if after_loss == 2 or after_loss == 3:
            if torres_af2 > 0 and vela9 + vela10 + vela11 + vela12 + vela13 == -5: after_torres_2 = "go"
            if torres_af2 < 0 and vela9 + vela10 + vela11 + vela12 + vela13== 5: after_torres_2 = "go"
            if padrao3x1_af2 > 0 and vela9 + vela10 + vela11 + vela12 + vela13== 5: after_padrao3x1 = "go"
            if padrao3x1_af2 < 0 and vela9 + vela10 + vela11 + vela12 + vela13== -5: after_padrao3x1 = "go"
            
         if after_loss == 3:
            if torres_af3 > 0 and vela14 + vela15 + vela16 + vela17 + vela18== -5: after_torres_3 = "go"
            if torres_af3 < 0 and vela14 + vela15 + vela16 + vela17 + vela18== 5: after_torres_3 = "go"
            if padrao3x1_af3 > 0 and vela14 + vela15 + vela16 + vela17 + vela18 == 5: after_padrao3x1 = "go"
            if padrao3x1_af3 < 0 and vela14 + vela15 + vela16 + vela17 + vela18== -5: after_padrao3x1 = "go"
          

        
     if after_loss == 0: 
        enter_torres = "go"  
        enter_padrao3x1 = "go" 
       
     if after_loss == 1:  
        if after_torres == "go": enter_torres = "go"
        if after_padrao3x1== "go": enter_padrao3x1 = "go"
      
     if after_loss == 2:  
        if after_torres == "go" and after_torres_2 == "go": enter_torres = "go"
        if after_padrao3x1 == "go" and after_padrao3x1_2 == "go": enter_padrao3x1 = "go"

     if after_loss == 3:  
        if after_torres == "go" and after_torres_2 == "go" and after_torres_3 == "go": enter_torres = "go"
        if after_padrao3x1 == "go" and after_padrao3x1_2 == "go" and after_padrao3x1_3 == "go": enter_padrao3x1 = "go"
 
     
     if after_loss > 0 and operaciones_al > 0:
        if paso_torres == True:
           enter_torres = 'go'
        if enter_torres == 'go':
           paso_torres = True
           count_torres = count_torres + 1
        if count_torres > operaciones_al:
           paso_torres = False
           enter_torres = 'none' 
           count_torres = 0  


     ######################################################################################################## 
    if indicador_tecnico == "on": 
        try:
                if conteo_sell >= 14 and conteo_buy <= 5:
                        if option_torres == "call": option_torres = "none"
                        if option_padrao3x1 == "call": option_padrao3x1 = "none"
                else:        

                    if conteo_buy >= 14 and conteo_sell <= 5:
                            if option_torres == "put": option_mhi2 = "none"
                            if option_padrao3x1 == "put": option_padrao3x1 = "none"
                         
                    else:
                            option_torres = "none" 
                            option_padrao3x1 = "none" 
                            
                            
        except: pass

    for i in divisa:                                             
            if i['estrategia'] == "Torres Gemelas" and enter_torres == 'go' and option_torres != 'none' and torres_entrada == 'go' and n77 < ntime:
                            n77 = n77 + 1               
                            hilo_torres_turbo = threading.Thread(target=turbo_mhi4, args=(money,i['divisa'], option_torres,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_torres_turbo.start() 
                                           
                         
            if i['estrategia'] == "Padrão 3x1" and enter_padrao3x1 == 'go' and option_padrao3x1 != 'none' and padrao3x1_entrada == 'go' and n77 < ntime: 
                            n77 = n77 + 1
                            hilo_padrao3x1_turbo = threading.Thread(target=turbo_milhao4, args=(money,i['divisa'], option_padrao3x1,martingala,tipo_martingala,comision,i['estrategia']))
                            hilo_padrao3x1_turbo.start() 
                   
           
    if ntime <= n77:
       stop_advice = 'active'    
 ##################################################################################################################################################################################

   
def turbo_mhi(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia,periodo):
          global current_user 
          global api
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id1 = api.buy(money,divisa,opcion,periodo)
               
            check_status = api.check_win_v4(id1)  
            if check_status[0] == "win": 
                estado = "Win" 
                if estrategia != 'señales':           
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                    historial.save() 
                break          
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    if estrategia != 'señales':
                        historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                        historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))           

                else:
                    estado = "Equal" 
                    if estrategia != 'señales':       
                        historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                        historial.save()
                    break

            i = i + 1 
            if(i>martingala):
               break           
                
def turbo_mhimai(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id2 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id2)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()   
                break       
            else:
                if check_status[0] == "loose":
                    money_back = money
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                 
                break

def turbo_milhao(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id3 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id3)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()  
                break         
            else:
                if check_status[0] == "loose":
                    money_back = money
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_milhaomai(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          global modo_cuenta
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id4 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id4)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()    
                break        
            else:
                if check_status[0] == "loose":
                    money_back = money
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):           
                break                                   


def turbo_mhi2(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id12 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id12)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()     
                break       
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_mhimai2(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id22 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id22)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()       
                break     
            else:
                if check_status[0] == "loose":
                    money_back = money
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):            
                break

def turbo_milhao2(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id32 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id32)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()  
                break          
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_milhaomai2(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          global modo_cuenta
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id42 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id42)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()    
                break        
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break
   
   
def turbo_mhi3(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          global modo_cuenta
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id13 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id13)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save() 
                break           
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_mhimai3(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          global modo_cuenta
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id23 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id23)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()    
                break        
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break 

def turbo_milhao3(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id33 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id33)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()  
                break          
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_milhaomai3(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop_all
          global modo_cuenta
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id43 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id43)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()      
                break      
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break


def turbo_mhi4(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id14 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id14)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()    
                break        
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_mhimai4(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id24 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id24)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()  
                break          
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break  

def turbo_milhao4(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global modo_cuenta
          global stop_all
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop_all == True: break
            check, id34 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id34)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()        
                break    
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break

def turbo_milhaomai4(money,divisa,opcion,martingala,tipo_martingala,comision,estrategia):
          global current_user 
          global stop
          formula = 0
          i = 0
          
          while i <= martingala:
            if stop == True: break
            check, id44 = api.buy(money,divisa,opcion,1)
               
            check_status = api.check_win_v4(id44)  
            if check_status[0] == "win": 
                estado = "Win"            
                historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money*(comision/100),martingala=i,estado=estado,estrategia=estrategia,fecha = timezone.now())
                historial.save()    
                break        
            else:
                if check_status[0] == "loose":
                    estado = "Loose"
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=money,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    if tipo_martingala == 'double':
                       formula = ((money * (comision/100)) - 1)
                       money = ((money + formula + 1) / (comision/100))
                    if tipo_martingala == 'single':
                       formula = (money * (comision/100)) 
                       money = ((money + formula) / (comision/100))   

                else:
                    estado = "Equal"        
                    historial = Historial(user=current_user,modo=modo_cuenta,divisa=divisa,ganancia=0,martingala=i,estado=estado,estrategia=estrategia,fecha=timezone.now())
                    historial.save()
                    break
            i = i + 1 
            if(i>martingala):          
                break
               
########################################################################   PAYPAL  ########################################################################

###########################################################################################################################################################
User._meta.get_field('email')._unique = True

@csrf_exempt
def conectar(request):
  global api
  global modo_cuenta
  balance = {}
  credenciales2 = request.body
  credenciales = json.loads(credenciales2) 
  email = credenciales["email"]
  password = credenciales["password"]
  mode = credenciales["modo"]
  modo_cuenta = mode
  api = IQ_Option(email, password)
  
  status, reason = api.connect()
  if reason == "2FA": 
                    
                    return JsonResponse({"mensaje":'2FA'})
  else:
                    
        if status:     
                    api.change_balance(mode)       
                    balance2 = api.get_balance()   
                    balance['estado'] = "Online" 
                    balance['modo'] = credenciales["modo"] 
                    balance['balance'] = balance2
                    api.get_server_timestamp()  
                    return JsonResponse({"balance":balance})
        else: return JsonResponse({"balance":'error'}) 
       
@csrf_exempt
def conectar2(request):
  global modo_cuenta
  global api
  balance = {}
  credenciales2 = request.body
  credenciales = json.loads(credenciales2) 
  codigo = credenciales.get("codigo")
  mode = credenciales.get("modo")
  modo_cuenta = mode
  status, reason = api.connect_2fa(codigo)
  
  if status:
        api.change_balance(mode)
        balance2 = api.get_balance()   
        balance['estado'] = "Online" 
        balance['modo'] = credenciales["modo"] 
        balance['balance'] = balance2
        api.get_server_timestamp()  
        return JsonResponse({"balance":balance})
  else: return JsonResponse({"balance":'error'}) 

@login_required
def foro(request, filtro):
    cantidad = Cliente.objects.all().count()
    cantidad = 5732 + cantidad
    if filtro == "fecha":
       mensajes = Foro.objects.all().order_by('-fecha').values()
    elif filtro == "voto":   
       mensajes = Foro.objects.all().order_by('-voto').values()
    else: mensajes = Foro.objects.all()   
    now = datetime.now()
    anual = str(now.year)
    mes = str(now.month)
    dia = str(now.day)
    fecha = anual+'-'+mes+'-'+dia

    if request.method == 'POST':
        form = ForoForm(request.POST)
        request.POST._mutable = True
        request.POST['username'] = request.user.username
        request.POST['fecha'] = fecha
        request.POST._mutable = False
        if form.is_valid():
           form.save()
           return redirect('/foro/bot')
        
    total = len(mensajes)
    return render(request, 'foro.html', {'datos':mensajes,'total':total,'cantidad':cantidad})

@csrf_exempt
def respuesta(request):
    form = RespuestaForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
    respuestas = Respuesta.objects.all() 
    respuestas_json = list(respuestas.values())
    return JsonResponse({'respuestas':respuestas_json})  

@csrf_exempt
def voto(request):
    id_foro = request.POST['foro_id']
    votos = Voto.objects.filter(foro_id = id_foro).values()
    votos2 = votos.filter(username = request.user)
    
    form = VotoForm(request.POST or None)

    if form.is_valid():
      if len(votos2) == 0:  
        instance = form.save(commit=False)
        instance.save()

    votos_json = len(votos)
    return JsonResponse({'votos':votos_json})

@csrf_exempt
def get_info(request):
   id_info = request.body
   id_foro = json.loads(id_info) 
   try:
        votos = Voto.objects.filter(foro_id = id_foro).values()
        votos_json = len(votos) 

        respuestas = Respuesta.objects.filter(foro_id = id_foro).values()
        respuestas_json = len(respuestas)

        if id_foro > 0:
            p = Foro.objects.get(pk=id_foro)
            p.voto= votos_json
            p.save()
   except:pass         

   return JsonResponse({'votos':votos_json, 'respuestas':respuestas_json})
   
@csrf_exempt
def get_respuestas(request):
    id_info = request.body
    id_foro = json.loads(id_info) 
    respuestas = Respuesta.objects.filter(foro_id = id_foro).values()
    respuestas_json = list(respuestas)
    return JsonResponse({'respuestas':respuestas_json})
          
def bienvenida(request):
      return render(request, 'bienvenida.html')    

def instancia():
    user = get_user()
    if user.is_authenticated:
        return api
     
def salir(request):
    stop('_request')
    logout(request)
    return redirect("/login-page")    






