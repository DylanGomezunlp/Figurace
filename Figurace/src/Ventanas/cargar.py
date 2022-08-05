import os
import csv
from config import *

def cargar_dataset(categoria):
    """Funcion que carga el dataset de la categoria que llega por parametro, y devulve su encabezado(list[str])
    y la lista de datos en la variable dataset(list[list[str]])"""
    dataset = os.path.join(LOCAL_PATH, 'src', 'Archivos', f"{categoria}.csv")
    with open(dataset, encoding= 'Utf-8') as fp:
        csv_reader = csv.reader(fp, delimiter = ',')
        header = next(csv_reader)
        dataset = list(csv_reader)
    return header, dataset

def crear_csv_partidas():
    """Funcion que crea el archivo csv de partidas"""
    with open(os.path.join(LOCAL_PATH, 'src', 'Archivos', 'partidas.csv'), 'w', encoding= 'Utf-8') as fp:
        csv_writer = csv.writer(fp, delimiter = ',')
        csv_writer.writerow(['timestamp', 'id', 'evento', 'usuarie', 'puntos_total', 'estado', 'texto ingresado',
        'respuesta', 'nivel'])

def comenzar_ronda(timestamp, id_partida, nick, dificultad, evento = 'inicio_partida', estado = 'nueva', texto_ingresado = '-',
                   respuesta = '-', puntos = 0):
    with open(os.path.join(LOCAL_PATH, 'src', 'Archivos', 'partidas.csv'), 'a', encoding= 'Utf-8', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter = ',')
        csv_writer.writerow([timestamp, id_partida, evento, nick, puntos, estado, texto_ingresado, respuesta, dificultad])


def aniadir_ronda(timestamp, id_partida, evento, nick, puntos, estado, texto_ingresado, respuesta, nivel):
    """Funcion que aniade una partida al archivo csv de partidas"""
    with open(os.path.join(LOCAL_PATH, 'src', 'Archivos', 'partidas.csv'), 'a', encoding= 'Utf-8', newline='') as fp:
        csv_writer = csv.writer(fp, delimiter = ',')
        csv_writer.writerow([timestamp, id_partida, evento, nick, puntos, estado, texto_ingresado, respuesta, nivel])
        