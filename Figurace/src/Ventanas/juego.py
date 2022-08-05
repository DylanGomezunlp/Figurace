import PySimpleGUI as sg
from config import *
import random

def crear_ventana_juego(categoria, dificultad, opciones, incorrectas, caracteristicas, header, cantidad_rondas=5, perfil= '---', caracteristicas_a_mostrar=5):
    random.shuffle(incorrectas) # mezclo las opciones incorrectas
    data = []
    for i in range(1,(cantidad_rondas + 1)):
        data.append([i,'---']) # creo la lista de rondas con las repuestas, que se mostraran en la ventana. Es decir, se mostrara el numero de ronda y si la opcion que se eligio en esa ronda, es correcta o incorrecta (Aun no tiene funcionalidad, por lo que esta por default vacio)
    img_path_juego = os.path.join(IMG_PATH, f'{categoria}.png')
    title_path = os.path.join(IMG_PATH, 'figurace titulo.png')
    categoria_display = [[sg.Text(f'{categoria}', key=f'-JUEGO-{categoria}-')],
                        [sg.Image(f'{img_path_juego}')]]
                         #Muestro la imagen de la categoria 
    caracteristicas_display = []
    for i in range(0,caracteristicas_a_mostrar):
        caracteristicas_display.append([sg.Text(f"{header[i]} : "), sg.Text(f"{caracteristicas[0][i]}", key= f"-CARACTERISTICAS-{i}")])

    botones = [ [sg.Button(opciones[0], enable_events=True, key="-BOTON-0")],
                        [sg.Button(incorrectas[0], enable_events=True, key ="-BOTON-1")],
                        [sg.Button(incorrectas[1], enable_events=True, key ="-BOTON-2")], #cambiar de la manera que dijo german
                        [sg.Button(incorrectas[2], enable_events=True, key ="-BOTON-3")],
                        [sg.Button(incorrectas[3], enable_events=True, key ="-BOTON-4")]] # los botones de las opciones
    random.shuffle(botones) # mezclo los botones de las opciones
    data_display = ["Ronda", "Respuesta"]
    x = 1
    tarjeta_display = [[sg.Text(f"Ronda Actual : {x} / {cantidad_rondas}", key = '-RONDA-')],
                        [sg.Frame("Caracteristicas", caracteristicas_display)], 
                        [sg.Text("Selecciona una!")],
                        botones[0],
                        botones[1],
                        botones[2],
                        botones[3],
                        botones[4],
                        [sg.Text("Su eleccion: No selecciono nada", key='-ELECCION-')],
                        [sg.Button("Seleccionar", button_color='Green', key='-SELECCIONAR-'), sg.Button("Pasar", button_color='Black', key='-PASAR-')]
                        ] 
    layout = [[sg.Text(f'Dificultad : {dificultad}', background_color= 'red' if dificultad == 'Experto' else 'blue')],
        [[sg.Text(f'Perfil: {perfil}')],
        [sg.Image(title_path,expand_x=True, expand_y=True)],
        sg.Table(values=data, headings=data_display, max_col_width=25, key="-TABLE-"),
        sg.Frame("Categoria", categoria_display), 
        [sg.Text(" ", key="-TIMER-")],
        sg.Frame("Tarjeta", tarjeta_display, key="-TARJETA-")],
        [sg.Button("Abandonar", key="-JUEGO-VOLVER-", button_color='green')]
        ]

    return sg.Window("¡ F I G U R A C E !", layout, finalize=True,  margins=(100, 100)), data, caracteristicas_display


def crear_ventana_comenzar(categoria, cant_rodas, tiempo):
    layout = [[sg.Text(f"La categoria que tendra esta partida es: {categoria}")],
    [sg.Text(f"El tiempo limite por tarjeta que tendra esta partida es: {tiempo}")],
    [sg.Text(f"La cantidad de rondas que tendra esta partida es: {cant_rodas}")],
    [sg.Button("Comenzar!", key = '-COMENZAR-'), sg.Button("Mejor no...", key='-CANCELAR-')]]
    return sg.Window("¡ F I G U R A C E !", layout,  margins=(50, 50))