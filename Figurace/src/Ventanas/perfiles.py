import PySimpleGUI as sg
import json
from config import *


def leer_perfiles():
    """Funcion que lee los perfiles creados.

    Returns:
        Str: Devuelve una lista con los nombres de los perfiles creados,o un string "-" indicando que no existe ninguno
    """
    with open(PERFILES_PATH, "r") as perfiles:
        datos_perfiles = json.load(perfiles)
        nombres = []
        for i in range(len(datos_perfiles)):

            try:
                nombres.append(datos_perfiles[i]["nick"])
            except:
                nombres.append("-")
    return nombres


def crear_archivo_perfiles():
    """Crea el archivo de perfiles la primera vez que se ejecuta el programa"""
    try:
        perfiles_test = open(PERFILES_PATH, "x")
        inicial = [{"nick": "-",
                    "edad": "-",
                    "genero": "-",
                    "puntaje": 0}]
        json.dump(inicial, perfiles_test)
    except FileExistsError:
        pass


def buscar_nick(actuales, nick):
    """Funcion que busca el nick en el archivo de perfiles.

    Args:
        actuales (List): Lista con los perfiles actuales, son solo 3 perfiles disponibles, asi que solo recorrco
        los ultimos 3 perfiles.
    """
    for elem in actuales:
        if elem["nick"] == nick:
            return True
    return False


def crear_perfil(nick, edad, genero):
    """Crea un perfil nuevo en el archivo de perfiles. Es decir crea
     un nuevo diccionario y lo agrega al archivo de perfiles.

    Args:
        nick (Str): Nick elegido por el usuario
        edad (int): Edad elegida por el usuario
        genero (Str): Genero elegido por el usuario
    """
    with open(PERFILES_PATH, "r") as arch_perfiles:  # ver PATH
        actuales = json.load(arch_perfiles)
        if buscar_nick(actuales, nick):
            sg.popup("El nick elegido ya existe", title='!Algo Ocurrio!')
        else:
            datos = {"nick": nick, "edad": edad,
                     "genero": genero, "puntaje": 0}
            actuales.append(datos)
            with open(PERFILES_PATH, "w") as arch_perfiles:
                json.dump(actuales, arch_perfiles)
            sg.popup("Perfil creado con éxito!")


def modificar_perfil(nick, edad, genero):
    """Modifica el perfil en base al nick que se le pasa por parametro, esta 
    funcion se invoca al tocar "guardar cambios" en la ventana de perfiles.

    Args:
        nick (Str): Nick elegido por el usuario
        edad (int): Edad elegida por el usuario
        genero (Str): Genero elegido por el usuario
    """
    encontre = False
    with open(PERFILES_PATH, "r") as arch_perfiles:  # ver PATH
        datos = json.load(arch_perfiles)
        for elem in datos:
            if elem["nick"] == nick:
                elem["edad"] = edad
                elem["genero"] = genero
                encontre = True
                sg.popup("Perfil modificado!")
                with open(PERFILES_PATH, "w") as arch_perfiles:
                    json.dump(datos, arch_perfiles)

        if encontre == False:
            perfil_no_encontrado()


def perfil_no_encontrado():
    """Funcion que muestra una ventana de error cuando no se encuentra el perfil"""
    sg.popup("El perfil que desea modificar no existe", title='!Algo Ocurrio!')


def crear_ventana_perfiles():
    layout = [[sg.Text('Nick:                    '), sg.InputText()],
              [sg.Text('Edad:                    '), sg.Slider(
                  orientation='h', default_value=18, range=(1, 99))],
              [sg.Text('Género autopercibido:'), sg.OptionMenu(
                  values=('Hombre', 'Mujer', 'Otro'), default_value='Otro')],
              [sg.Button('Crear nuevo perfil'), sg.Button('Modificar perfil')], [sg.Button("Volver  ", key="-CONFIGURACION-VOLVER-", button_color='red')]]

    return sg.Window('Perfiles', layout, finalize=True, margins=(200, 150), element_justification="bottom")
