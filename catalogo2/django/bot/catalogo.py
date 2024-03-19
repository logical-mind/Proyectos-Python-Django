import threading
from datetime import datetime, timedelta
import json


def catalogo(api):
         
        comision2 = 0

        mercado = []
        mhi_lista = []
        mhi2_lista = []
        mhi3_lista = []
        mhimai_lista = []
        mhi2mai_lista = []
        mhi3mai_lista = []
        milhao_lista = []
        milhaomai_lista = []
        padrao23_lista = []
        melhor_lista = []
        torres_lista = []
        padrao3x1_lista = []


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


        def catalogo_mhi(data,minuto):
            try: 
                global mhi_lista
                mhi_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 1 or minuto == 6:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            if inicio <= 957:    

                                if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                                else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                        else: vela4 = 0

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                        vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 < 0):
                                    mhi_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 > 0):
                                        mhi_lista.append("win")
                                    else:   
                                        if inicio <= 957:    
                                            if(vela0 + vela1 + vela2 > 0 and vela4 < 0 and martingala >= 1):
                                                mhi_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0 and martingala >= 1):
                                                    mhi_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 2):
                                                        mhi_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 2):
                                                            mhi_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 3):
                                                                mhi_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 3):   
                                                                    mhi_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 4):
                                                                        mhi_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 4):   
                                                                            mhi_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 5):
                                                                                mhi_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 5):   
                                                                                    mhi_lista.append("g5")
                                                                                else:  
                                                                                    mhi_lista.append("hit")    
                                        else: mhi_lista.append("p1")

                            inicio = inicio + 5
                            n = n + 1 
                    
                if minuto == 2 or minuto == 7:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                        else: vela4 = 0


                            if inicio <= 957:
                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                        vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                vela5 = -1
                                        else: vela5 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 


                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 < 0):
                                    mhi_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 > 0):
                                        mhi_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 < 0 and martingala >= 1):
                                                mhi_lista.append("g1") 
                                            else:  
                                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0 and martingala >= 1):
                                                    mhi_lista.append("g1")       
                                                else: 
                                                  if inicio <= 957:     
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 2):
                                                        mhi_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 2):
                                                            mhi_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 3):
                                                                mhi_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 3):   
                                                                    mhi_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 4):
                                                                        mhi_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 4):   
                                                                            mhi_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 5):
                                                                                mhi_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 5):   
                                                                                    mhi_lista.append("g5")
                                                                                else:  
                                                                                    mhi_lista.append("hit")    
                                                  else: mhi_lista.append("p2")
                            inicio = inicio + 5
                            n = n + 1 
                
                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            
                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if inicio <= 957:
                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 < 0):
                                    mhi_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 > 0):
                                        mhi_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 < 0 and martingala >= 1):
                                                mhi_lista.append("g1") 
                                            else: 
                                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0 and martingala >= 1):
                                                    mhi_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 2):
                                                        mhi_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 2):
                                                            mhi_lista.append("g2")  
                                                        else:  
                                                         if inicio <= 957:   
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 3):
                                                                mhi_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 3):   
                                                                    mhi_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 4):
                                                                        mhi_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 4):   
                                                                            mhi_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 5):
                                                                                mhi_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 5):   
                                                                                    mhi_lista.append("g5")
                                                                                else:  
                                                                                    mhi_lista.append("hit")    
                                                         else: mhi_lista.append("p3")
                            inicio = inicio + 5
                            n = n + 1   
                
                if minuto == 4 or minuto == 9:
                        inicio = 2
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                vela4 = -1
                                        else: vela4 = 0

                            
                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 


                            
                            if(martingala >= 3): 
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                            if inicio <= 952:                    
                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 

                                
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 < 0):
                                    mhi_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 > 0):
                                        mhi_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 < 0 and martingala >= 1):
                                                mhi_lista.append("g1") 
                                            else: 
                                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0 and martingala >= 1):
                                                    mhi_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 2):
                                                        mhi_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 2):
                                                            mhi_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 3):
                                                                mhi_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 3):   
                                                                    mhi_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 952:                                 
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 4):
                                                                        mhi_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 4):   
                                                                            mhi_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 5):
                                                                                mhi_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 5):   
                                                                                    mhi_lista.append("g5")
                                                                                else:  
                                                                                    mhi_lista.append("hit")    
                                                                 else: mhi_lista.append("p4")
                            inicio = inicio + 5
                            n = n + 1    

                if minuto == 0 or minuto == 5:
                    inicio = 2
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']: 
                                vela0 = -1
                            else: vela0 = 0  
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                            vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                vela1 = -1
                            else: vela1 = 0   
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   
                        
                        if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                            vela3 = 1 
                        else:
                            if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                vela3 = -1
                            else: vela3 = 0
            
                        

                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                    vela4 = 1 
                        else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                        
                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                            vela5 = 1 
                        else:
                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                            else: vela5 = 0  


                        
                        if(martingala >= 3): 
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                            vela6 = 1 
                            else:
                                            if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                            else: vela6 = 0

                                            
                        if(martingala >= 4):
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                        if inicio <= 952:                    
                            if(martingala >= 5):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                    else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0 

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhi_lista.append("none")
                        else:    
                            if(vela0 + vela1 + vela2 > 0 and vela3 < 0):
                                mhi_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela3 > 0):
                                    mhi_lista.append("win")
                                else:       
                                        if(vela0 + vela1 + vela2 > 0 and vela4 < 0 and martingala >= 1):
                                            mhi_lista.append("g1") 
                                        else: 
                                            if(vela0 + vela1 + vela2 < 0 and vela4 > 0 and martingala >= 1):
                                                mhi_lista.append("g1")       
                                            else:    
                                                if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 2):
                                                    mhi_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 2):
                                                        mhi_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 3):
                                                            mhi_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 3):   
                                                                mhi_lista.append("g3")
                                                            else:                                  
                                                                if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 4):
                                                                    mhi_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 4):   
                                                                        mhi_lista.append("g4") 
                                                                    else:  
                                                                     if inicio <= 952:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 5):
                                                                            mhi_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 5):   
                                                                                mhi_lista.append("g5")
                                                                            else:  
                                                                                mhi_lista.append("hit")    
                                                                     else: mhi_lista.append("p5")
                        inicio = inicio + 5
                        n = n + 1  
            except:pass

        def catalogo_mhimai(data,minuto):
            try: 
                global mhimai_lista
                mhimai_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 1 or minuto == 6:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            if inicio <= 957:    

                                if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                                else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                        else: vela4 = 0

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                        vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhimai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 > 0):
                                    mhimai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 < 0):
                                        mhimai_lista.append("win")
                                    else:   
                                        if inicio <= 957:    
                                            if(vela0 + vela1 + vela2 > 0 and vela4 > 0 and martingala >= 1):
                                                mhimai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela4 < 0 and martingala >= 1):
                                                    mhimai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 2):
                                                        mhimai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 2):
                                                            mhimai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 3):
                                                                mhimai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 3):   
                                                                    mhimai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 4):
                                                                        mhimai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 4):   
                                                                            mhimai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 5):
                                                                                mhimai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 5):   
                                                                                    mhimai_lista.append("g5")
                                                                                else:  
                                                                                    mhimai_lista.append("hit")    
                                        else: mhimai_lista.append("p1")

                            inicio = inicio + 5
                            n = n + 1 
                    
                if minuto == 2 or minuto == 7:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                        else: vela4 = 0


                            if inicio <= 957:
                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                        vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                vela5 = -1
                                        else: vela5 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 


                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhimai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 > 0):
                                    mhimai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 < 0):
                                        mhimai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 > 0 and martingala >= 1):
                                                mhimai_lista.append("g1") 
                                            else:  
                                                if(vela0 + vela1 + vela2 < 0 and vela4 < 0 and martingala >= 1):
                                                    mhimai_lista.append("g1")       
                                                else: 
                                                 if inicio <= 957:     
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 2):
                                                        mhimai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 2):
                                                            mhimai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 3):
                                                                mhimai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 3):   
                                                                    mhimai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 4):
                                                                        mhimai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 4):   
                                                                            mhimai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 5):
                                                                                mhimai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 5):   
                                                                                    mhimai_lista.append("g5")
                                                                                else:  
                                                                                    mhimai_lista.append("hit")    
                                                 else: mhimai_lista.append("p2")
                            inicio = inicio + 5
                            n = n + 1 
                
                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                
                            

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            
                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if inicio <= 957:
                                if(martingala >= 3): 
                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhimai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 > 0):
                                    mhimai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 < 0):
                                        mhimai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 > 0 and martingala >= 1):
                                                mhimai_lista.append("g1") 
                                            else: 
                                                if(vela0 + vela1 + vela2 < 0 and vela4 < 0 and martingala >= 1):
                                                    mhimai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 2):
                                                        mhimai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 2):
                                                            mhimai_lista.append("g2")  
                                                        else:  
                                                         if inicio <= 957:   
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 3):
                                                                mhimai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 3):   
                                                                    mhimai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 4):
                                                                        mhimai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 4):   
                                                                            mhimai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 5):
                                                                                mhimai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 5):   
                                                                                    mhimai_lista.append("g5")
                                                                                else:  
                                                                                    mhimai_lista.append("hit")    
                                                         else: mhimai_lista.append("p3")
                            inicio = inicio + 5
                            n = n + 1   
                
                if minuto == 4 or minuto == 9:
                        inicio = 2
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0
                

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                vela4 = -1
                                        else: vela4 = 0

                            
                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 


                            
                            if(martingala >= 3): 
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                        vela6 = -1
                                                else: vela6 = 0

                            if inicio <= 952:                    
                                if(martingala >= 4):
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0

                                if(martingala >= 5):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0 

                                
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhimai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 > 0 and vela3 > 0):
                                    mhimai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela3 < 0):
                                        mhimai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela4 > 0 and martingala >= 1):
                                                mhimai_lista.append("g1") 
                                            else: 
                                                if(vela0 + vela1 + vela2 < 0 and vela4 < 0 and martingala >= 1):
                                                    mhimai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 2):
                                                        mhimai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 2):
                                                            mhimai_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 3):
                                                                mhimai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 3):   
                                                                    mhimai_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 952:                                 
                                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 4):
                                                                        mhimai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 4):   
                                                                            mhimai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 5):
                                                                                mhimai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 5):   
                                                                                    mhimai_lista.append("g5")
                                                                                else:  
                                                                                    mhimai_lista.append("hit")    
                                                                 else: mhimai_lista.append("p4")
                            inicio = inicio + 5
                            n = n + 1    

                if minuto == 0 or minuto == 5:
                    inicio = 2
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']: 
                                vela0 = -1
                            else: vela0 = 0  
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                            vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                vela1 = -1
                            else: vela1 = 0   
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   
                        
                        if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                            vela3 = 1 
                        else:
                            if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                vela3 = -1
                            else: vela3 = 0
            
                        

                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                    vela4 = 1 
                        else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                        
                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                            vela5 = 1 
                        else:
                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                            else: vela5 = 0  


                        
                        if(martingala >= 3): 
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                            vela6 = 1 
                            else:
                                            if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                            else: vela6 = 0

                                            
                        if(martingala >= 4):
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                        if inicio <= 952:                    
                            if(martingala >= 5):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                    else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0 

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhimai_lista.append("none")
                        else:    
                            if(vela0 + vela1 + vela2 > 0 and vela3 > 0):
                                mhimai_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela3 < 0):
                                    mhimai_lista.append("win")
                                else:       
                                        if(vela0 + vela1 + vela2 > 0 and vela4 > 0 and martingala >= 1):
                                            mhimai_lista.append("g1") 
                                        else: 
                                            if(vela0 + vela1 + vela2 < 0 and vela4 < 0 and martingala >= 1):
                                                mhimai_lista.append("g1")       
                                            else:    
                                                if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 2):
                                                    mhimai_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 2):
                                                        mhimai_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 3):
                                                            mhimai_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 3):   
                                                                mhimai_lista.append("g3")
                                                            else:                                  
                                                                if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 4):
                                                                    mhimai_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 4):   
                                                                        mhimai_lista.append("g4") 
                                                                    else:  
                                                                     if inicio <= 952:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 5):
                                                                            mhimai_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 5):   
                                                                                mhimai_lista.append("g5")
                                                                            else:  
                                                                                mhimai_lista.append("hit")    
                                                                     else: mhimai_lista.append("p5")
                        inicio = inicio + 5
                        n = n + 1   
            except:pass

        def catalogo_milhao(data,minuto):
                try:  
                        global milhao_lista
                        milhao_lista = []
                        cuadrante = 192
                        martingala = 5
                        n = 0

                        if minuto == 1 or minuto == 6:
                                inicio = 5
                                while(n<cuadrante):

                                    if data[inicio]['open'] < data[inicio]['close']: 
                                        vela0 = 1 
                                    else:
                                        if data[inicio]['open'] > data[inicio]['close']: 
                                            vela0 = -1
                                        else: vela0 = 0  
                                    
                                    if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                        vela1 = 1 
                                    else:
                                        if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                            vela1 = -1
                                        else: vela1 = 0   
                                        
                                    if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                        vela2 = 1 
                                    else:
                                        if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                            vela2 = -1
                                        else: vela2 = 0   
                                    
                                    if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                        vela3 = 1 
                                    else:
                                        if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                                vela3 = -1
                                        else: vela3 = 0

                                    if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                                vela4 = 1 
                                    else:
                                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                    vela4 = -1
                                            else: vela4 = 0

                                    if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                            vela5 = 1 
                                    else:
                                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                    vela5 = -1
                                            else: vela5 = 0    
                        
                                    if inicio <= 955:    

                                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                        else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                                else: vela6 = 0

                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                        vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0  

                                        if(martingala >= 3): 
                                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                        vela8 = 1 
                                                else:
                                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                                vela8 = -1
                                                        else: vela8 = 0

                                        if(martingala >= 4):
                                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                        vela9 = 1 
                                                else:
                                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                                vela9 = -1
                                                        else: vela9 = 0

                                        if(martingala >= 5):
                                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                        vela10 = 1 
                                                else:
                                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                                vela10 = -1
                                                        else: vela10 = 0 
                                    
                                    
                                    if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                        milhao_lista.append("none")
                                    else:    
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 < 0):
                                            milhao_lista.append("win")
                                        else:     
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 > 0):
                                                milhao_lista.append("win")
                                            else:   
                                                if inicio <= 955:    
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 < 0 and martingala >= 1):
                                                        milhao_lista.append("g1") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 > 0 and martingala >= 1):
                                                            milhao_lista.append("g1")       
                                                        else:    
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 < 0 and martingala >= 2):
                                                                milhao_lista.append("g2") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 > 0 and martingala >= 2):
                                                                    milhao_lista.append("g2")  
                                                                else:  
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 < 0 and martingala >= 3):
                                                                        milhao_lista.append("g3") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 > 0 and martingala >= 3):   
                                                                            milhao_lista.append("g3")
                                                                        else:                               
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 < 0 and martingala >= 4):
                                                                                milhao_lista.append("g4") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 > 0 and martingala >= 4):   
                                                                                    milhao_lista.append("g4") 
                                                                                else:  
                                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 < 0 and martingala >= 5):
                                                                                        milhao_lista.append("g5") 
                                                                                    else:
                                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                            milhao_lista.append("g5")
                                                                                        else:  
                                                                                            milhao_lista.append("hit")    
                                                else: milhao_lista.append("p1")

                                    inicio = inicio + 5
                                    n = n + 1 
                            
                        if minuto == 2 or minuto == 7:
                                inicio = 5
                                while(n<cuadrante):

                                    if data[inicio]['open'] < data[inicio]['close']: 
                                        vela0 = 1 
                                    else:
                                        if data[inicio]['open'] > data[inicio]['close']: 
                                            vela0 = -1
                                        else: vela0 = 0  
                                    
                                    if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                        vela1 = 1 
                                    else:
                                        if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                            vela1 = -1
                                        else: vela1 = 0   
                                        
                                    if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                        vela2 = 1 
                                    else:
                                        if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                            vela2 = -1
                                        else: vela2 = 0   
                                    
                                    if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                        vela3 = 1 
                                    else:
                                        if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                                vela3 = -1
                                        else: vela3 = 0

                                    if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                                vela4 = 1 
                                    else:
                                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                    vela4 = -1
                                            else: vela4 = 0

                                    if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                            vela5 = 1 
                                    else:
                                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                    vela5 = -1
                                            else: vela5 = 0    
                        
                                    if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                    else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                                else: vela6 = 0

                                    if inicio <= 955:            

                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                        vela7 = 1 
                                        else:
                                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                        vela7 = -1
                                                else: vela7 = 0  

                                        if(martingala >= 3): 
                                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                        vela8 = 1 
                                                else:
                                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                                vela8 = -1
                                                        else: vela8 = 0

                                        if(martingala >= 4):
                                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                        vela9 = 1 
                                                else:
                                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                                vela9 = -1
                                                        else: vela9 = 0

                                        if(martingala >= 5):
                                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                        vela10 = 1 
                                                else:
                                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                                vela10 = -1
                                                        else: vela10 = 0 
                                    
                                    
                                    if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                        milhao_lista.append("none")
                                    else:    
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 < 0):
                                            milhao_lista.append("win")
                                        else:     
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 > 0):
                                                milhao_lista.append("win")
                                            else:       
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 < 0 and martingala >= 1):
                                                        milhao_lista.append("g1") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 > 0 and martingala >= 1):
                                                            milhao_lista.append("g1")       
                                                        else:
                                                         if inicio <= 955:      
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 < 0 and martingala >= 2):
                                                                milhao_lista.append("g2") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 > 0 and martingala >= 2):
                                                                    milhao_lista.append("g2")  
                                                                else:  
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 < 0 and martingala >= 3):
                                                                        milhao_lista.append("g3") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 > 0 and martingala >= 3):   
                                                                            milhao_lista.append("g3")
                                                                        else:                               
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 < 0 and martingala >= 4):
                                                                                milhao_lista.append("g4") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 > 0 and martingala >= 4):   
                                                                                    milhao_lista.append("g4") 
                                                                                else:  
                                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 < 0 and martingala >= 5):
                                                                                        milhao_lista.append("g5") 
                                                                                    else:
                                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                            milhao_lista.append("g5")
                                                                                        else:  
                                                                                            milhao_lista.append("hit")    
                                                         else: milhao_lista.append("p2")

                                    inicio = inicio + 5
                                    n = n + 1 
                        
                        if minuto == 3 or minuto == 8:
                                inicio = 5
                                while(n<cuadrante):

                                    if data[inicio]['open'] < data[inicio]['close']: 
                                        vela0 = 1 
                                    else:
                                        if data[inicio]['open'] > data[inicio]['close']: 
                                            vela0 = -1
                                        else: vela0 = 0  
                                    
                                    if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                        vela1 = 1 
                                    else:
                                        if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                            vela1 = -1
                                        else: vela1 = 0   
                                        
                                    if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                        vela2 = 1 
                                    else:
                                        if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                            vela2 = -1
                                        else: vela2 = 0   
                                    
                                    if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                        vela3 = 1 
                                    else:
                                        if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                                vela3 = -1
                                        else: vela3 = 0

                                    if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                                vela4 = 1 
                                    else:
                                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                    vela4 = -1
                                            else: vela4 = 0

                                    if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                            vela5 = 1 
                                    else:
                                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                    vela5 = -1
                                            else: vela5 = 0    
                        
                                    if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                    else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                                else: vela6 = 0

                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                    vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0  

                                    if inicio <= 955:

                                        if(martingala >= 3): 
                                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                        vela8 = 1 
                                                else:
                                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                                vela8 = -1
                                                        else: vela8 = 0

                                        if(martingala >= 4):
                                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                        vela9 = 1 
                                                else:
                                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                                vela9 = -1
                                                        else: vela9 = 0

                                        if(martingala >= 5):
                                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                        vela10 = 1 
                                                else:
                                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                                vela10 = -1
                                                        else: vela10 = 0 
                                    
                                    
                                    if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                        milhao_lista.append("none")
                                    else:    
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 < 0):
                                            milhao_lista.append("win")
                                        else:     
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 > 0):
                                                milhao_lista.append("win")
                                            else:       
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 < 0 and martingala >= 1):
                                                        milhao_lista.append("g1") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 > 0 and martingala >= 1):
                                                            milhao_lista.append("g1")       
                                                        else:    
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 < 0 and martingala >= 2):
                                                                milhao_lista.append("g2") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 > 0 and martingala >= 2):
                                                                    milhao_lista.append("g2")  
                                                                else: 
                                                                 if inicio <= 955:   
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 < 0 and martingala >= 3):
                                                                        milhao_lista.append("g3") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 > 0 and martingala >= 3):   
                                                                            milhao_lista.append("g3")
                                                                        else:                               
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 < 0 and martingala >= 4):
                                                                                milhao_lista.append("g4") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 > 0 and martingala >= 4):   
                                                                                    milhao_lista.append("g4") 
                                                                                else:  
                                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 < 0 and martingala >= 5):
                                                                                        milhao_lista.append("g5") 
                                                                                    else:
                                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                            milhao_lista.append("g5")
                                                                                        else:  
                                                                                            milhao_lista.append("hit")    
                                                                 else: milhao_lista.append("p3")

                                    inicio = inicio + 5
                                    n = n + 1   
                        
                        if minuto == 4 or minuto == 9:
                                inicio = 0
                                while(n<cuadrante):

                                    if data[inicio]['open'] < data[inicio]['close']: 
                                        vela0 = 1 
                                    else:
                                        if data[inicio]['open'] > data[inicio]['close']: 
                                            vela0 = -1
                                        else: vela0 = 0  
                                    
                                    if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                        vela1 = 1 
                                    else:
                                        if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                            vela1 = -1
                                        else: vela1 = 0   
                                        
                                    if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                        vela2 = 1 
                                    else:
                                        if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                            vela2 = -1
                                        else: vela2 = 0   
                                    
                                    if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                        vela3 = 1 
                                    else:
                                        if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                                vela3 = -1
                                        else: vela3 = 0

                                    if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                                vela4 = 1 
                                    else:
                                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                    vela4 = -1
                                            else: vela4 = 0

                                    if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                            vela5 = 1 
                                    else:
                                            if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                    vela5 = -1
                                            else: vela5 = 0    
                        
                                    if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                                vela6 = 1 
                                    else:
                                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                    vela6 = -1
                                                else: vela6 = 0

                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                    vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0  

                                    

                                    if(martingala >= 3): 
                                            if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                    vela8 = 1 
                                            else:
                                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                            vela8 = -1
                                                    else: vela8 = 0

                                    if inicio <= 950:

                                        if(martingala >= 4):
                                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                        vela9 = 1 
                                                else:
                                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                                vela9 = -1
                                                        else: vela9 = 0

                                        if(martingala >= 5):
                                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                        vela10 = 1 
                                                else:
                                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                                vela10 = -1
                                                        else: vela10 = 0 
                                    
                                    
                                    if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                        milhao_lista.append("none")
                                    else:    
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 < 0):
                                            milhao_lista.append("win")
                                        else:     
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 > 0):
                                                milhao_lista.append("win")
                                            else:       
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 < 0 and martingala >= 1):
                                                        milhao_lista.append("g1") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 > 0 and martingala >= 1):
                                                            milhao_lista.append("g1")       
                                                        else:    
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 < 0 and martingala >= 2):
                                                                milhao_lista.append("g2") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 > 0 and martingala >= 2):
                                                                    milhao_lista.append("g2")  
                                                                else: 
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 < 0 and martingala >= 3):
                                                                        milhao_lista.append("g3") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 > 0 and martingala >= 3):   
                                                                            milhao_lista.append("g3")
                                                                        else: 
                                                                         if inicio <= 950:                                
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 < 0 and martingala >= 4):
                                                                                milhao_lista.append("g4") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 > 0 and martingala >= 4):   
                                                                                    milhao_lista.append("g4") 
                                                                                else:  
                                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 < 0 and martingala >= 5):
                                                                                        milhao_lista.append("g5") 
                                                                                    else:
                                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                            milhao_lista.append("g5")
                                                                                        else:  
                                                                                            milhao_lista.append("hit")    
                                                                         else: milhao_lista.append("p4")

                                    inicio = inicio + 5
                                    n = n + 1    

                        if minuto == 0 or minuto == 5:
                            inicio = 0
                            while(n<cuadrante):

                                if data[inicio]['open'] < data[inicio]['close']: 
                                    vela0 = 1 
                                else:
                                    if data[inicio]['open'] > data[inicio]['close']: 
                                        vela0 = -1
                                    else: vela0 = 0  
                                
                                if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                    vela1 = 1 
                                else:
                                    if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                        vela1 = -1
                                    else: vela1 = 0   
                                    
                                if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                    vela2 = 1 
                                else:
                                    if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                        vela2 = -1
                                    else: vela2 = 0   
                                
                                if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                    vela3 = 1 
                                else:
                                    if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                            vela3 = -1
                                    else: vela3 = 0

                                if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                            vela4 = 1 
                                else:
                                        if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                                vela4 = -1
                                        else: vela4 = 0

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                        vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                                vela5 = -1
                                        else: vela5 = 0    
                    
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                            vela6 = 1 
                                else:
                                            if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                                vela6 = -1
                                            else: vela6 = 0

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                        else: vela7 = 0  

                                

                                if(martingala >= 3): 
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0

                                if inicio <= 950:

                                    if(martingala >= 4):
                                            if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                    vela9 = 1 
                                            else:
                                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                            vela9 = -1
                                                    else: vela9 = 0

                                    if(martingala >= 5):
                                            if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                    vela10 = 1 
                                            else:
                                                    if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                            vela10 = -1
                                                    else: vela10 = 0 
                                
                                
                                if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                    milhao_lista.append("none")
                                else:    
                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 < 0):
                                        milhao_lista.append("win")
                                    else:     
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 > 0):
                                            milhao_lista.append("win")
                                        else:       
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 < 0 and martingala >= 1):
                                                    milhao_lista.append("g1") 
                                                else:
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 > 0 and martingala >= 1):
                                                        milhao_lista.append("g1")       
                                                    else:    
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 < 0 and martingala >= 2):
                                                            milhao_lista.append("g2") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 > 0 and martingala >= 2):
                                                                milhao_lista.append("g2")  
                                                            else: 
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 < 0 and martingala >= 3):
                                                                    milhao_lista.append("g3") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 > 0 and martingala >= 3):   
                                                                        milhao_lista.append("g3")
                                                                    else:                              
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 < 0 and martingala >= 4):
                                                                            milhao_lista.append("g4") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 > 0 and martingala >= 4):   
                                                                                milhao_lista.append("g4") 
                                                                            else: 
                                                                             if inicio <= 950:   
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 < 0 and martingala >= 5):
                                                                                    milhao_lista.append("g5") 
                                                                                else:
                                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                        milhao_lista.append("g5")
                                                                                    else:  
                                                                                        milhao_lista.append("hit")    
                                                                             else: milhao_lista.append("p5")

                                inicio = inicio + 5
                                n = n + 1
                except:pass

        def catalogo_milhaomai(data,minuto):
            try:  
                global milhaomai_lista
                milhaomai_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 1 or minuto == 6:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                    else: vela5 = 0    
                
                            if inicio <= 955:    

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                                else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                        else: vela7 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0

                                if(martingala >= 4):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                vela9 = 1 
                                        else:
                                                if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                        vela9 = -1
                                                else: vela9 = 0

                                if(martingala >= 5):
                                        if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                vela10 = 1 
                                        else:
                                                if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                        vela10 = -1
                                                else: vela10 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                milhaomai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 > 0):
                                    milhaomai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 < 0):
                                        milhaomai_lista.append("win")
                                    else:   
                                        if inicio <= 955:    
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 > 0 and martingala >= 1):
                                                milhaomai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 < 0 and martingala >= 1):
                                                    milhaomai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 > 0 and martingala >= 2):
                                                        milhaomai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 < 0 and martingala >= 2):
                                                            milhaomai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 > 0 and martingala >= 3):
                                                                milhaomai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    milhaomai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 > 0 and martingala >= 4):
                                                                        milhaomai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            milhaomai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 > 0 and martingala >= 5):
                                                                                milhaomai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    milhaomai_lista.append("g5")
                                                                                else:  
                                                                                    milhaomai_lista.append("hit")    
                                        else: milhaomai_lista.append("p1")

                            inicio = inicio + 5
                            n = n + 1 
                    
                if minuto == 2 or minuto == 7:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                    else: vela5 = 0    
                
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0

                            if inicio <= 955:            

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                        else: vela7 = 0  

                                if(martingala >= 3): 
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0

                                if(martingala >= 4):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                vela9 = 1 
                                        else:
                                                if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                        vela9 = -1
                                                else: vela9 = 0

                                if(martingala >= 5):
                                        if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                vela10 = 1 
                                        else:
                                                if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                        vela10 = -1
                                                else: vela10 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                milhaomai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 > 0):
                                    milhaomai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 < 0):
                                        milhaomai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 > 0 and martingala >= 1):
                                                milhaomai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 < 0 and martingala >= 1):
                                                    milhaomai_lista.append("g1")       
                                                else:
                                                 if inicio <= 955:      
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 > 0 and martingala >= 2):
                                                        milhaomai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 < 0 and martingala >= 2):
                                                            milhaomai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 > 0 and martingala >= 3):
                                                                milhaomai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    milhaomai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 > 0 and martingala >= 4):
                                                                        milhaomai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            milhaomai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 > 0 and martingala >= 5):
                                                                                milhaomai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    milhaomai_lista.append("g5")
                                                                                else:  
                                                                                    milhaomai_lista.append("hit")    
                                                 else: milhaomai_lista.append("p2")

                            inicio = inicio + 5
                            n = n + 1 
                
                if minuto == 3 or minuto == 8:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                    else: vela5 = 0    
                
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                            else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                    else: vela7 = 0  

                            if inicio <= 955:

                                if(martingala >= 3): 
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                        else:
                                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                        vela8 = -1
                                                else: vela8 = 0

                                if(martingala >= 4):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                vela9 = 1 
                                        else:
                                                if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                        vela9 = -1
                                                else: vela9 = 0

                                if(martingala >= 5):
                                        if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                vela10 = 1 
                                        else:
                                                if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                        vela10 = -1
                                                else: vela10 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                milhaomai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 > 0):
                                    milhaomai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 < 0):
                                        milhaomai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 > 0 and martingala >= 1):
                                                milhaomai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 < 0 and martingala >= 1):
                                                    milhaomai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 > 0 and martingala >= 2):
                                                        milhaomai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 < 0 and martingala >= 2):
                                                            milhaomai_lista.append("g2")  
                                                        else: 
                                                         if inicio <= 955:   
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 > 0 and martingala >= 3):
                                                                milhaomai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    milhaomai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 > 0 and martingala >= 4):
                                                                        milhaomai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            milhaomai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 > 0 and martingala >= 5):
                                                                                milhaomai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    milhaomai_lista.append("g5")
                                                                                else:  
                                                                                    milhaomai_lista.append("hit")    
                                                         else: milhaomai_lista.append("p3")

                            inicio = inicio + 5
                            n = n + 1   
                
                if minuto == 4 or minuto == 9:
                        inicio = 0
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']: 
                                    vela0 = -1
                                else: vela0 = 0  
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                    vela1 = -1
                                else: vela1 = 0   
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   
                            
                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                        vela3 = -1
                                else: vela3 = 0

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                        vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                            vela4 = -1
                                    else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                    else: vela5 = 0    
                
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                            else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                    else: vela7 = 0  

                            

                            if(martingala >= 3): 
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                    else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0

                            if inicio <= 950:

                                if(martingala >= 4):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                                vela9 = 1 
                                        else:
                                                if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                        vela9 = -1
                                                else: vela9 = 0

                                if(martingala >= 5):
                                        if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                                vela10 = 1 
                                        else:
                                                if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                        vela10 = -1
                                                else: vela10 = 0 
                            
                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                                milhaomai_lista.append("none")
                            else:    
                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 > 0):
                                    milhaomai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 < 0):
                                        milhaomai_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 > 0 and martingala >= 1):
                                                milhaomai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 < 0 and martingala >= 1):
                                                    milhaomai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 > 0 and martingala >= 2):
                                                        milhaomai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 < 0 and martingala >= 2):
                                                            milhaomai_lista.append("g2")  
                                                        else: 
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 > 0 and martingala >= 3):
                                                                milhaomai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    milhaomai_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 950:                                
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 > 0 and martingala >= 4):
                                                                        milhaomai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            milhaomai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 > 0 and martingala >= 5):
                                                                                milhaomai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    milhaomai_lista.append("g5")
                                                                                else:  
                                                                                    milhaomai_lista.append("hit")    
                                                                 else: milhaomai_lista.append("p4")

                            inicio = inicio + 5
                            n = n + 1    

                if minuto == 0 or minuto == 5:
                    inicio = 0
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']: 
                                vela0 = -1
                            else: vela0 = 0  
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                            vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']: 
                                vela1 = -1
                            else: vela1 = 0   
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   
                        
                        if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                            vela3 = 1 
                        else:
                            if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                    vela3 = -1
                            else: vela3 = 0

                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                    vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0    
            
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0

                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                        else:
                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                else: vela7 = 0  

                        

                        if(martingala >= 3): 
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                        else: vela8 = 0

                        if inicio <= 950:

                            if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                    else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0

                            if(martingala >= 5):
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                            vela10 = 1 
                                    else:
                                            if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                            else: vela10 = 0 
                        
                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0 or vela3 == 0 or vela4 == 0):
                            milhaomai_lista.append("none")
                        else:    
                            if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela5 > 0):
                                milhaomai_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela5 < 0):
                                    milhaomai_lista.append("win")
                                else:       
                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela6 > 0 and martingala >= 1):
                                            milhaomai_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela6 < 0 and martingala >= 1):
                                                milhaomai_lista.append("g1")       
                                            else:    
                                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela7 > 0 and martingala >= 2):
                                                    milhaomai_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela7 < 0 and martingala >= 2):
                                                        milhaomai_lista.append("g2")  
                                                    else: 
                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela8 > 0 and martingala >= 3):
                                                            milhaomai_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela8 < 0 and martingala >= 3):   
                                                                milhaomai_lista.append("g3")
                                                            else:                              
                                                                if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela9 > 0 and martingala >= 4):
                                                                    milhaomai_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela9 < 0 and martingala >= 4):   
                                                                        milhaomai_lista.append("g4") 
                                                                    else: 
                                                                     if inicio <= 950:   
                                                                        if(vela0 + vela1 + vela2 + vela3 + vela4 > 0 and vela10 > 0 and martingala >= 5):
                                                                            milhaomai_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 + vela3 + vela4 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                milhaomai_lista.append("g5")
                                                                            else:  
                                                                                milhaomai_lista.append("hit")    
                                                                     else: milhaomai_lista.append("p5")

                        inicio = inicio + 5
                        n = n + 1            
            except:pass

        def catalogo_mhi2(data,minuto):
            try: 
                global mhi2_lista
                mhi2_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 2 or minuto == 7:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                              vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                  vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                              vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                              vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0

                            if inicio <= 957: 

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                                else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0  

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                           vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                    mhi2_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                        mhi2_lista.append("win")
                                    else:  
                                        if inicio <= 957:    
                                            if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 1):
                                                mhi2_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                    mhi2_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                        mhi2_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                            mhi2_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                                mhi2_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                    mhi2_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                        mhi2_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                            mhi2_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                                mhi2_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                    mhi2_lista.append("g5")
                                                                                else:    
                                                                                    mhi2_lista.append("hit")      
                                        else: mhi2_lista.append("p1")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0      

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                            if inicio <= 957:
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                           if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                             vela7 = -1
                                           else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                    mhi2_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                        mhi2_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 1):
                                                mhi2_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                    mhi2_lista.append("g1")       
                                                else:  
                                                 if inicio <= 957:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                        mhi2_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                            mhi2_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                                mhi2_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                    mhi2_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                        mhi2_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                            mhi2_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                                mhi2_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                    mhi2_lista.append("g5")
                                                                                else:    
                                                                                    mhi2_lista.append("hit")      
                                                 else: mhi2_lista.append("p2")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 4 or minuto == 9:
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                              vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                  vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                              vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                              vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                            if inicio <= 952:
                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                          vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                    mhi2_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                        mhi2_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 1):
                                                mhi2_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                    mhi2_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                        mhi2_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                            mhi2_lista.append("g2")  
                                                        else:  
                                                         if inicio <= 952:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                                mhi2_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                    mhi2_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                        mhi2_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                            mhi2_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                                mhi2_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                    mhi2_lista.append("g5")
                                                                                else:    
                                                                                    mhi2_lista.append("hit")      
                                                         else: mhi2_lista.append("p3")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:
                        inicio = 2            
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                              vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                  vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                              vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  


                            if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                            if inicio <= 952:               
                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                    mhi2_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                        mhi2_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 1):
                                                mhi2_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                    mhi2_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                        mhi2_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                            mhi2_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                                mhi2_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                    mhi2_lista.append("g3")
                                                                else:  
                                                                 if inicio <= 952:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                        mhi2_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                            mhi2_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                                mhi2_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                    mhi2_lista.append("g5")
                                                                                else:    
                                                                                    mhi2_lista.append("hit")      
                                                                 else: mhi2_lista.append("p4")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                    inicio = 2   
                    while(n<cuadrante):
                        if data[inicio]['open'] < data[inicio]['close']: 
                           vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                               vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                           vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   
                            
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                            else: vela4 = 0

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                    vela6 = -1
                                else: vela6 = 0  


                        if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                      vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                                    
                        if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                        if inicio <= 952:
                            if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhi2_lista.append("none")
                        else:
                            if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                mhi2_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                    mhi2_lista.append("win")
                                else:      
                                        if(vela0 + vela1 + vela2 > 0 and vela5 < 0 and martingala >= 1):
                                            mhi2_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                mhi2_lista.append("g1")       
                                            else:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                    mhi2_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                        mhi2_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                            mhi2_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                mhi2_lista.append("g3")
                                                            else:                                 
                                                                if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                    mhi2_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                        mhi2_lista.append("g4") 
                                                                    else:  
                                                                     if inicio <= 952:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                            mhi2_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                mhi2_lista.append("g5")
                                                                            else:    
                                                                                mhi2_lista.append("hit")      
                                                                     else: mhi2_lista.append("p5")
                    
                        inicio = inicio + 5
                        n = n + 1
            except: pass

        def catalogo_mhi2mai(data,minuto):
            try: 
                global mhi2mai_lista
                mhi2mai_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 2 or minuto == 7:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0

                            if inicio <= 957: 

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                                else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0  

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                              vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 > 0):
                                    mhi2mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 < 0):
                                        mhi2mai_lista.append("win")
                                    else:  
                                        if inicio <= 957:    
                                            if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 1):
                                                mhi2mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 1):
                                                    mhi2mai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 2):
                                                        mhi2mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 2):
                                                            mhi2mai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 3):
                                                                mhi2mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    mhi2mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 4):
                                                                        mhi2mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            mhi2mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 5):
                                                                                mhi2mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    mhi2mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi2mai_lista.append("hit")      
                                        else: mhi2mai_lista.append("p1")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                    vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0      

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                            if inicio <= 957:
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                           vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 > 0):
                                    mhi2mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 < 0):
                                        mhi2mai_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 1):
                                                mhi2mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 1):
                                                    mhi2mai_lista.append("g1")       
                                                else:  
                                                 if inicio <= 957:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 2):
                                                        mhi2mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 2):
                                                            mhi2mai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 3):
                                                                mhi2mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    mhi2mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 4):
                                                                        mhi2mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            mhi2mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 5):
                                                                                mhi2mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    mhi2mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi2mai_lista.append("hit")      
                                                 else: mhi2mai_lista.append("p2")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 4 or minuto == 9:
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                              vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                            if inicio <= 952:
                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 > 0):
                                    mhi2mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 < 0):
                                        mhi2mai_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 1):
                                                mhi2mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 1):
                                                    mhi2mai_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 2):
                                                        mhi2mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 2):
                                                            mhi2mai_lista.append("g2")  
                                                        else:  
                                                         if inicio <= 952:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 3):
                                                                mhi2mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    mhi2mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 4):
                                                                        mhi2mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            mhi2mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 5):
                                                                                mhi2mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    mhi2mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi2mai_lista.append("hit")      
                                                         else: mhi2mai_lista.append("p3")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:
                        inicio = 2            
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  


                            if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                            if inicio <= 952:               
                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                           vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi2mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela4 > 0):
                                    mhi2mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela4 < 0):
                                        mhi2mai_lista.append("win")
                                    else:      
                                            if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 1):
                                                mhi2mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 1):
                                                    mhi2mai_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 2):
                                                        mhi2mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 2):
                                                            mhi2mai_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 3):
                                                                mhi2mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    mhi2mai_lista.append("g3")
                                                                else:  
                                                                 if inicio <= 952:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 4):
                                                                        mhi2mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            mhi2mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 5):
                                                                                mhi2mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    mhi2mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi2mai_lista.append("hit")      
                                                                 else: mhi2mai_lista.append("p4")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                    inicio = 2   
                    while(n<cuadrante):
                        if data[inicio]['open'] < data[inicio]['close']: 
                          vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                               vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                           vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                           vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   
                            
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                            else: vela4 = 0

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                    vela6 = -1
                                else: vela6 = 0  


                        if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                       vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                                    
                        if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                        if inicio <= 952:
                            if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhi2mai_lista.append("none")
                        else:
                            if(vela0 + vela1 + vela2 > 0 and vela4 > 0):
                                mhi2mai_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 < 0):
                                    mhi2mai_lista.append("win")
                                else:      
                                        if(vela0 + vela1 + vela2 > 0 and vela5 > 0 and martingala >= 1):
                                            mhi2mai_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 < 0 and martingala >= 1):
                                                mhi2mai_lista.append("g1")       
                                            else:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 2):
                                                    mhi2mai_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 2):
                                                        mhi2mai_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 3):
                                                            mhi2mai_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 3):   
                                                                mhi2mai_lista.append("g3")
                                                            else:                                 
                                                                if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 4):
                                                                    mhi2mai_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 4):   
                                                                        mhi2mai_lista.append("g4") 
                                                                    else:  
                                                                     if inicio <= 952:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 5):
                                                                            mhi2mai_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                mhi2mai_lista.append("g5")
                                                                            else:    
                                                                                mhi2mai_lista.append("hit")      
                                                                     else: mhi2mai_lista.append("p5")
                    
                        inicio = inicio + 5
                        n = n + 1
            except:pass

        def catalogo_padrao23(data,minuto):
            try:  
                global padrao23_lista
                padrao23_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 2 or minuto == 7:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                              vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0

                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                               vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                    vela3 = -1
                                else: vela3 = 0       

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0

                            if inicio <= 957: 

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                                else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0  

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                           vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela3 == 0):
                                padrao23_lista.append("none")
                            else:
                                if(vela3 > 0 and vela4 > 0):
                                    padrao23_lista.append("win")
                                else:     
                                    if(vela3 < 0 and vela4 < 0):
                                        padrao23_lista.append("win")
                                    else:  
                                        if inicio <= 957:    
                                            if(vela3 > 0 and vela5 > 0 and martingala >= 1):
                                                padrao23_lista.append("g1") 
                                            else:
                                                if(vela3 < 0 and vela5 < 0 and martingala >= 1):
                                                    padrao23_lista.append("g1")       
                                                else:    
                                                    if(vela3 > 0 and vela6 > 0 and martingala >= 2):
                                                        padrao23_lista.append("g2") 
                                                    else:
                                                        if(vela3 < 0 and vela6 < 0 and martingala >= 2):
                                                            padrao23_lista.append("g2")  
                                                        else:  
                                                            if(vela3 > 0 and vela7 > 0 and martingala >= 3):
                                                                padrao23_lista.append("g3") 
                                                            else:
                                                                if(vela3 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    padrao23_lista.append("g3")
                                                                else:                               
                                                                    if(vela3 > 0 and vela8 > 0 and martingala >= 4):
                                                                        padrao23_lista.append("g4") 
                                                                    else:
                                                                        if(vela3 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            padrao23_lista.append("g4") 
                                                                        else:  
                                                                            if(vela3 > 0 and vela9 > 0 and martingala >= 5):
                                                                                padrao23_lista.append("g5") 
                                                                            else:
                                                                                if(vela3 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    padrao23_lista.append("g5")
                                                                                else:    
                                                                                    padrao23_lista.append("hit")      
                                        else: padrao23_lista.append("p1")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                              vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                  vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                              vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0 

                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                               vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                    vela3 = -1
                                else: vela3 = 0      

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0      

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                            if inicio <= 957:
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0   

                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao23_lista.append("none")
                            else:
                                if(vela3 > 0 and vela4 > 0):
                                    padrao23_lista.append("win")
                                else:     
                                    if(vela3 < 0 and vela4 < 0):
                                        padrao23_lista.append("win")
                                    else:      
                                            if(vela3 > 0 and vela5 > 0 and martingala >= 1):
                                                padrao23_lista.append("g1") 
                                            else:
                                                if(vela3 < 0 and vela5 < 0 and martingala >= 1):
                                                    padrao23_lista.append("g1")       
                                                else:  
                                                 if inicio <= 957:    
                                                    if(vela3 > 0 and vela6 > 0 and martingala >= 2):
                                                        padrao23_lista.append("g2") 
                                                    else:
                                                        if(vela3 < 0 and vela6 < 0 and martingala >= 2):
                                                            padrao23_lista.append("g2")  
                                                        else:  
                                                            if(vela3 > 0 and vela7 > 0 and martingala >= 3):
                                                                padrao23_lista.append("g3") 
                                                            else:
                                                                if(vela3 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    padrao23_lista.append("g3")
                                                                else:                               
                                                                    if(vela3 > 0 and vela8 > 0 and martingala >= 4):
                                                                        padrao23_lista.append("g4") 
                                                                    else:
                                                                        if(vela3 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            padrao23_lista.append("g4") 
                                                                        else:  
                                                                            if(vela3 > 0 and vela9 > 0 and martingala >= 5):
                                                                                padrao23_lista.append("g5") 
                                                                            else:
                                                                                if(vela3 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    padrao23_lista.append("g5")
                                                                                else:    
                                                                                    padrao23_lista.append("hit")      
                                                 else: padrao23_lista.append("p2")
                        
                            inicio = inicio + 5
                            n = n + 1 

                if minuto == 4 or minuto == 9:
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0 

                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                    vela3 = -1
                                else: vela3 = 0      

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                            if inicio <= 952:
                                if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                            vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao23_lista.append("none")
                            else:
                                if(vela3 > 0 and vela4 > 0):
                                    padrao23_lista.append("win")
                                else:     
                                    if(vela3 < 0 and vela4 < 0):
                                        padrao23_lista.append("win")
                                    else:      
                                            if(vela3 > 0 and vela5 > 0 and martingala >= 1):
                                                padrao23_lista.append("g1") 
                                            else:
                                                if(vela3 < 0 and vela5 < 0 and martingala >= 1):
                                                    padrao23_lista.append("g1")       
                                                else:      
                                                    if(vela3 > 0 and vela6 > 0 and martingala >= 2):
                                                        padrao23_lista.append("g2") 
                                                    else:
                                                        if(vela3 < 0 and vela6 < 0 and martingala >= 2):
                                                            padrao23_lista.append("g2")  
                                                        else:  
                                                         if inicio <= 952:  
                                                            if(vela3 > 0 and vela7 > 0 and martingala >= 3):
                                                                padrao23_lista.append("g3") 
                                                            else:
                                                                if(vela3 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    padrao23_lista.append("g3")
                                                                else:                               
                                                                    if(vela3 > 0 and vela8 > 0 and martingala >= 4):
                                                                        padrao23_lista.append("g4") 
                                                                    else:
                                                                        if(vela3 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            padrao23_lista.append("g4") 
                                                                        else:  
                                                                            if(vela3 > 0 and vela9 > 0 and martingala >= 5):
                                                                                padrao23_lista.append("g5") 
                                                                            else:
                                                                                if(vela3 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    padrao23_lista.append("g5")
                                                                                else:    
                                                                                    padrao23_lista.append("hit")      
                                                         else: padrao23_lista.append("p3")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:
                        inicio = 2            
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0

                            if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                                vela3 = 1 
                            else:
                                if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                    vela3 = -1
                                else: vela3 = 0       

                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                else: vela4 = 0

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                    
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  


                            if(martingala >= 3): 
                                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                                        else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                            else: vela7 = 0

                            if inicio <= 952:               
                                if(martingala >= 4):
                                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                                        else:
                                            if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                            else: vela8 = 0

                                if(martingala >= 5):
                                        if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                          vela9 = 1 
                                        else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao23_lista.append("none")
                            else:
                                if(vela3 > 0 and vela4 > 0):
                                    padrao23_lista.append("win")
                                else:     
                                    if(vela3 < 0 and vela4 < 0):
                                        padrao23_lista.append("win")
                                    else:      
                                            if(vela3 > 0 and vela5 > 0 and martingala >= 1):
                                                padrao23_lista.append("g1") 
                                            else:
                                                if(vela3 < 0 and vela5 < 0 and martingala >= 1):
                                                    padrao23_lista.append("g1")       
                                                else:      
                                                    if(vela3 > 0 and vela6 > 0 and martingala >= 2):
                                                        padrao23_lista.append("g2") 
                                                    else:
                                                        if(vela3 < 0 and vela6 < 0 and martingala >= 2):
                                                            padrao23_lista.append("g2")  
                                                        else:    
                                                            if(vela3 > 0 and vela7 > 0 and martingala >= 3):
                                                                padrao23_lista.append("g3") 
                                                            else:
                                                                if(vela3 < 0 and vela7 < 0 and martingala >= 3):   
                                                                    padrao23_lista.append("g3")
                                                                else:  
                                                                 if inicio <= 952:                               
                                                                    if(vela3 > 0 and vela8 > 0 and martingala >= 4):
                                                                        padrao23_lista.append("g4") 
                                                                    else:
                                                                        if(vela3 < 0 and vela8 < 0 and martingala >= 4):   
                                                                            padrao23_lista.append("g4") 
                                                                        else:  
                                                                            if(vela3 > 0 and vela9 > 0 and martingala >= 5):
                                                                                padrao23_lista.append("g5") 
                                                                            else:
                                                                                if(vela3 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                    padrao23_lista.append("g5")
                                                                                else:    
                                                                                    padrao23_lista.append("hit")      
                                                                 else: padrao23_lista.append("p4")
                        
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                    inicio = 2   
                    while(n<cuadrante):
                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                               vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                            vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0

                        if data[inicio + 3]['open'] < data[inicio + 3]['close']: 
                            vela3 = 1 
                        else:
                            if data[inicio + 3]['open'] > data[inicio + 3]['close']:
                                vela3 = -1
                            else: vela3 = 0       
                            
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                            if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                            else: vela4 = 0

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0 

                
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                    vela6 = -1
                                else: vela6 = 0  


                        if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                    else:
                                            if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                            else: vela7 = 0

                                    
                        if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                        if inicio <= 952:
                            if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                       vela9 = 1 
                                    else:
                                            if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                            else: vela9 = 0 

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            padrao23_lista.append("none")
                        else:
                            if(vela3 > 0 and vela4 > 0):
                                padrao23_lista.append("win")
                            else:     
                                if(vela3 < 0 and vela4 < 0):
                                    padrao23_lista.append("win")
                                else:      
                                        if(vela3 > 0 and vela5 > 0 and martingala >= 1):
                                            padrao23_lista.append("g1") 
                                        else:
                                            if(vela3 < 0 and vela5 < 0 and martingala >= 1):
                                                padrao23_lista.append("g1")       
                                            else:      
                                                if(vela3 > 0 and vela6 > 0 and martingala >= 2):
                                                    padrao23_lista.append("g2") 
                                                else:
                                                    if(vela3 < 0 and vela6 < 0 and martingala >= 2):
                                                        padrao23_lista.append("g2")  
                                                    else:    
                                                        if(vela3 > 0 and vela7 > 0 and martingala >= 3):
                                                            padrao23_lista.append("g3") 
                                                        else:
                                                            if(vela3 < 0 and vela7 < 0 and martingala >= 3):   
                                                                padrao23_lista.append("g3")
                                                            else:                                 
                                                                if(vela3 > 0 and vela8 > 0 and martingala >= 4):
                                                                    padrao23_lista.append("g4") 
                                                                else:
                                                                    if(vela3 < 0 and vela8 < 0 and martingala >= 4):   
                                                                        padrao23_lista.append("g4") 
                                                                    else:  
                                                                     if inicio <= 952:  
                                                                        if(vela3 > 0 and vela9 > 0 and martingala >= 5):
                                                                            padrao23_lista.append("g5") 
                                                                        else:
                                                                            if(vela3 < 0 and vela9 < 0 and martingala >= 5):   
                                                                                padrao23_lista.append("g5")
                                                                            else:    
                                                                                padrao23_lista.append("hit")      
                                                                     else: padrao23_lista.append("p5")
                    
                        inicio = inicio + 5
                        n = n + 1
            except:pass


        def catalogo_mhi3(data,minuto):
            try: 
                global mhi3_lista
                mhi3_lista = []
                cuadrante = 192
                martingala = 5
                n = 0 
                
                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0
                            

                            if inicio <= 957: 

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                                else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 < 0):
                                    mhi3_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 > 0):
                                        mhi3_lista.append("win")
                                    else: 
                                        if inicio <= 957:      
                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 1):
                                                mhi3_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 1):
                                                    mhi3_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 2):
                                                        mhi3_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 2):
                                                            mhi3_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 3):
                                                                mhi3_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 3):   
                                                                    mhi3_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 4):
                                                                        mhi3_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 4):   
                                                                            mhi3_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 < 0 and martingala >= 5):
                                                                                mhi3_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                    mhi3_lista.append("g5")
                                                                                else:    
                                                                                    mhi3_lista.append("hit")      
                                        else: mhi3_lista.append("p1")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 4 or minuto == 9: 
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                                 vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            if inicio <= 952:

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 < 0):
                                    mhi3_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 > 0):
                                        mhi3_lista.append("win")
                                    else:     
                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 1):
                                                mhi3_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 1):
                                                    mhi3_lista.append("g1")       
                                                else:
                                                 if inicio <= 952:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 2):
                                                        mhi3_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 2):
                                                            mhi3_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 3):
                                                                mhi3_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 3):   
                                                                    mhi3_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 4):
                                                                        mhi3_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 4):   
                                                                            mhi3_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 < 0 and martingala >= 5):
                                                                                mhi3_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                    mhi3_lista.append("g5")
                                                                                else:    
                                                                                    mhi3_lista.append("hit")      
                                                 else: mhi3_lista.append("p2")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:   
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                            else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0 

                            if inicio <= 952:
                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 < 0):
                                    mhi3_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 > 0):
                                        mhi3_lista.append("win")
                                    else:     
                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 1):
                                                mhi3_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 1):
                                                    mhi3_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 2):
                                                        mhi3_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 2):
                                                            mhi3_lista.append("g2")  
                                                        else:
                                                         if inicio <= 952:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 3):
                                                                mhi3_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 3):   
                                                                    mhi3_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 4):
                                                                        mhi3_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 4):   
                                                                            mhi3_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 < 0 and martingala >= 5):
                                                                                mhi3_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                    mhi3_lista.append("g5")
                                                                                else:    
                                                                                    mhi3_lista.append("hit")      
                                                         else: mhi3_lista.append("p3")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                            else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0 

                            
                            if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0
                            
                            if inicio <= 952:

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 < 0):
                                    mhi3_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 > 0):
                                        mhi3_lista.append("win")
                                    else:   
                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 1):
                                                mhi3_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 1):
                                                    mhi3_lista.append("g1")       
                                                else:     
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 2):
                                                        mhi3_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 2):
                                                            mhi3_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 3):
                                                                mhi3_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 3):   
                                                                    mhi3_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 952:                                
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 4):
                                                                        mhi3_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 4):   
                                                                            mhi3_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 < 0 and martingala >= 5):
                                                                                mhi3_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                    mhi3_lista.append("g5")
                                                                                else:    
                                                                                    mhi3_lista.append("hit")      
                                                                 else: mhi3_lista.append("p4")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 2 or minuto == 7:                 
                    inicio = 2
                    while(n<cuadrante):
                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                               vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                           vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                            vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0  

                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0 

                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                        else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                    else: vela7 = 0 

                        if(martingala >= 3):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                    else: vela8 = 0

                        if(martingala >= 4):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else: 
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                    else: vela9 = 0

                        if inicio <= 952:

                            if(martingala >= 5): 
                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                    vela10 = 1 
                                else:
                                    if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                vela10 = -1
                                    else: vela10 = 0     

                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhi3_lista.append("none")
                        else:
                            if(vela0 + vela1 + vela2 > 0 and vela5 < 0):
                                mhi3_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela5 > 0):
                                    mhi3_lista.append("win")
                                else:   
                                        if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 1):
                                            mhi3_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 1):
                                                mhi3_lista.append("g1")       
                                            else:     
                                                if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 2):
                                                    mhi3_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 2):
                                                        mhi3_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 3):
                                                            mhi3_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 3):   
                                                                mhi3_lista.append("g3")
                                                            else:                                
                                                                if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 4):
                                                                    mhi3_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 4):   
                                                                        mhi3_lista.append("g4") 
                                                                    else:
                                                                      if inicio <= 952:    
                                                                        if(vela0 + vela1 + vela2 > 0 and vela10 < 0 and martingala >= 5):
                                                                            mhi3_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela10 > 0 and martingala >= 5):   
                                                                                mhi3_lista.append("g5")
                                                                            else:    
                                                                                mhi3_lista.append("hit")      
                                                                      else: mhi3_lista.append("p5")
                        
                        inicio = inicio + 5
                        n = n + 1
            except:pass

        def catalogo_mhi3mai(data,minuto):
            try: 
                global mhi3mai_lista
                mhi3mai_lista = []
                cuadrante = 192
                martingala = 5
                n = 0 
                
                if minuto == 3 or minuto == 8:
                        inicio = 7
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0
                            

                            if inicio <= 957: 

                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                                else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 > 0):
                                    mhi3mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 < 0):
                                        mhi3mai_lista.append("win")
                                    else: 
                                        if inicio <= 957:      
                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 1):
                                                mhi3mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 1):
                                                    mhi3mai_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 2):
                                                        mhi3mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 2):
                                                            mhi3mai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 3):
                                                                mhi3mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    mhi3mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 4):
                                                                        mhi3mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            mhi3mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 5):
                                                                                mhi3mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    mhi3mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi3mai_lista.append("hit")      
                                        else: mhi3mai_lista.append("p1")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 4 or minuto == 9: 
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            if inicio <= 952:

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 > 0):
                                    mhi3mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 < 0):
                                        mhi3mai_lista.append("win")
                                    else:     
                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 1):
                                                mhi3mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 1):
                                                    mhi3mai_lista.append("g1")       
                                                else:
                                                 if inicio <= 952:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 2):
                                                        mhi3mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 2):
                                                            mhi3mai_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 3):
                                                                mhi3mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    mhi3mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 4):
                                                                        mhi3mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            mhi3mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 5):
                                                                                mhi3mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    mhi3mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi3mai_lista.append("hit")      
                                                 else: mhi3mai_lista.append("p2")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:   
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                             vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                 vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                             vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                             vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                            else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0 

                            if inicio <= 952:
                                if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 > 0):
                                    mhi3mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 < 0):
                                        mhi3mai_lista.append("win")
                                    else:     
                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 1):
                                                mhi3mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 1):
                                                    mhi3mai_lista.append("g1")       
                                                else:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 2):
                                                        mhi3mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 2):
                                                            mhi3mai_lista.append("g2")  
                                                        else:
                                                         if inicio <= 952:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 3):
                                                                mhi3mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    mhi3mai_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 4):
                                                                        mhi3mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            mhi3mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 5):
                                                                                mhi3mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    mhi3mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi3mai_lista.append("hit")      
                                                         else: mhi3mai_lista.append("p3")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                        inicio = 2
                        while(n<cuadrante):
                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0  


                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                        vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0 
                            
                            

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                                vela7 = 1 
                            else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                    vela7 = -1
                                        else: vela7 = 0 

                            
                            if(martingala >= 3):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0
                            
                            if inicio <= 952:

                                if(martingala >= 4):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else: 
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else:
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                mhi3mai_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela5 > 0):
                                    mhi3mai_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela5 < 0):
                                        mhi3mai_lista.append("win")
                                    else:   
                                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 1):
                                                mhi3mai_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 1):
                                                    mhi3mai_lista.append("g1")       
                                                else:     
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 2):
                                                        mhi3mai_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 2):
                                                            mhi3mai_lista.append("g2")  
                                                        else:    
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 3):
                                                                mhi3mai_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 3):   
                                                                    mhi3mai_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 952:                                
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 4):
                                                                        mhi3mai_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 4):   
                                                                            mhi3mai_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 5):
                                                                                mhi3mai_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                    mhi3mai_lista.append("g5")
                                                                                else:    
                                                                                    mhi3mai_lista.append("hit")      
                                                                 else: mhi3mai_lista.append("p4")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 2 or minuto == 7:                 
                    inicio = 2
                    while(n<cuadrante):
                        if data[inicio]['open'] < data[inicio]['close']: 
                           vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                              vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                           vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                            vela5 = 1 
                        else:
                                if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                    vela5 = -1
                                else: vela5 = 0  

                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0 

                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                            vela7 = 1 
                        else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                                vela7 = -1
                                    else: vela7 = 0 

                        if(martingala >= 3):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                    else: vela8 = 0

                        if(martingala >= 4):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else: 
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                    else: vela9 = 0

                        if inicio <= 952:

                            if(martingala >= 5): 
                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                    vela10 = 1 
                                else:
                                    if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                vela10 = -1
                                    else: vela10 = 0     

                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            mhi3mai_lista.append("none")
                        else:
                            if(vela0 + vela1 + vela2 > 0 and vela5 > 0):
                                mhi3mai_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela5 < 0):
                                    mhi3mai_lista.append("win")
                                else:   
                                        if(vela0 + vela1 + vela2 > 0 and vela6 > 0 and martingala >= 1):
                                            mhi3mai_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela6 < 0 and martingala >= 1):
                                                mhi3mai_lista.append("g1")       
                                            else:     
                                                if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 2):
                                                    mhi3mai_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 2):
                                                        mhi3mai_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 3):
                                                            mhi3mai_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 3):   
                                                                mhi3mai_lista.append("g3")
                                                            else:                                
                                                                if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 4):
                                                                    mhi3mai_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 4):   
                                                                        mhi3mai_lista.append("g4") 
                                                                    else:
                                                                     if inicio <= 952:    
                                                                        if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 5):
                                                                            mhi3mai_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 5):   
                                                                                mhi3mai_lista.append("g5")
                                                                            else:    
                                                                                mhi3mai_lista.append("hit")      
                                                                     else: mhi3mai_lista.append("p5")
                        
                        inicio = inicio + 5
                        n = n + 1
            except:pass

        def catalogo_melhor(data,minuto):
            try: 
                global melhor_lista
                melhor_lista = []
                cuadrante = 192
                martingala = 5
                n = 0 
                
                if minuto == 3 or minuto == 8:
                        inicio = 6
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                else: vela6 = 0
                            

                            if inicio <= 956: 

                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                        else: vela7 = 0 

                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 4):
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else: 
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 11]['open'] < data[inicio + 11]['close']: 
                                        vela11 = 1 
                                    else:
                                        if data[inicio + 11]['open'] > data[inicio + 11]['close']:
                                                    vela11 = -1
                                        else: vela11 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                melhor_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela6 > 0):
                                    melhor_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela6 < 0):
                                        melhor_lista.append("win")
                                    else: 
                                        if inicio <= 956:      
                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 1):
                                                melhor_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 1):
                                                    melhor_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 2):
                                                        melhor_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 2):
                                                            melhor_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 3):
                                                                melhor_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 3):   
                                                                    melhor_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 4):
                                                                        melhor_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 4):   
                                                                            melhor_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela11 > 0 and martingala >= 5):
                                                                                melhor_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela11 < 0 and martingala >= 5):   
                                                                                    melhor_lista.append("g5")
                                                                                else:    
                                                                                    melhor_lista.append("hit")      
                                        else: melhor_lista.append("p1")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 4 or minuto == 9: 
                        inicio = 1
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                                vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                else: vela6 = 0
                        

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                            else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                    else: vela7 = 0 

                            if inicio <= 951:
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                                else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                    vela8 = -1
                                        else: vela8 = 0    

                                if(martingala >= 3):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 4):
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else: 
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 11]['open'] < data[inicio + 11]['close']: 
                                        vela11 = 1 
                                    else:
                                        if data[inicio + 11]['open'] > data[inicio + 11]['close']:
                                                    vela11 = -1
                                        else: vela11 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                melhor_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela6 > 0):
                                    melhor_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela6 < 0):
                                        melhor_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 1):
                                                melhor_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 1):
                                                    melhor_lista.append("g1")       
                                                else:
                                                 if inicio <= 951:      
                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 2):
                                                        melhor_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 2):
                                                            melhor_lista.append("g2")  
                                                        else:  
                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 3):
                                                                melhor_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 3):   
                                                                    melhor_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 4):
                                                                        melhor_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 4):   
                                                                            melhor_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela11 > 0 and martingala >= 5):
                                                                                melhor_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela11 < 0 and martingala >= 5):   
                                                                                    melhor_lista.append("g5")
                                                                                else:    
                                                                                    melhor_lista.append("hit")      
                                                 else: melhor_lista.append("p2")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 0 or minuto == 5:   
                        inicio = 1
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                               vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                else: vela6 = 0
                        

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                            else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                    else: vela7 = 0 


                            if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                            else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                    else: vela8 = 0    

                            if inicio <= 951:
                                if(martingala >= 3):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                                if(martingala >= 4):
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else: 
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 11]['open'] < data[inicio + 11]['close']: 
                                        vela11 = 1 
                                    else:
                                        if data[inicio + 11]['open'] > data[inicio + 11]['close']:
                                                    vela11 = -1
                                        else: vela11 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                melhor_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela6 > 0):
                                    melhor_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela6 < 0):
                                        melhor_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 1):
                                                melhor_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 1):
                                                    melhor_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 2):
                                                        melhor_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 2):
                                                            melhor_lista.append("g2")  
                                                        else: 
                                                         if inicio <= 951:   
                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 3):
                                                                melhor_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 3):   
                                                                    melhor_lista.append("g3")
                                                                else:                               
                                                                    if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 4):
                                                                        melhor_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 4):   
                                                                            melhor_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela11 > 0 and martingala >= 5):
                                                                                melhor_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela11 < 0 and martingala >= 5):   
                                                                                    melhor_lista.append("g5")
                                                                                else:    
                                                                                    melhor_lista.append("hit")      
                                                         else: melhor_lista.append("p3")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 1 or minuto == 6:
                        inicio = 1
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                   vela0 = -1
                                else: vela0 = 0   
                            
                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0   

                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                else: vela6 = 0
                        

                            if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                            else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                    else: vela7 = 0 


                            if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                                vela8 = 1 
                            else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                                vela8 = -1
                                    else: vela8 = 0    

                            if(martingala >= 3):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                    vela9 = -1
                                        else: vela9 = 0

                            if inicio <= 951:
                                if(martingala >= 4):
                                    if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                        vela10 = 1 
                                    else: 
                                        if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                    vela10 = -1
                                        else: vela10 = 0

                                if(martingala >= 5): 
                                    if data[inicio + 11]['open'] < data[inicio + 11]['close']: 
                                        vela11 = 1 
                                    else:
                                        if data[inicio + 11]['open'] > data[inicio + 11]['close']:
                                                    vela11 = -1
                                        else: vela11 = 0     

                            
                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                melhor_lista.append("none")
                            else:
                                if(vela0 + vela1 + vela2 > 0 and vela6 > 0):
                                    melhor_lista.append("win")
                                else:     
                                    if(vela0 + vela1 + vela2 < 0 and vela6 < 0):
                                        melhor_lista.append("win")
                                    else:       
                                            if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 1):
                                                melhor_lista.append("g1") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 1):
                                                    melhor_lista.append("g1")       
                                                else:    
                                                    if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 2):
                                                        melhor_lista.append("g2") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 2):
                                                            melhor_lista.append("g2")  
                                                        else: 
                                                            if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 3):
                                                                melhor_lista.append("g3") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 3):   
                                                                    melhor_lista.append("g3")
                                                                else: 
                                                                 if inicio <= 951:                                
                                                                    if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 4):
                                                                        melhor_lista.append("g4") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 4):   
                                                                            melhor_lista.append("g4") 
                                                                        else:  
                                                                            if(vela0 + vela1 + vela2 > 0 and vela11 > 0 and martingala >= 5):
                                                                                melhor_lista.append("g5") 
                                                                            else:
                                                                                if(vela0 + vela1 + vela2 < 0 and vela11 < 0 and martingala >= 5):   
                                                                                    melhor_lista.append("g5")
                                                                                else:    
                                                                                    melhor_lista.append("hit")      
                                                                 else: melhor_lista.append("p4")
                            
                            inicio = inicio + 5
                            n = n + 1

                if minuto == 2 or minuto == 7:                 
                    inicio = 1
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                             vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                               vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                           vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                            vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0   

                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                            vela6 = 1 
                        else:
                            if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                    vela6 = -1
                            else: vela6 = 0
                    

                        if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                        else:
                                if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                else: vela7 = 0 


                        if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                            vela8 = 1 
                        else:
                                if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                            vela8 = -1
                                else: vela8 = 0    

                        if(martingala >= 3):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                                vela9 = -1
                                    else: vela9 = 0

                        if(martingala >= 4):
                                if data[inicio + 10]['open'] < data[inicio + 10]['close']: 
                                    vela10 = 1 
                                else: 
                                    if data[inicio + 10]['open'] > data[inicio + 10]['close']:
                                                vela10 = -1
                                    else: vela10 = 0

                        if inicio <= 951:
                            if(martingala >= 5): 
                                if data[inicio + 11]['open'] < data[inicio + 11]['close']: 
                                    vela11 = 1 
                                else:
                                    if data[inicio + 11]['open'] > data[inicio + 11]['close']:
                                                vela11 = -1
                                    else: vela11 = 0     

                        
                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            melhor_lista.append("none")
                        else:
                            if(vela0 + vela1 + vela2 > 0 and vela6 > 0):
                                melhor_lista.append("win")
                            else:     
                                if(vela0 + vela1 + vela2 < 0 and vela6 < 0):
                                    melhor_lista.append("win")
                                else:       
                                        if(vela0 + vela1 + vela2 > 0 and vela7 > 0 and martingala >= 1):
                                            melhor_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela7 < 0 and martingala >= 1):
                                                melhor_lista.append("g1")       
                                            else:    
                                                if(vela0 + vela1 + vela2 > 0 and vela8 > 0 and martingala >= 2):
                                                    melhor_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela8 < 0 and martingala >= 2):
                                                        melhor_lista.append("g2")  
                                                    else: 
                                                        if(vela0 + vela1 + vela2 > 0 and vela9 > 0 and martingala >= 3):
                                                            melhor_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela9 < 0 and martingala >= 3):   
                                                                melhor_lista.append("g3")
                                                            else:                                 
                                                                if(vela0 + vela1 + vela2 > 0 and vela10 > 0 and martingala >= 4):
                                                                    melhor_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela10 < 0 and martingala >= 4):   
                                                                        melhor_lista.append("g4") 
                                                                    else: 
                                                                     if inicio <= 951:   
                                                                        if(vela0 + vela1 + vela2 > 0 and vela11 > 0 and martingala >= 5):
                                                                            melhor_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela11 < 0 and martingala >= 5):   
                                                                                melhor_lista.append("g5")
                                                                            else:    
                                                                                melhor_lista.append("hit")      
                                                                     else: melhor_lista.append("p5")
                        
                        inicio = inicio + 5
                        n = n + 1            
            except:pass

        def catalogo_torres(data,minuto):
            try:  
                global torres_lista
                torres_lista = []
                cuadrante = 192
                martingala = 5
                n = 0

                if minuto == 0 or minuto == 5:
                    inicio = 5
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 

                        if inicio <= 955:        

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                            else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                            if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 

                            if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0):
                            torres_lista.append("none")
                        else:
                         if(vela0 > 0 and vela4 > 0):
                            torres_lista.append("win")
                         else:     
                            if(vela0 < 0 and vela4 < 0):
                                torres_lista.append("win")
                            else: 
                                if inicio <= 955:        
                                    if(vela0 > 0 and vela5 > 0  and martingala >= 1):
                                        torres_lista.append("g1") 
                                    else:
                                        if(vela0 < 0 and vela5 < 0 and martingala >= 1):
                                            torres_lista.append("g1")       
                                        else:      
                                            if(vela0 > 0 and vela6 > 0 and martingala >= 2):
                                                torres_lista.append("g2") 
                                            else:
                                                if(vela0 < 0 and vela6 < 0 and martingala >= 2):
                                                    torres_lista.append("g2")  
                                                else:  
                                                    if(vela0 > 0 and vela7 > 0 and martingala >= 3):
                                                       torres_lista.append("g3") 
                                                    else:
                                                        if(vela0 < 0 and vela7 < 0 and martingala >= 3):   
                                                            torres_lista.append("g3")
                                                        else:                               
                                                            if(vela0 > 0 and vela8 > 0 and martingala >= 4):
                                                                torres_lista.append("g4") 
                                                            else:
                                                                if(vela0 < 0 and vela8 < 0 and martingala >= 4):   
                                                                    torres_lista.append("g4") 
                                                                else:  
                                                                    if(vela0 > 0 and vela9 > 0 and martingala >= 5):
                                                                        torres_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 < 0 and vela9 < 0 and martingala >= 5):   
                                                                            torres_lista.append("g5")
                                                                        else:    
                                                                            torres_lista.append("hit")      
                                else: torres_lista.append("p1") 
                    
                        inicio = inicio + 5
                        n = n + 1
                
                if minuto == 1 or minuto == 6:
                    inicio = 5
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        if inicio <= 955:
                            
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                            else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                            if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 

                            if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0):
                            torres_lista.append("none")
                        else:
                         if(vela0 > 0 and vela4 > 0):
                            torres_lista.append("win")
                         else:     
                            if(vela0 < 0 and vela4 < 0):
                                torres_lista.append("win")
                            else:     
                                    if(vela0 > 0 and vela5 > 0  and martingala >= 1):
                                        torres_lista.append("g1") 
                                    else:
                                        if(vela0 < 0 and vela5 < 0 and martingala >= 1):
                                            torres_lista.append("g1")       
                                        else:  
                                         if inicio <= 955:      
                                            if(vela0 > 0 and vela6 > 0 and martingala >= 2):
                                                torres_lista.append("g2") 
                                            else:
                                                if(vela0 < 0 and vela6 < 0 and martingala >= 2):
                                                    torres_lista.append("g2")  
                                                else:    
                                                    if(vela0 > 0 and vela7 > 0 and martingala >= 3):
                                                      torres_lista.append("g3") 
                                                    else:
                                                        if(vela0 < 0 and vela7 < 0 and martingala >= 3):   
                                                            torres_lista.append("g3")
                                                        else:                               
                                                            if(vela0 > 0 and vela8 > 0 and martingala >= 4):
                                                                torres_lista.append("g4") 
                                                            else:
                                                                if(vela0 < 0 and vela8 < 0 and martingala >= 4):   
                                                                    torres_lista.append("g4") 
                                                                else:  
                                                                    if(vela0 > 0 and vela9 > 0 and martingala >= 5):
                                                                        torres_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 < 0 and vela9 < 0 and martingala >= 5):   
                                                                            torres_lista.append("g5")
                                                                        else:    
                                                                            torres_lista.append("hit")      
                                         else: torres_lista.append("p2") 
                    
                        inicio = inicio + 5
                        n = n + 1
                
                if minuto == 2 or minuto == 7:
                    inicio = 5
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  
                        
                        if inicio <= 955:
                            if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 


                            if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0):
                            torres_lista.append("none")
                        else:
                         if(vela0 > 0 and vela4 > 0):
                            torres_lista.append("win")
                         else:     
                            if(vela0 < 0 and vela4 < 0):
                                torres_lista.append("win")
                            else:     
                                    if(vela0 > 0 and vela5 > 0  and martingala >= 1):
                                        torres_lista.append("g1") 
                                    else:
                                        if(vela0 < 0 and vela5 < 0 and martingala >= 1):
                                            torres_lista.append("g1")       
                                        else:      
                                            if(vela0 > 0 and vela6 > 0 and martingala >= 2):
                                                torres_lista.append("g2") 
                                            else:
                                                if(vela0 < 0 and vela6 < 0 and martingala >= 2):
                                                    torres_lista.append("g2")  
                                                else:
                                                 if inicio <= 955:      
                                                    if(vela0 > 0 and vela7 > 0 and martingala >= 3):
                                                       torres_lista.append("g3") 
                                                    else:
                                                        if(vela0 < 0 and vela7 < 0 and martingala >= 3):   
                                                            torres_lista.append("g3")
                                                        else:                                 
                                                            if(vela0 > 0 and vela8 > 0 and martingala >= 4):
                                                                torres_lista.append("g4") 
                                                            else:
                                                                if(vela0 < 0 and vela8 < 0 and martingala >= 4):   
                                                                    torres_lista.append("g4") 
                                                                else:  
                                                                    if(vela0 > 0 and vela9 > 0 and martingala >= 5):
                                                                        torres_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 < 0 and vela9 < 0 and martingala >= 5):   
                                                                            torres_lista.append("g5")
                                                                        else:    
                                                                            torres_lista.append("hit")      
                                                 else: torres_lista.append("p3") 
                    
                        inicio = inicio + 5
                        n = n + 1
                
                if minuto == 3 or minuto == 8:
                    inicio = 5
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 

                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        
                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  
                        

                        if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 

                        if inicio <= 955:
                            if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0):
                            torres_lista.append("none")
                        else:
                         if(vela0 > 0 and vela4 > 0):
                            torres_lista.append("win")
                         else:     
                            if(vela0 < 0 and vela4 < 0):
                                torres_lista.append("win")
                            else:     
                                    if(vela0 > 0 and vela5 > 0  and martingala >= 1):
                                        torres_lista.append("g1") 
                                    else:
                                        if(vela0 < 0 and vela5 < 0 and martingala >= 1):
                                            torres_lista.append("g1")       
                                        else:      
                                            if(vela0 > 0 and vela6 > 0 and martingala >= 2):
                                                torres_lista.append("g2") 
                                            else:
                                                if(vela0 < 0 and vela6 < 0 and martingala >= 2):
                                                    torres_lista.append("g2")  
                                                else:    
                                                    if(vela0 > 0 and vela7 > 0 and martingala >= 3):
                                                        torres_lista.append("g3") 
                                                    else:
                                                        if(vela0 < 0 and vela7 < 0 and martingala >= 3):   
                                                            torres_lista.append("g3")
                                                        else: 
                                                         if inicio <= 955:                                  
                                                            if(vela0 > 0 and vela8 > 0 and martingala >= 4):
                                                                torres_lista.append("g4") 
                                                            else:
                                                                if(vela0 < 0 and vela8 < 0 and martingala >= 4):   
                                                                    torres_lista.append("g4") 
                                                                else:  
                                                                    
                                                                    if(vela0 > 0 and vela9 > 0 and martingala >= 5):
                                                                        torres_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 < 0 and vela9 < 0 and martingala >= 5):   
                                                                            torres_lista.append("g5")
                                                                        else:    
                                                                            torres_lista.append("hit")      
                                                         else: torres_lista.append("p4") 
                    
                        inicio = inicio + 5
                        n = n + 1
                                    
                if minuto == 4 or minuto == 9:
                    inicio = 0
                    while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0   
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 


                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                        if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 

                        if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 
                        
                        if inicio <= 950:

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0):
                            torres_lista.append("none")
                        else:
                         if(vela0 > 0 and vela4 > 0):
                            torres_lista.append("win")
                         else:     
                            if(vela0 < 0 and vela4 < 0):
                                torres_lista.append("win")
                            else:       
                                    if(vela0 > 0 and vela5 > 0  and martingala >= 1):
                                        torres_lista.append("g1") 
                                    else:
                                        if(vela0 < 0 and vela5 < 0 and martingala >= 1):
                                            torres_lista.append("g1")       
                                        else:    
                                            if(vela0 > 0 and vela6 > 0 and martingala >= 2):
                                                torres_lista.append("g2") 
                                            else:
                                                if(vela0 < 0 and vela6 < 0 and martingala >= 2):
                                                    torres_lista.append("g2")  
                                                else:  
                                                    if(vela0 > 0 and vela7 > 0 and martingala >= 3):
                                                       torres_lista.append("g3") 
                                                    else:
                                                        if(vela0 < 0 and vela7 < 0 and martingala >= 3):   
                                                            torres_lista.append("g3")
                                                        else:                               
                                                            if(vela0 > 0 and vela8 > 0 and martingala >= 4):
                                                                torres_lista.append("g4") 
                                                            else:
                                                                if(vela0 < 0 and vela8 < 0 and martingala >= 4):   
                                                                    torres_lista.append("g4") 
                                                                else:  
                                                                 if inicio <= 950:  
                                                                    if(vela0 > 0 and vela9 > 0 and martingala >= 5):
                                                                        torres_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 < 0 and vela9 < 0 and martingala >= 5):   
                                                                            torres_lista.append("g5")
                                                                        else:    
                                                                            torres_lista.append("hit")      
                                                                 else: torres_lista.append("p5") 
                    
                        inicio = inicio + 5
                        n = n + 1
            except:pass

        def catalogo_padrao3x1(data,minuto):
            try:  
                    global padrao3x1_lista
                    padrao3x1_lista = []
                    cuadrante = 192
                    martingala = 5
                    n = 0

                    if minuto == 0 or minuto == 5:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                    vela0 = -1
                                else: vela0 = 0

                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0       
                            
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                    else: vela4 = 0 

                            if inicio <= 955:        

                                if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                                else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0 

                            
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0  

                                if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                    else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                        else: vela7 = 0 

                                if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                            vela8 = -1
                                        else: vela8 = 0 

                                if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                            vela9 = -1
                                        else: vela9 = 0  

                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao3x1_lista.append("none")
                            else:
                             if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                padrao3x1_lista.append("win")
                             else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                    padrao3x1_lista.append("win")
                                else: 
                                    if inicio <= 955:        
                                        if(vela0 + vela1 + vela2 > 0 and vela5 < 0  and martingala >= 1):
                                            padrao3x1_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                padrao3x1_lista.append("g1")       
                                            else:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                    padrao3x1_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                        padrao3x1_lista.append("g2")  
                                                    else:  
                                                        if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                          padrao3x1_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                padrao3x1_lista.append("g3")
                                                            else:                               
                                                                if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                    padrao3x1_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                        padrao3x1_lista.append("g4") 
                                                                    else:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                            padrao3x1_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                padrao3x1_lista.append("g5")
                                                                            else:    
                                                                                padrao3x1_lista.append("hit")      
                                    else: padrao3x1_lista.append("p1") 
                        
                            inicio = inicio + 5
                            n = n + 1
                    
                    if minuto == 1 or minuto == 6:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                    vela0 = -1
                                else: vela0 = 0  

                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0     
                            
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                    else: vela4 = 0 

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0 

                            if inicio <= 955:
                                
                                if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                                else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0  

                                if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                    else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                        else: vela7 = 0 

                                if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                            vela8 = -1
                                        else: vela8 = 0 

                                if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                            vela9 = -1
                                        else: vela9 = 0  

                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao3x1_lista.append("none")
                            else:
                             if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                padrao3x1_lista.append("win")
                             else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                    padrao3x1_lista.append("win")
                                else:     
                                        if(vela0 + vela1 + vela2 > 0 and vela5 < 0  and martingala >= 1):
                                            padrao3x1_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                padrao3x1_lista.append("g1")       
                                            else:  
                                             if inicio <= 955:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                    padrao3x1_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                        padrao3x1_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                             padrao3x1_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                padrao3x1_lista.append("g3")
                                                            else:                               
                                                                if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                    padrao3x1_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                        padrao3x1_lista.append("g4") 
                                                                    else:  
                                                                        if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                            padrao3x1_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                padrao3x1_lista.append("g5")
                                                                            else:    
                                                                                padrao3x1_lista.append("hit")      
                                             else: padrao3x1_lista.append("p2") 
                        
                            inicio = inicio + 5
                            n = n + 1
                    
                    if minuto == 2 or minuto == 7:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                    vela0 = -1
                                else: vela0 = 0  

                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                               vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0     
                            
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                    else: vela4 = 0 

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0 

                            
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0  
                            
                            if inicio <= 955:
                                if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                    else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                        else: vela7 = 0 


                                if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                            vela8 = -1
                                        else: vela8 = 0 

                                if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                            vela9 = -1
                                        else: vela9 = 0  

                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao3x1_lista.append("none")
                            else:
                             if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                padrao3x1_lista.append("win")
                             else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                    padrao3x1_lista.append("win")
                                else:     
                                        if(vela0 + vela1 + vela2 > 0 and vela5 < 0  and martingala >= 1):
                                            padrao3x1_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                padrao3x1_lista.append("g1")       
                                            else:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                    padrao3x1_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                        padrao3x1_lista.append("g2")  
                                                    else:
                                                     if inicio <= 955:      
                                                       if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                            padrao3x1_lista.append("g3") 
                                                       else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                            padrao3x1_lista.append("g3")
                                                        else:                                 
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                padrao3x1_lista.append("g4") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                    padrao3x1_lista.append("g4") 
                                                                else:  
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                        padrao3x1_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                            padrao3x1_lista.append("g5")
                                                                        else:    
                                                                            padrao3x1_lista.append("hit")      
                                                     else: padrao3x1_lista.append("p3") 
                    
                        inicio = inicio + 5
                        n = n + 1
                
                    if minuto == 3 or minuto == 8:
                        inicio = 5
                        while(n<cuadrante):

                            if data[inicio]['open'] < data[inicio]['close']: 
                                vela0 = 1 
                            else:
                                if data[inicio]['open'] > data[inicio]['close']:
                                    vela0 = -1
                                else: vela0 = 0 

                            if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                                vela1 = 1 
                            else:
                                if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                    vela1 = -1
                                else: vela1 = 0    
                                
                            if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                               vela2 = 1 
                            else:
                                if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                    vela2 = -1
                                else: vela2 = 0      
                            
                            if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                                vela4 = 1 
                            else:
                                    if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                        vela4 = -1
                                    else: vela4 = 0 

                            if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                    vela5 = 1 
                            else:
                                        if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                            vela5 = -1
                                        else: vela5 = 0 

                            
                            if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                    vela6 = 1 
                            else:
                                        if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                            vela6 = -1
                                        else: vela6 = 0  
                            

                            if(martingala >= 3): 
                                    if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                        vela7 = 1 
                                    else:
                                        if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                            vela7 = -1
                                        else: vela7 = 0 

                            if inicio <= 955:
                                if(martingala >= 4):
                                    if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                        vela8 = 1 
                                    else:
                                        if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                            vela8 = -1
                                        else: vela8 = 0 

                                if(martingala >= 5):
                                    if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                        vela9 = 1 
                                    else:
                                        if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                            vela9 = -1
                                        else: vela9 = 0  

                            if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                                padrao3x1_lista.append("none")
                            else:
                             if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                                padrao3x1_lista.append("win")
                             else:     
                                if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                    padrao3x1_lista.append("win")
                                else:     
                                        if(vela0 + vela1 + vela2 > 0 and vela5 < 0  and martingala >= 1):
                                            padrao3x1_lista.append("g1") 
                                        else:
                                            if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                                padrao3x1_lista.append("g1")       
                                            else:      
                                                if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                    padrao3x1_lista.append("g2") 
                                                else:
                                                    if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                        padrao3x1_lista.append("g2")  
                                                    else:    
                                                        if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                             padrao3x1_lista.append("g3") 
                                                        else:
                                                            if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                                padrao3x1_lista.append("g3")
                                                            else: 
                                                             if inicio <= 955:                                  
                                                                if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                    padrao3x1_lista.append("g4") 
                                                                else:
                                                                    if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                        padrao3x1_lista.append("g4") 
                                                                    else:  
                                                                        
                                                                        if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                            padrao3x1_lista.append("g5") 
                                                                        else:
                                                                            if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                                padrao3x1_lista.append("g5")
                                                                            else:    
                                                                                padrao3x1_lista.append("hit")      
                                                             else: padrao3x1_lista.append("p4") 
                        
                            inicio = inicio + 5
                            n = n + 1
                                        
                    if minuto == 4 or minuto == 9:
                     inicio = 0
                     while(n<cuadrante):

                        if data[inicio]['open'] < data[inicio]['close']: 
                            vela0 = 1 
                        else:
                            if data[inicio]['open'] > data[inicio]['close']:
                                vela0 = -1
                            else: vela0 = 0  

                        if data[inicio + 1]['open'] < data[inicio + 1]['close']: 
                          vela1 = 1 
                        else:
                            if data[inicio + 1]['open'] > data[inicio + 1]['close']:
                                vela1 = -1
                            else: vela1 = 0    
                            
                        if data[inicio + 2]['open'] < data[inicio + 2]['close']: 
                           vela2 = 1 
                        else:
                            if data[inicio + 2]['open'] > data[inicio + 2]['close']:
                                vela2 = -1
                            else: vela2 = 0     
                        
                        if data[inicio + 4]['open'] < data[inicio + 4]['close']: 
                            vela4 = 1 
                        else:
                                if data[inicio + 4]['open'] > data[inicio + 4]['close']:
                                    vela4 = -1
                                else: vela4 = 0 


                        if data[inicio + 5]['open'] < data[inicio + 5]['close']: 
                                vela5 = 1 
                        else:
                                    if data[inicio + 5]['open'] > data[inicio + 5]['close']:
                                        vela5 = -1
                                    else: vela5 = 0 

                        if data[inicio + 6]['open'] < data[inicio + 6]['close']: 
                                vela6 = 1 
                        else:
                                    if data[inicio + 6]['open'] > data[inicio + 6]['close']:
                                        vela6 = -1
                                    else: vela6 = 0  

                        if(martingala >= 3): 
                                if data[inicio + 7]['open'] < data[inicio + 7]['close']: 
                                    vela7 = 1 
                                else:
                                    if data[inicio + 7]['open'] > data[inicio + 7]['close']:
                                        vela7 = -1
                                    else: vela7 = 0 

                        if(martingala >= 4):
                                if data[inicio + 8]['open'] < data[inicio + 8]['close']: 
                                    vela8 = 1 
                                else:
                                    if data[inicio + 8]['open'] > data[inicio + 8]['close']:
                                        vela8 = -1
                                    else: vela8 = 0 
                        
                        if inicio <= 950:

                            if(martingala >= 5):
                                if data[inicio + 9]['open'] < data[inicio + 9]['close']: 
                                    vela9 = 1 
                                else:
                                    if data[inicio + 9]['open'] > data[inicio + 9]['close']:
                                        vela9 = -1
                                    else: vela9 = 0  

                        if(vela0 == 0 or vela1 == 0 or vela2 == 0):
                            padrao3x1_lista.append("none")
                        else:
                         if(vela0 + vela1 + vela2 > 0 and vela4 < 0):
                            padrao3x1_lista.append("win")
                         else:     
                            if(vela0 + vela1 + vela2 < 0 and vela4 > 0):
                                padrao3x1_lista.append("win")
                            else:       
                                    if(vela0 + vela1 + vela2 > 0 and vela5 < 0  and martingala >= 1):
                                        padrao3x1_lista.append("g1") 
                                    else:
                                        if(vela0 + vela1 + vela2 < 0 and vela5 > 0 and martingala >= 1):
                                            padrao3x1_lista.append("g1")       
                                        else:    
                                            if(vela0 + vela1 + vela2 > 0 and vela6 < 0 and martingala >= 2):
                                                padrao3x1_lista.append("g2") 
                                            else:
                                                if(vela0 + vela1 + vela2 < 0 and vela6 > 0 and martingala >= 2):
                                                    padrao3x1_lista.append("g2")  
                                                else:  
                                                    if(vela0 + vela1 + vela2 > 0 and vela7 < 0 and martingala >= 3):
                                                         padrao3x1_lista.append("g3") 
                                                    else:
                                                        if(vela0 + vela1 + vela2 < 0 and vela7 > 0 and martingala >= 3):   
                                                            padrao3x1_lista.append("g3")
                                                        else:                               
                                                            if(vela0 + vela1 + vela2 > 0 and vela8 < 0 and martingala >= 4):
                                                                padrao3x1_lista.append("g4") 
                                                            else:
                                                                if(vela0 + vela1 + vela2 < 0 and vela8 > 0 and martingala >= 4):   
                                                                    padrao3x1_lista.append("g4") 
                                                                else:  
                                                                 if inicio <= 950:  
                                                                    if(vela0 + vela1 + vela2 > 0 and vela9 < 0 and martingala >= 5):
                                                                        padrao3x1_lista.append("g5") 
                                                                    else:
                                                                        if(vela0 + vela1 + vela2 < 0 and vela9 > 0 and martingala >= 5):   
                                                                            padrao3x1_lista.append("g5")
                                                                        else:    
                                                                            padrao3x1_lista.append("hit")      
                                                                 else: padrao3x1_lista.append("p5") 
                    
                        inicio = inicio + 5
                        n = n + 1            
            except: pass


        def start(divisa):
            try:  
                    data,hora = llamar_velas(divisa)

                    hilo_mhi = threading.Thread(target=catalogo_mhi, args=(data,hora,))  
                    hilo_mhi.start() 
                    hilo_mhimai = threading.Thread(target=catalogo_mhimai, args=(data,hora,))  
                    hilo_mhimai.start()
                    hilo_milhao = threading.Thread(target=catalogo_milhao, args=(data,hora,))  
                    hilo_milhao.start()
                    hilo_milhaomai = threading.Thread(target=catalogo_milhaomai, args=(data,hora,))  
                    hilo_milhaomai.start()

                    hilo_mhi2 = threading.Thread(target=catalogo_mhi2, args=(data,hora,))  
                    hilo_mhi2.start()
                    hilo_mhi2mai = threading.Thread(target=catalogo_mhi2mai, args=(data,hora,))  
                    hilo_mhi2mai.start()
                    hilo_padrao23 = threading.Thread(target=catalogo_padrao23, args=(data,hora,))  
                    hilo_padrao23.start()

                    hilo_mhi3 = threading.Thread(target=catalogo_mhi3, args=(data,hora,))  
                    hilo_mhi3.start() 
                    hilo_mhi3mai = threading.Thread(target=catalogo_mhi3mai, args=(data,hora,))  
                    hilo_mhi3mai.start()
                    hilo_melhor = threading.Thread(target=catalogo_melhor, args=(data,hora,))  
                    hilo_melhor.start()

                    hilo_torres = threading.Thread(target=catalogo_torres, args=(data,hora,))  
                    hilo_torres.start()
                    hilo_padrao3x1 = threading.Thread(target=catalogo_padrao3x1, args=(data,hora,))  
                    hilo_padrao3x1.start()

                    

                    hilo_mhi.join()
                    hilo_mhimai.join()
                    hilo_milhao.join()
                    hilo_milhaomai.join()
                    

                    hilo_mhi2.join()
                    hilo_mhi2mai.join()
                    hilo_padrao23.join()

                    hilo_mhi3.join()
                    hilo_mhi3mai.join()
                    hilo_melhor.join()

                    hilo_torres.join()
                    hilo_padrao3x1.join()
            except:pass  


        comision = llamar_divisas()
                     
        if len(comision) > 0:
                        
                                    divisa = comision[0]['divisa']  
                                    comision2 = comision[0]['type']
                    
                                    start(divisa)
                                
                                    diccionario1 = {
                                        "divisa": divisa,
                                        "nombre": "MHI",
                                        "comision": comision2,
                                        "catalogo":mhi_lista,
                                    }

                                    diccionario2 = {
                                        "divisa": divisa,
                                        "nombre": "MHI Mayoría",
                                        "comision": comision2,
                                        "catalogo":mhimai_lista,
                                    }

                                    diccionario3 = {
                                        "divisa": divisa,
                                        "nombre": "MHI2",
                                        "comision": comision2,
                                        "catalogo":mhi2_lista,
                                    }

                                    diccionario4 = {
                                        "divisa": divisa,
                                        "nombre": "MHI2 Mayoría",
                                        "comision": comision2,
                                        "catalogo":mhi2mai_lista,
                                    }

                                    diccionario5 = {
                                        "divisa": divisa,
                                        "nombre": "MHI3",
                                        "comision": comision2,
                                        "catalogo":mhi3_lista,
                                    }

                                    diccionario6 = {
                                        "divisa": divisa,
                                        "nombre": "MHI3 Mayoría",
                                        "comision": comision2,
                                        "catalogo":mhi3mai_lista,
                                    }

                                    diccionario7 = {
                                        "divisa": divisa,
                                        "nombre": "Milhão Minoría",
                                        "comision": comision2,
                                        "catalogo":milhao_lista,
                                    }

                                    diccionario8 = {
                                        "divisa": divisa,
                                        "nombre": "Milhão Mayoría",
                                        "comision": comision2,
                                        "catalogo":milhaomai_lista,
                                    }

                                    diccionario9 = {
                                        "divisa": divisa,
                                        "nombre": "Melhor de 3",
                                        "comision": comision2,
                                        "catalogo":melhor_lista,
                                    }

                                    diccionario10 = {
                                        "divisa": divisa,
                                        "nombre": "Padrão 23",
                                        "comision": comision2,
                                        "catalogo":padrao23_lista,
                                    }

                                    diccionario11 = {
                                        "divisa": divisa,
                                        "nombre": "Torres Gemelas",
                                        "comision": comision2,
                                        "catalogo":torres_lista,
                                    }


                                    diccionario12 = {
                                        "divisa": divisa,
                                        "nombre": "Padrão 3x1",
                                        "comision": comision2,
                                        "catalogo":padrao3x1_lista,
                                    }
                                    
                                    mercado = []

                                    mercado.append(diccionario1)
                                    mercado.append(diccionario2)
                                    mercado.append(diccionario3)
                                    mercado.append(diccionario4)
                                    mercado.append(diccionario5)
                                    mercado.append(diccionario6)
                                    mercado.append(diccionario7)
                                    mercado.append(diccionario8)
                                    mercado.append(diccionario9)
                                    mercado.append(diccionario10)
                                    mercado.append(diccionario11)
                                    mercado.append(diccionario12)
                                    mercado_json = json.dumps(mercado)

                                    print(mercado_json)
        return mercado_json
                                    
                                    

                          
                                  

