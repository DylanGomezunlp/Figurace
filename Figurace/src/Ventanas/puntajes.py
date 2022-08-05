import PySimpleGUI as sg
import pandas as pd
from config import *


def procesar_puntajes():
    """lee el csv de partidas y devuelve 10 diccionarios (por cada dificultad: devuelve un diccionario ordenado por puntajes maximos y uno ordenado por promedios"""

    datframe = pd.read_csv(PARTIDAS_PATH, encoding="utf-8")
    filtrado = pd.DataFrame(columns=["usuarie", "nivel", "puntos"])

    for i in datframe.index:
        if datframe["evento"][i] == "Fin":
            filtrado.loc[filtrado.shape[0]] = [datframe["usuarie"]
                                               [i], datframe["nivel"][i], datframe["puntos"][i]]

    filtrado = filtrado.astype({'puntos': 'float'})
    filtrado = filtrado.astype({'puntos': 'int'})
    usuarios = list(filtrado["usuarie"].unique())
    dict_f = dict.fromkeys(usuarios)
    dict_n = dict.fromkeys(usuarios)
    dict_d = dict.fromkeys(usuarios)
    dict_e = dict.fromkeys(usuarios)
    dict_p = dict.fromkeys(usuarios)

    for elem in usuarios:
        cant_f = 0
        cant_n = 0
        cant_d = 0
        cant_e = 0
        cant_p = 0
        max_f = 0
        max_n = 0
        max_d = 0
        max_e = 0
        max_p = 0
        acumulado_f = 0
        acumulado_n = 0
        acumulado_d = 0
        acumulado_e = 0
        acumulado_p = 0
        for i in filtrado.index:

            if filtrado["usuarie"][i] == elem:

                if filtrado["nivel"][i] == "Facil":
                    cant_f += 1
                    acumulado_f += filtrado["puntos"][i]
                    if filtrado["puntos"][i] > max_f:
                        max_f = filtrado["puntos"][i]

                elif filtrado["nivel"][i] == "Normal":
                    cant_n += 1
                    acumulado_n += filtrado["puntos"][i]
                    if filtrado["puntos"][i] > max_n:
                        max_n = filtrado["puntos"][i]

                elif filtrado["nivel"][i] == "Dificil":
                    cant_d += 1
                    acumulado_d += filtrado["puntos"][i]
                    if filtrado["puntos"][i] > max_d:
                        max_d = filtrado["puntos"][i]

                elif filtrado["nivel"][i] == "Experto":
                    cant_e += 1
                    acumulado_e += filtrado["puntos"][i]
                    if filtrado["puntos"][i] > max_e:
                        max_e = filtrado["puntos"][i]
                elif filtrado["nivel"][i] == "Personalizado":
                    cant_p += 1
                    acumulado_p += filtrado["puntos"][i]
                    if filtrado["puntos"][i] > max_p:
                        max_p = filtrado["puntos"][i]
        try:
            prom_f = int(acumulado_f/cant_f)
        except ZeroDivisionError:
            prom_f = 0
        try:
            prom_n = int(acumulado_n/cant_n)
        except ZeroDivisionError:
            prom_n = 0
        try:
            prom_d = int(acumulado_d/cant_d)
        except ZeroDivisionError:
            prom_d = 0
        try:
            prom_e = int(acumulado_e/cant_e)
        except ZeroDivisionError:
            prom_e = 0
        try:
            prom_p = int(acumulado_p/cant_p)
        except ZeroDivisionError:
            prom_p = 0

        dict_f[elem] = {"Max": max_f, "Prom": prom_f}
        dict_n[elem] = {"Max": max_n, "Prom": prom_n}
        dict_d[elem] = {"Max": max_d, "Prom": prom_d}
        dict_e[elem] = {"Max": max_e, "Prom": prom_e}
        dict_p[elem] = {"Max": max_p, "Prom": prom_p}

    list_n = []
    list_f = []
    list_d = []
    list_e = []
    list_p = []

    for key in dict_n:
        dic = {"Nick": key, "Max": dict_n[key]
               ["Max"], "Prom": dict_n[key]["Prom"]}
        list_n.append(dic)
    for key in dict_f:
        dic = {"Nick": key, "Max": dict_f[key]
               ["Max"], "Prom": dict_f[key]["Prom"]}
        list_f.append(dic)
    for key in dict_d:
        dic = {"Nick": key, "Max": dict_d[key]
               ["Max"], "Prom": dict_d[key]["Prom"]}
        list_d.append(dic)
    for key in dict_e:
        dic = {"Nick": key, "Max": dict_e[key]
               ["Max"], "Prom": dict_e[key]["Prom"]}
        list_e.append(dic)
    for key in dict_p:
        dic = {"Nick": key, "Max": dict_p[key]
               ["Max"], "Prom": dict_p[key]["Prom"]}
        list_p.append(dic)

    f_max = sorted(list_f, key=lambda x: x['Max'], reverse=True)
    n_max = sorted(list_n, key=lambda x: x['Max'], reverse=True)
    d_max = sorted(list_d, key=lambda x: x['Max'], reverse=True)
    e_max = sorted(list_e, key=lambda x: x['Max'], reverse=True)
    p_max = sorted(list_p, key=lambda x: x['Max'], reverse=True)
    f_prom = sorted(list_f, key=lambda x: x['Prom'], reverse=True)
    n_prom = sorted(list_n, key=lambda x: x['Prom'], reverse=True)
    d_prom = sorted(list_d, key=lambda x: x['Prom'], reverse=True)
    e_prom = sorted(list_e, key=lambda x: x['Prom'], reverse=True)
    p_prom = sorted(list_p, key=lambda x: x['Prom'], reverse=True)

    return f_max, n_max, d_max, e_max, p_max, f_prom, n_prom, d_prom, e_prom, p_prom



