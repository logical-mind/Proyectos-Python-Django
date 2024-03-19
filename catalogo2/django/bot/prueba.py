from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import pymysql 
import time 
import json

tiempo = 0
api = IQ_Option("juanerodriguez23@gmail.com", "Jamil171120")
api.connect()


def llamar_divisas():
            try:  
                lista = []
                assets = {}
                ALL_Asset=api.get_all_open_time()

                for type_name, data in ALL_Asset.items():
                    for Asset,value in data.items():
                        if type_name == 'turbo' and value["open"] == True:
                            if Asset != "USDZAR-OTC" and Asset != "USDINR-OTC" and Asset != "USDHKD-OTC" and Asset != "USDSGD-OTC" and Asset != "USDZAR" and Asset != "USDINR" and Asset != "USDHKD" and Asset != "USDSGD" and Asset != "XAUUSD" and Asset != "AUDCAD" and Asset != "USDCHF":    
                                assets = {
                                        "type": type_name,
                                        "divisa": Asset
                                        }
                                
                                lista.append(assets)
                        """if type_name == 'digital' and value["open"] == True: 
                            if Asset != "USDZAR-OTC" and Asset != "USDINR-OTC" and Asset != "USDHKD-OTC" and Asset != "USDSGD-OTC" and Asset != "USDZAR" and Asset != "USDINR" and Asset != "USDHKD" and Asset != "USDSGD" and Asset != "XAUUSD":     
                                assets = {
                                        "type": type_name,
                                        "divisa": Asset
                                        }
                                
                                lista.append(assets)""" 

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

divisa = llamar_divisas()

lista_final = []

fecha_actual = datetime.now().date()
hora_inicial = f"{fecha_actual} 16:00:00.00"
 
datetime_object = datetime.strptime(hora_inicial, "%Y-%m-%d %H:%M:%S.%f")
datetime_object = datetime_object - timedelta(days=1)

for x in divisa:
    lista = []
    dia = {}
    asset = x["divisa"]
    periodo = 1
    rango = 10

    if rango == 5:
           dojis_permitidos = 2
           velas_permitidas = 3

    if rango == 10:
           dojis_permitidos = 2
           velas_permitidas = 8

    if rango == 15:
           dojis_permitidos = 3
           velas_permitidas = 12       

    if rango == 20:
           dojis_permitidos = 4
           velas_permitidas = 16       

    if periodo == 1: 
           tiempo = 60
           n_velas = 601
           porciento_total = 100

    if periodo == 5: 
           tiempo = 300
           n_velas = 121 
           porciento_total = 90


    if periodo == 10: 
           tiempo = 600
           n_velas = 61  
           porciento_total = 100

    if periodo == 15: 
           tiempo = 900
           n_velas = 41  
           porciento_total = 100 

    if periodo == 30: 
           tiempo = 1800
           n_velas = 21  
           porciento_total = 100       

   
           

          
    for i in range(rango):
        
        
        hora_inicial = datetime_object - timedelta(days=i)
        print(hora_inicial)
        # de 6AM a 4PM mercado normal
        data = api.get_candles(asset,tiempo,n_velas,datetime.timestamp(hora_inicial))
        fecha_solo = hora_inicial.date()


        hora_inicial2 = f"{fecha_solo} 06:00:00.00"
        datetime_object2 = datetime.strptime(hora_inicial2, "%Y-%m-%d %H:%M:%S.%f")


        for i in data:
        
            if i['open'] < i['close']:
                vela = 'alcista'
            elif i['open'] > i['close']:
                vela = 'bajista'
            else:
                vela = 'doji'
    

            # Crear un nuevo diccionario para cada iteración
            dia = {
                "vela": vela,
                "hora": datetime_object2.strftime("%Y-%m-%d %H:%M:%S.%f")
            }
            
            lista.append(dia)

            datetime_object2 += timedelta(minutes=periodo)

    horas_procesadas = set()
    for i in lista:
            fecha_objeto = datetime.strptime(i['hora'], "%Y-%m-%d %H:%M:%S.%f")
            hora_minuto_segundo = fecha_objeto.strftime("%H:%M:%S")


            if hora_minuto_segundo not in horas_procesadas:
                    elementos_filtrados = [x for x in lista if datetime.strptime(x['hora'], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M:%S") == hora_minuto_segundo]
                    #print(f'Elementos para la hora {hora_especifica}: {elementos_filtrados}')  

                    alcistas = sum(1 for vela in elementos_filtrados if vela['vela'] == 'alcista')
                    bajistas = sum(1 for vela in elementos_filtrados if vela['vela'] == 'bajista')
                    doji = sum(1 for vela in elementos_filtrados if vela['vela'] == 'doji')

                    '''print('conteo_alcistas: ',alcistas)
                    print('conteo_bajistas: ',bajistas)
                    print('conteo_doji: ',conteo_doji)'''
                    try:
                        total_velas = alcistas + bajistas
                        porcentaje_alcistas = (alcistas / total_velas) * 100
                        porcentaje_bajistas = (bajistas / total_velas) * 100
                    except:pass
                    # Imprimir resultados
                    if porcentaje_alcistas >= porciento_total and doji <= dojis_permitidos and total_velas >= velas_permitidas:
                            fecha_final = f"{datetime.now().date()} {hora_minuto_segundo}"
                            porcentaje_dict = {
                                'hora': fecha_final,
                                'divisa': asset,
                                'accion': 'call',
                                'periodo': periodo
                            }
                            
                            lista_final.append(porcentaje_dict)
                            print(f' Divisa: {asset} | Porcentaje de velas alcistas: {porcentaje_alcistas}% |', hora_minuto_segundo)
                    if porcentaje_bajistas >= porciento_total and doji <= dojis_permitidos and total_velas >=velas_permitidas:  
                            fecha_final = f"{datetime.now().date()} {hora_minuto_segundo}"
                            porcentaje_dict = {
                              'hora': fecha_final,
                              'divisa': asset,
                              'accion': 'put',
                              'periodo':  periodo
                              }  
                              
                            lista_final.append(porcentaje_dict)
                            print(f' Divisa: {asset} | Porcentaje de velas bajistas: {porcentaje_bajistas}% |', hora_minuto_segundo)

                    horas_procesadas.add(hora_minuto_segundo)    

fechas_unicas = set()
lista_final_sin_duplicados = [elemento for elemento in lista_final if not (elemento['hora'] in fechas_unicas or fechas_unicas.add(elemento['hora']))]

lista_final2 = json.dumps(lista_final_sin_duplicados)  

try:         
                    conexion = pymysql.connect(
                            host='195.35.18.148',
                            user='monse',
                            password='Jamil171120',
                            database='catalobot'
                            )
                    with conexion.cursor() as cursor:
                    
                            consulta = "UPDATE bot_senal SET senales = %s"
                            valores = (lista_final2,)  # Asegúrate de proporcionar valores reales
                            cursor.execute(consulta, valores)

                            fecha_y_hora_actual = datetime.now()
                            consulta = "UPDATE bot_senal SET fecha_y_hora = %s"
                            cursor.execute(consulta, fecha_y_hora_actual)
                            
                            conexion.commit()

except pymysql.Error as e:
                print(f"Error: {e}")

finally:
                conexion.close()

