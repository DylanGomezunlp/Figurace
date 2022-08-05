import PySimpleGUI as sg
import os
from config import *



sg.theme('LightBrown8')


def crear_ventana_principal(nombres, clave='Experto', elegido='---'):
    img_logo= os.path.join(IMG_PATH, 'gatubi logo.png')
    layout = [
        [sg.Image(img_logo, expand_x=True, expand_y=True)],
        [sg.Button("!JUGAR!", key='-PRINCIPAL-JUGAR-', button_color='brown', expand_x=True, expand_y=True)],
        [sg.Text('DIFICULTAD', expand_x=True, expand_y=True), sg.OptionMenu(values=('Facil', 'Normal', 'Dificil',
                                                      'Experto', 'Personalizado'),  key='-PRINCIPAL-DIFICULTAD-', default_value=clave)],
        [sg.Button("Configuracion", key='-PRINCIPAL-CONFIGURACION-', expand_x=True, expand_y=True)],
        [sg.Button("Puntajes", key='-PRINCIPAL-PUNTAJES-', expand_x=True, expand_y=True)],
        [sg.Button("Perfiles", key="-PRINCIPAL-PERFILES-", expand_x=True, expand_y=True), sg.OptionMenu(
            values=(nombres), key='-PRINCIPAL-PERFILES-', default_value=elegido, expand_x=True, expand_y=True)],
        [sg.Button("Salir", key="-SALIR-", button_color='red', expand_x=True, expand_y=True)]
    ]
    return sg.Window("FIGURACE", layout, finalize=True, default_button_element_size=(10, 2), margins=(200, 100))


def crear_ventana_configuracion(dificultad, clave='Experto'):
    layout = [
        [sg.Text("Cantidad de rondas"), sg.InputOptionMenu(
            ['5','10','15','20'], default_value=dificultad[clave]['cant_rondas'], k='-CONFIGURACION-RONDAS-', disabled= True if clave != 'Personalizado' else False)],
        [sg.Text("Tiempo limite"),sg.Slider(range=(1,180),orientation='h',default_value=dificultad[clave]['tiempo_limite'] , k='-CONFIGURACION-TIEMPO-', disabled= True if clave != 'Personalizado' else False)],
        [sg.Text("Puntaje sumado por respuesta correcta"), sg.Slider(
            orientation='h', key='-CONFIGURACION-CORRECTA-', default_value=dificultad[clave]['puntaje_correcto'], disabled= True if clave != 'Personalizado' else False)],
        [sg.Text("Puntaje restado por respuesta incorrecta"),sg.Slider(
            orientation='h', key='-CONFIGURACION-INCORRECTA-', default_value=dificultad[clave]['puntaje_incorrecta'], disabled= True if clave != 'Personalizado' else False)],
        [sg.Text("Cantidad de caracteristicas a tomar"), sg.InputOptionMenu(
            ["1", "2", "3", "4", "5"], key='-CONFIGURACION-CARACT-'
        ,default_value=dificultad[clave]['cant_caracteristicas'], disabled= True if clave != 'Personalizado' else False)],
        [sg.Button("Volver  ", key="-CONFIGURACION-VOLVER-", button_color='red'), sg.Button("Guardar Cambios", key="-CONFIGURACION-GUARDAR-", button_color='black', disabled= True if clave != 'Personalizado' else False)]] 

    return sg.Window("Configuracion", layout, finalize=True, margins=(200, 150), element_justification="bottom")