def crear_ventana_puntaje(facil, normal, dificil, experto, personalizado, facil_prom, normal_prom, dificil_prom, experto_prom, personalizado_prom):
    """crea ventana con los puntajes de cada nivel, y con el puntaje promedio por nivel"""
    heading = ["Pos" ,"Nick", "Puntajes"]
    i = 0
    facil_data = []
    normal_data = []
    dificil_data = []
    experto_data = []
    personalizado_data = []
    facil_prom_data = []
    normal_prom_data = []
    dificil_prom_data = []
    experto_prom_data = []
    personalizado_prom_data = []
    for (k0,k1,k2,k3,k4,k5,k6,k7,k8,k9) in zip(facil, normal, dificil, experto, personalizado, facil_prom, normal_prom, dificil_prom, experto_prom, personalizado_prom):
        i = i + 1
        facil_data.append([i, k0["Nick"], k0["Max"]])
        normal_data.append([i, k1["Nick"], k1["Max"]])
        dificil_data.append([i, k2["Nick"], k2["Max"]])
        experto_data.append([i, k3["Nick"], k3["Max"]])
        personalizado_data.append([i, k4["Nick"], k4["Max"]])
        facil_prom_data.append([i, k5["Nick"], k5["Prom"]])
        normal_prom_data.append([i, k6["Nick"], k6["Prom"]])
        dificil_prom_data.append([i, k7["Nick"], k7["Prom"]])
        experto_prom_data.append([i, k8["Nick"], k8["Prom"]])
        personalizado_prom_data.append([i, k9["Nick"], k9["Prom"]])
    layout = [[sg.Text("20 MEJORES PUNTAJES POR DIFICULTAD!")],
              [sg.Text("Facil:", text_color="Blue"),
               sg.Table(values=facil_data, headings=heading, max_col_width=25),
               sg.Text("Normal:", text_color="Blue"),
               sg.Table(values=normal_data, headings=heading, max_col_width=25),
               sg.Text("Dificil:", text_color='black'),
               sg.Table(values= dificil_data, headings=heading, max_col_width=25),
               sg.Text("Experto:", text_color='red'),
               sg.Table(values=experto_data, headings=heading, max_col_width=25),
               sg.Text("Personalizado:", text_color='red'),
               sg.Table(values=personalizado_data, headings=heading, max_col_width=25)],
                [sg.Text("20 MEJORES PUNTAJES POR PROMEDIO!")],
                [sg.Text("Facil:", text_color="Blue"),
                    sg.Table(values=facil_prom_data, headings=heading, max_col_width=25),
                    sg.Text("Normal:", text_color="Blue"),
                    sg.Table(values=normal_prom_data, headings=heading, max_col_width=25),
                    sg.Text("Dificil:", text_color='black'),
                    sg.Table(values=dificil_prom_data, headings=heading, max_col_width=25),
                    sg.Text("Experto:", text_color='red'),
                    sg.Table(values=experto_prom_data, headings=heading, max_col_width=25),
                    sg.Text("Personalizado:", text_color='red'),
                    sg.Table(values=personalizado_prom_data, headings=heading, max_col_width=25)],
              [sg.Button("Volver", key="-CONFIGURACION-VOLVER-", button_color='red')]]

    return sg.Window("Puntajes!", layout, finalize=True, margins=(200, 150))
