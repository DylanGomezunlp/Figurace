import json
import os  
from config import *

def funcion_dificultad(values,tiempo,cant_r,pc,pi,cc):
    """Funcion que crea el archivo con los datos de dificultad personalizados, o lee los datos de la dificultad elegida

    Args:
        values (Str): La dificultad que selecciono el usuario
        tiempo (int): Tiempo de la partida
        cant_r (int): Cantidad de rondas de la partida
        pc (int): Puntaje sumado por cada opcion correcta
        pi (int): Puntjae restado por cada opcion incorrecta
        cc (int): Cantidad de caracteristicas a mostrar en la partida

    Returns:
        Dicc[Str, dict[Str:str]]: _description_
    """
    with open(CONFIG_PATH,'r',encoding='utf-8') as dj:
        datos=json.load(dj)
        if(values=='Facil'):
            datos_elegidos=datos[0]
        elif values=='Normal':
            datos_elegidos= datos[1]
        elif values=='Dificil':
            datos_elegidos=datos[2]
        elif values=='Experto':
            datos_elegidos=datos[3]
        else:
            datos_elegidos=  {"Personalizado":{
                                            "tiempo_limite": "0"
                                            ,"cant_rondas": "0"
                                            ,"puntaje_correcto":"0"
                                            ,"puntaje_incorrecta": "0"
                                            ,"cant_caracteristicas" : "0"
                                                }
                                                }
            path = os.path.join(LOCAL_PATH, 'src', 'Archivos', 'custom.json')                                    
            with open(path,'w',encoding='utf-8') as cus:
                datos_elegidos['Personalizado']['tiempo_limite']=tiempo
                datos_elegidos['Personalizado']['cant_rondas']=cant_r
                datos_elegidos['Personalizado']['puntaje_correcto']=pc
                datos_elegidos['Personalizado']['puntaje_incorrecta']=pi
                datos_elegidos['Personalizado']['cant_caracteristicas']= cc
                json.dump(datos_elegidos,cus)
    return datos_elegidos

def get_cantidad_caracteristicas(values):
    """Funcion que retorna la cantidad de caracteristicas que tiene el dataset"""
    with open(CONFIG_PATH,'r',encoding='utf-8') as dj: #necesito leer y escribir el json
        datos=json.load(dj)
        if(values=='Facil'):
            datos_elegidos=datos[0]
        elif values=='Normal':
            datos_elegidos= datos[1]
        elif values=='Dificil':
            datos_elegidos=datos[2]
        elif values=='Experto':
            datos_elegidos=datos[3]
        else:
            path = os.path.join(LOCAL_PATH, 'src', 'Archivos', 'custom.json')
            with open(path) as datos:
                datos_elegidos=json.load(datos)
                return int(datos_elegidos['Personalizado']['cant_caracteristicas']), int(datos_elegidos['Personalizado']['tiempo_limite'])
        return int(datos_elegidos[values]['cant_caracteristicas']), int(datos_elegidos[values]['tiempo_limite'])

def get_cantidad_rondas(values):
    """Funcion que retorna la cantidad de rondas que tiene el dataset"""
    with open(CONFIG_PATH,'r',encoding='utf-8') as dj: #necesito leer y escribir el json
        datos=json.load(dj)
        if(values=='Facil'):
            datos_elegidos=datos[0]
        elif values=='Normal':
            datos_elegidos= datos[1]
        elif values=='Dificil':
            datos_elegidos=datos[2]
        elif values=='Experto':
            datos_elegidos=datos[3]
        else:
            path = os.path.join(LOCAL_PATH, 'src', 'Archivos', 'custom.json')
            with open(path) as datos:
                datos_elegidos=json.load(datos)
                return datos_elegidos['Personalizado']['cant_rondas']
        return datos_elegidos[values]['cant_rondas']

def cargar_personalizado():
    path = os.path.join(LOCAL_PATH, 'src', 'Archivos', 'custom.json')
    with open(path) as datos:
        datos_elegidos=json.load(datos)
        return datos_elegidos['Personalizado']['cant_caracteristicas'], datos_elegidos['Personalizado']['cant_rondas'], datos_elegidos['Personalizado']['puntaje_correcto'], datos_elegidos['Personalizado']['puntaje_incorrecta'], datos_elegidos['Personalizado']['tiempo_limite']