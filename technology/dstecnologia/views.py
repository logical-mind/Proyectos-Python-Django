from django.shortcuts import render, redirect
from dstecnologia.models import estudiantes, calificacion, grado
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import registerForm, calificaciones
from django.contrib.auth.models import User, Group
from django.http import JsonResponse
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests

def index(request):
    
    return render(request, "dstecnologia/index.html")

def rnc(request, rnc):
     
        url = 'https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx'

        headers = {
            'Host': 'www.dgii.gov.do',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Accept': '*/*',
            'Accept-Language': 'es-ES,es;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-MicrosoftAjax': 'Delta=true',
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'Origin': 'https://www.dgii.gov.do',
            'Connection': 'keep-alive',
            'Referer': 'https://www.dgii.gov.do/app/WebApps/ConsultasWeb/consultas/rnc.aspx',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Pragma': 'no-cache',
        }

        data = {
        
        "ctl00$smMain":	"ctl00$cphMain$upBusqueda|ctl00$cphMain$btnBuscarPorRNC",
        "ctl00$cphMain$txtRNCCedula":	rnc,
        "ctl00$cphMain$txtRazonSocial":	"",
        "__EVENTTARGET":"",
        "__EVENTARGUMENT":	"",
        "__VIEWSTATE":	"/wEPDwUKMTkxNDA2Nzc4Nw9kFgJmD2QWAgIBD2QWAgIDD2QWAmYPZBYCAgEPZBYEAgEPDxYIHgRUZXh0BTpObyBzZSBlbmNvbnRyYXJvbiBkYXRvcyByZWdpc3RyYWRvcyBkZSBlc3RlIGNvbnRyaWJ1eWVudGUuHghDc3NDbGFzcwUTbGFiZWwgbGFiZWwtd2FybmluZx4EXyFTQgICHgdWaXNpYmxlZ2RkAgUPFgIeBXN0eWxlBQ1kaXNwbGF5Ok5vbmU7FggCAQ8WAh8EBQ1kaXNwbGF5Ok5vbmU7ZAIDDxYCHwQFDWRpc3BsYXk6Tm9uZTtkAgUPPCsADwIADxYEHgtfIURhdGFCb3VuZGceC18hSXRlbUNvdW50ZmQKEBYEZgIBAgMCBBYEPCsABQEAFgIeCkhlYWRlclRleHQFC0PDqWR1bGEvUk5DPCsABQEAFgIfBwUUTm9tYnJlL1JhesOzbiBTb2NpYWw8KwAFAQAWAh8HBQpDYXRlZ29yw61hPCsABQEAFgIfBwURUsOpZ2ltZW4gZGUgcGFnb3MWBGZmZmZkAgcPPCsADQEADxYCHwNoZGQYAgUfY3RsMDAkY3BoTWFpbiRndkJ1c2NSYXpvblNvY2lhbA9nZAUjY3RsMDAkY3BoTWFpbiRkdkRhdG9zQ29udHJpYnV5ZW50ZXMPZ2S/MyBq0UWtfRBrcaCuie/HHkV4Lw==",
        "__EVENTVALIDATION":	"/wEWBQLwg/G3CgLqq//bBAKC/r/9AwKhwMi7BAKKnIvVCY5JfDmk+3xJ+XRVRTKtaXRiF6SZ",
        "__ASYNCPOST":	"true",
        "ctl00$cphMain$btnBuscarPorRNC":	"Buscar",
        }

        # Codificar los datos
        encoded_data = urlencode(data)

        # Realizar la solicitud POST con cookies si es necesario
        response = requests.post(url, headers=headers, data=encoded_data)

        soup = BeautifulSoup(response.text, 'html.parser')

        data_dict = {}
        for row in soup.find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 2:
                key = columns[0].text.strip()
                value = columns[1].text.strip()
                data_dict[key] = value

        return JsonResponse(data_dict)

@login_required
def blackboard(request):
    estudiantess= estudiantes.objects.all()
    grados = grado.objects.all()
    
    #group = request.user.groups.all()[0].name
    group = 'estudiante'
    
    if (group == "estudiante"):
     return render(request, "dstecnologia/blackboard.html", {"estudiantess":estudiantess})  
    if (group == "profesor"):
     return render(request, "dstecnologia/bb_profesor/index_profesor.html", {"grados":grados})    


def blackboard_docentes(request):
    grados = grado.objects.all()
    data = {"grados":grados}
    return render(request, "dstecnologia/bb_profesor/index_profesor.html", data)        

def compiler(request):
    return render(request, "dstecnologia/python_compiler.html")    

def qualifications(request,seleccion):
    calificacions = calificacion.objects.filter(username=request.user.username)
    estudiantess= estudiantes.objects.filter(groups__name="estudiante")
    
    
    s_grado = (seleccion[0:3])
    s_seccion = (seleccion[3:4])
    s_nivel = (seleccion[4:])
     
    meses = ["Agosto","Septiembre","Octubre","Noviembre","Diciembre"] 
    form = calificaciones(request.POST)

    if request.method == "POST":
            if form.is_valid():
                form.save()  
                return redirect("/qualifications/"+seleccion)         
               
    else: form = calificaciones 

    #group = request.user.groups.all()[0].name
    group = 'estudiante'
    
    if (group == "estudiante"): 
     return render(request, "dstecnologia/bb/qualifications.html", {"calificacions":calificacions, "meses":meses})
    if (group == "profesor"):
     return render(request, "dstecnologia/bb_profesor/lista_estudiantes.html", {"estudiantess":estudiantess, "s_grado":s_grado, "s_seccion":s_seccion, "s_nivel":s_nivel, "meses":meses})   

        

def practices(request):
    return render(request, "dstecnologia/bb/practices.html")  

def contac(request):
    return render(request, "dstecnologia/contacto.html")     

def denegado(request):
    return render(request, "dstecnologia/denegado.html")      

def contenido(request):
    return render(request, "dstecnologia/bb/contenido.html")  
  

def registro(request):
        form = registerForm(request.POST)
        calificacions = calificacion.objects.latest()

        if request.method == "POST":
            if form.is_valid():
                form.save()  
                return redirect("/register")         
               
        else: form = registerForm 
        context = { 'form': form, 'calificacions':calificacions} 
        return render(request, "dstecnologia/admin/register.html", context)
        


def salir(request):
    logout(request)
    return redirect("/") 
