from iqoptionapi.stable_api import IQ_Option
from datetime import datetime, timedelta
import pymysql
import time, json

api = IQ_Option("juanerodriguez23@gmail.com", "Jamil171120")
api.connect()


def llamar_divisas():
    try:
        lista = []
        assets = {}
        ALL_Asset = api.get_all_open_time()

        for type_name, data in ALL_Asset.items():
            for Asset, value in data.items():
                if value.get("open", False):
                    if type_name == 'turbo':
                        if Asset not in ["USDZAR-OTC", "USDINR-OTC", "USDHKD-OTC", "USDSGD-OTC", "USDZAR", "USDINR", "USDHKD", "USDSGD", "XAUUSD", "AUDCAD", "USDCHF"]:
                            assets = {"type": type_name, "divisa": Asset}
                            lista.append(assets)

        divisa_dict = {}
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

    except Exception as e:
        print(f"Error en llamar_divisas: {str(e)}")


def obtener_indicadores(divisa):
    tecnicos_1m = []
    tecnicos_5m = []
    tecnicos_15m = []

    try:
        accion_m1, accion_m5, accion_m15 = 'hold', 'hold', 'hold'
        indicators = api.get_technical_indicators(divisa)
        for indicator in indicators:
            medias = [
                                    'Simple Moving Average (5)',
                                    'Simple Moving Average (10)',
                                    'Simple Moving Average (20)',
                                    'Simple Moving Average (30)',
                                    'Simple Moving Average (50)',
                                    'Simple Moving Average (100)',
                                    'Simple Moving Average (200)',
                                    'Exponential Moving Average (5)',
                                    'Exponential Moving Average (10)',
                                    'Exponential Moving Average (20)',
                                    'Exponential Moving Average (30)',
                                    'Exponential Moving Average (50)',
                                    'Exponential Moving Average (100)',
                                    'Exponential Moving Average (200)',
                                    'Ichimoku Cloud Base Line (9, 26, 52, 26)',
                                    'Volume Weighted Moving Average (20)',
                                    'Hull Moving Average (9)',
                                    'Relative Strength Index (14)',
                                    'Williams Percent Range (14)'

            ]


            for x in medias:
                if indicator.get("name") == x and indicator.get("candle_size"):
                    if indicator["candle_size"] == 60:
                        if x == "Williams Percent Range (14)":
                            wpr_m1 = indicator.get("action", "")
                        elif x == "Relative Strength Index (14)":
                            rsi_m1 = indicator.get("action", "")
                        else: tecnicos_1m.append(indicator.get("action", ""))

                    if indicator["candle_size"] == 300:
                        if x == "Williams Percent Range (14)":
                            wpr_m5 = indicator.get("action", "")
                        elif x == "Relative Strength Index (14)":
                            rsi_m5 = indicator.get("action", "")
                        else: tecnicos_5m.append(indicator.get("action", "")) 

                    if indicator["candle_size"] == 900:
                        if x == "Williams Percent Range (14)":
                            wpr_m15 = indicator.get("action", "")
                        elif x == "Relative Strength Index (14)":
                            rsi_m15 = indicator.get("action", "")
                        else: tecnicos_15m.append(indicator.get("action", ""))       

         
        if tecnicos_1m.count('buy') >= 12 and  rsi_m1 == 'hold' and tecnicos_5m.count('buy') >= 12:
             accion_m1 = 'call'
        elif tecnicos_1m.count('sell') >= 12 and rsi_m1 == 'hold' and tecnicos_5m.count('sell') >= 12:
             accion_m1 = 'put'

        if tecnicos_5m.count('buy') >= 12 and rsi_m5 == 'hold' and tecnicos_15m.count('buy') >= 12:
            accion_m5 = 'call'
        elif tecnicos_5m.count('sell') >= 12 and rsi_m5 == 'hold' and tecnicos_15m.count('sell') >= 12:
            accion_m5 = 'put'

        if tecnicos_15m.count('buy') >= 12 and rsi_m15 == 'hold':
            accion_m15 = 'call'
        elif tecnicos_15m.count('sell') >= 12 and rsi_m15 == 'hold':
            accion_m15 = 'put'        

        
        return accion_m1, accion_m5, accion_m15

    except Exception as e:
        print(f"Error al obtener indicadores para {divisa}: {str(e)}")
        return "", "", ""


def indicadores():
    divisas = []
    while True:
        now = datetime.now()
        s = format(now.second)
        if s == '20':
            divisas = llamar_divisas()
        if s == '30':
            lista = []
            senal_final = []
            if 'OTC' not in divisas[0]['divisa']:
                for divisa in divisas:
                    if divisa['divisa'] != 'EURGBP':
                        accion_m1, accion_m5, accion_m15 = obtener_indicadores(divisa['divisa'])

                        diccionario = {
                            'divisa': divisa,
                            'm1': accion_m1,
                            'm5': accion_m5,
                            'm15': accion_m15,
                        }
                        print(diccionario)
                        lista.append(diccionario)

                now = datetime.now()
                next_minute = now + timedelta(minutes=1)
                next_minute = next_minute.replace(second=0)

                for i in lista:
                    if i['m1'] == 'put' or i['m1'] == 'call':
                        senal_dict = {
                            'hora': next_minute.strftime("%Y-%m-%d %H:%M:%S"),
                            'divisa': i['divisa']['divisa'],
                            'accion': i['m1'],
                            'periodo': 1
                        }
                        senal_final.append(senal_dict)

                    # ... (similar blocks for other timeframes)

                conexion = pymysql.connect(
                    host='195.35.18.148',
                    user='monse',
                    password='Jamil171120',
                    database='catalobot'
                )
                with conexion.cursor() as cursor:
                    if senal_final:
                        consulta = "UPDATE bot_senal SET senales = %s"
                        valores = (json.dumps(senal_final),)  # Convert list to JSON before updating
                        cursor.execute(consulta, valores)

                    consulta = "UPDATE bot_indicador SET indicadores = %s"
                    valores = (json.dumps(lista),)  # Convert list to JSON before updating
                    cursor.execute(consulta, valores)

                    fecha_y_hora_actual = datetime.now()
                    consulta = "UPDATE bot_indicador SET fecha_y_hora = %s"
                    cursor.execute(consulta, fecha_y_hora_actual)

                    conexion.commit()

                time.sleep(30)
            else:
                time.sleep(40)
        time.sleep(1)


indicadores()