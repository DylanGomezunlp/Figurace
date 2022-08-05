import random
from time import time
import uuid
import PySimpleGUI as sg
from src.Ventanas.menu import crear_ventana_configuracion, crear_ventana_principal
from src.Ventanas.cargar import cargar_dataset, aniadir_ronda, comenzar_ronda
from src.Ventanas.puntajes import crear_ventana_puntaje, procesar_puntajes
from src.Ventanas.sortear import opciones_rand
from src.Ventanas.juego import crear_ventana_juego
from src.Ventanas.sortear import sortear_dataset
from src.Ventanas.perfiles import crear_ventana_perfiles, crear_archivo_perfiles, crear_perfil, modificar_perfil, leer_perfiles
from src.Ventanas.guardar_datos_dificultad import cargar_personalizado, funcion_dificultad, get_cantidad_rondas, get_cantidad_caracteristicas



keys = ["-BOTON-0", "-BOTON-1", "-BOTON-2", "-BOTON-3", "-BOTON-4"]
ok = False
x = 0
cc, cant_r, pc, pi, tiempo = cargar_personalizado()
crear_archivo_perfiles()
nombres = leer_perfiles()
last_window = crear_ventana_principal(nombres)
while True:
    current_window, event, values = sg.read_all_windows(timeout=100)
    ###MANEJADOR DEL TIMEOUT###
    if event != "__TIMEOUT__":
        last_window = current_window
    else:
        current_window = last_window
        pantalla = current_window
    print(f"Ventana actual: {current_window}, Evento: {event}, valores: {values}")
    if ((event == sg.WIN_CLOSED and sg.popup_yes_no('Seguro de que quiere salir?') == 'Yes') or (event == '-SALIR-' and sg.popup_yes_no('Seguro de que quiere salir?') == 'Yes')): 
        current_window.close()
        break
    ####################################################################################################

    ###MANEJADOR DEL MENU DE CONFIGURACION###
    elif event == "-PRINCIPAL-CONFIGURACION-":
        dificultad = funcion_dificultad(
            values['-PRINCIPAL-DIFICULTAD-'], tiempo, cant_r, pc, pi, cc)
        clave = values['-PRINCIPAL-DIFICULTAD-']
        crear_ventana_configuracion(dificultad, clave)
        current_window.close()
        dificultad, elegido = values['-PRINCIPAL-DIFICULTAD-'], values['-PRINCIPAL-PERFILES-0']
     ####################################################################################################

    ###MANEJADOR DEL EVENTO DE GUARDAR LA CONFIGURACION PERSONALIZADA####
    elif event == "-CONFIGURACION-GUARDAR-" and clave == 'Personalizado':
        dicc = funcion_dificultad(dificultad, values['-CONFIGURACION-TIEMPO-'], values['-CONFIGURACION-RONDAS-'],
                                  values['-CONFIGURACION-CORRECTA-'], values['-CONFIGURACION-INCORRECTA-'], values['-CONFIGURACION-CARACT-'])
        tiempo = values['-CONFIGURACION-TIEMPO-']
        cant_r = values['-CONFIGURACION-RONDAS-']
        pc = values['-CONFIGURACION-CORRECTA-']
        pi = values['-CONFIGURACION-INCORRECTA-']
        cc = values['-CONFIGURACION-CARACT-']
        sg.popup("Se guardo la configuracion correctamente!", title='')
        crear_ventana_configuracion(dicc, clave)
        current_window.close()
        ####################################################################################################
    elif event == "-CONFIGURACION-VOLVER-":
        nombres = leer_perfiles()
        crear_ventana_principal(nombres, dificultad, elegido)
        current_window.close()
    ####################################################################################################

    ###MANEJADOR DEL MENU DE PUNTAJES###
    elif event == "-PRINCIPAL-PUNTAJES-":
        f_max, n_max, d_max, e_max, p_max, f_prom, n_prom, d_prom, e_prom, p_prom = procesar_puntajes()
        crear_ventana_puntaje(f_max, n_max, d_max, e_max, p_max, f_prom, n_prom, d_prom, e_prom, p_prom)
        current_window.close()
        dificultad, elegido = values['-PRINCIPAL-DIFICULTAD-'], values['-PRINCIPAL-PERFILES-0']
    ####################################################################################################

    ###MANEJADOR DEL MENU DE PERFILES###
    elif event == "-PRINCIPAL-PERFILES-":
        crear_ventana_perfiles()
        current_window.close()
        dificultad, elegido = values['-PRINCIPAL-DIFICULTAD-'], values['-PRINCIPAL-PERFILES-0']
    elif event == "Crear nuevo perfil":
        if (values[0] == "" or len(values[0])>5):
            sg.Popup('No puedes crear un perfil vacio o con un nick de mas de 5 caracteres!')
        else:
            crear_perfil(values[0], int(values[1]), values[2])
    elif event == "Modificar perfil":
        modificar_perfil(values[0], int(values[1]), values[2])
    ####################################################################################################

    ###MANEJADOR DEL MENU DE JUEGO###
    elif event == "-PRINCIPAL-JUGAR-" and values['-PRINCIPAL-PERFILES-0'] != "---":
        categoria = sortear_dataset() #sorteo dataset 
        header, dataset = cargar_dataset(categoria) #consigo los datos del dataset
        
        dificultad = values['-PRINCIPAL-DIFICULTAD-'] #agarro la dificultad elegida
        rondas= int(get_cantidad_rondas(dificultad)) #consigo cantidad de rondas segun dificultad
        palabras = [] 
        caracteristicas = []
        if sg.popup_ok_cancel(f"La categoria que tendra esta partida es: {categoria}", 
        f"El tiempo limite por tarjeta que tendra esta partida es: {tiempo}",
        f"La cantidad de rondas que tendra esta partida es: {rondas}", 
        "Quiere comenzar la partida?",
        title='Comenzar?') == "OK": #boton comenzar
            ok = True #Booleano para iniciar el manejador de la pantalla del juego
            x = 0 #variable auxiliar para contabilizar la ronda y actualizar las tarjetas
            for p in dataset:
                palabras.append(p[5])
            cant_caract, tiempo_total= get_cantidad_caracteristicas(dificultad) 
            opciones = opciones_rand(rondas, dataset) # agarro {cant_rondas} listas al azar del dataset
            lista_opciones = []
            for p in opciones:
                lista_opciones.append(p[5])  # pongo el dato a adivinar en esa lista
                caracteristicas.append(p[0:5])   # pongo en la lista de caracteristicas, la que corresponde con la opcion correcta
            lista_errores = list(set(palabras) - set(lista_opciones)) # genero una lista con todas las opciones incorrectas y eligo 25 listas de ahi, para no tener problemas en el futuro
            incorrectas = opciones_rand(100, lista_errores)
            last_window, data, caracteristicas_display= crear_ventana_juego(categoria, dificultad, lista_opciones, incorrectas, caracteristicas, header, rondas, values['-PRINCIPAL-PERFILES-0'], cant_caract) #la verdad que ni yo mismo entiendo como ahora no explota todo, pero bueno tiene que ver con el last window de aca kjj
            current_window.close()
            ####################################################################################################
            diccionario_dificultad = funcion_dificultad(values['-PRINCIPAL-DIFICULTAD-'],tiempo,cant_r,pc,pi,cc)
            hora_inicial = time() #inicializo la hora para el timer
            restantes = None #tiempo restante de la ronda
            y = 0 #variable auxiliar para actualizar las opciones de la tarjeta
            ####################variables para guardar en el csv###################
            puntos_total = 0
            id_partida = uuid.uuid4()
            timestamp= int(time())
            nick = values['-PRINCIPAL-PERFILES-0']
            ##################################################################
            current_window = last_window
            dificultad, elegido = values['-PRINCIPAL-DIFICULTAD-'], values['-PRINCIPAL-PERFILES-0']
            comenzar_ronda(timestamp,id_partida, nick, dificultad) #guardo en el csv el inicio de partida
    elif event == "-PRINCIPAL-JUGAR-" and values['-PRINCIPAL-PERFILES-0'] == "---":
        sg.Popup('No has elegido un perfil')
    ##########################################################################################

    ###MANEJADOR DE LA PANTALLA DE JUEGO###
    if ok:
        if event == "-JUEGO-VOLVER-" and sg.popup_yes_no('Seguro de que quiere salir? Perdera todo el progreso de la partida.') == 'Yes':
            timestamp= int(time())
            aniadir_ronda(timestamp, id_partida, 'cancelada' , nick, 0, '-', '-' , '-', dificultad) 
            #si se cancela la partida, guardo la partida como cancelada y regreso al inicio
            current_window.close()
            ok = False #regreso el booleano del manejador del juego a falso para que termine de ejecutar el evento del timer.
            last_window = crear_ventana_principal(nombres, dificultad,elegido)
            
        ##################################### EL COSO QUE DICE LA OPCION QUE TOCASTE #####################################################
        elif event in keys:
            opcion = current_window[event].get_text()
            current_window["-ELECCION-"].update(f"Su eleccion: {opcion}")
        
        ############################# TIMER #############################################################
        elif hora_inicial:
            transcurridos = int(time() - hora_inicial)
            restantes = tiempo_total - transcurridos
            if restantes <= 0:
                hora_inicial = None
                current_window["-TIMER-"].update("Tiempo agotado")
                sg.popup("Tiempo agotado, siguiente ronda!")
                time_out = True
                event = '-PASAR-' #termina ronda, pasa siguiente tarjeta o termina juego
            else:
                time_out = False
                current_window["-TIMER-"].update(f"Quedan {restantes} segundos")
        ################################ CAMBIO DE TARJETA ##########################################################
        match event:
            case "-PASAR-": 
                timestamp= int(time())
                if x<len(data)-1:
                    evento = 'Intento'
                    #################ACTUALIZACION DE LA TABLITA####################################################################
                    data[x][1] = "MAL!"
                    puntos_total -= pi #resto los puntos de esa ronda
                    current_window["-TABLE-"].update(values=data)
                    try:
                        aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'TimeOut' if time_out else data[x][1], opcion , lista_opciones[x], dificultad)
                    except: #aca hay un try except, porque puede pasar que alguna variable no este definida al momento del time out o del evento pasar
                        aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'TimeOut' if time_out else data[x][1], '-' , lista_opciones[x], dificultad)####################################################################################
                    x = x + 1 #x es ronda anterior, x+1 es ronda actual
                    current_window["-RONDA-"].update(f"Ronda Actual : {x+1} / {rondas}")
                    ################################ACTUALIZACION DE LA TARJETA##############################################################
                    i = random.randint(0,4)
                    current_window[f"-BOTON-{i}"].update(lista_opciones[x])#actualizo la opcion correcta
                    for j in range(0, 4):
                        if j != i:
                            y = y + 1
                            current_window[f"-BOTON-{j}"].update(incorrectas[y]) #actualizo las opciones incorrectas
                    for i in range(0,cant_caract):
                        current_window[f"-CARACTERISTICAS-{i}"].update(caracteristicas[x][i])#actualizo las caracteristicas
                    hora_inicial = time() #actualizo el timer
                else:
                    sg.popup("No hay mas rondas")
                    try: 
                        if opcion == lista_opciones[x]: #elif por si nunca se toco nada al inicio del juego. es decir, desde el inicio es todo timeout
                            respuesta = 'BIEN!'
                        elif opcion != lista_opciones[x]:
                            respuesta = 'MAL!'
                        else:
                            respuesta = 'TimeOut'
                    except:
                        respuesta = 'TimeOut'
                    try:
                        aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'TimeOut' if time_out else data[x][1], opcion , lista_opciones[x], dificultad)
                    except:
                        aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'TimeOut' if time_out else data[x][1], '-' , lista_opciones[x], dificultad)
                    evento = 'Fin'
                    aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'Finalizada', '-', '-', dificultad) #añado la ronda final
                    ok = False
                    sg.popup("Su puntaje es: " + str(puntos_total)) #muestro el puntaje del jugador en esa partida, y regreso al menu principal
                    last_window = crear_ventana_principal(nombres, dificultad, elegido)
                    current_window.close()
            case "-SELECCIONAR-":
                timestamp= int(time()) #coloco el time stamp de ese momento.
                try:
                    evento = 'Intento'
                    if opcion == "No selecciono nada":
                        sg.popup("Seleccione una opcion!")
                    else:
                        if ((x<len(data)-1) and (opcion == lista_opciones[x])):
                            data[x][1] = "BIEN!"
                            puntos_total += pc
                            current_window["-TABLE-"].update(values=data)
                            aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, data[x][1] if data[x][1] in ('BIEN!', 'MAL!') else 'TimeOut', opcion, lista_opciones[x], dificultad)
                            x = x + 1 #x es ronda actual
                            current_window["-RONDA-"].update(f"Ronda Actual : {x+1} / {rondas}")
                            ################################ACTUALIZACION DE LA TARJETA##############################################################
                            i = random.randint(0,4)
                            current_window[f"-BOTON-{i}"].update(lista_opciones[x])#actualizo la opcion correcta
                            for j in range(0, 4):
                                if j != i:
                                    y = y + 1
                                    current_window[f"-BOTON-{j}"].update(incorrectas[y]) #actualizo las opciones incorrectas
                            for i in range(0,cant_caract):
                                current_window[f"-CARACTERISTICAS-{i}"].update(caracteristicas[x][i])
                            ################################ACTUALIZACION DEL COSO QUE TE DICE QUE OPCION TOCASTE##############################################################
                            opcion = "No selecciono nada"
                            current_window["-ELECCION-"].update(f"Su eleccion: {opcion}")
                            hora_inicial = time() #reinicio timer
                        elif ((x<len(data)-1) and (opcion != lista_opciones[x])):
                            data[x][1] = "MAL!"
                            puntos_total -= pi
                            current_window["-TABLE-"].update(values=data)
                            aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, data[x][1] if data[x][1] in ('BIEN!', 'MAL!') else 'TimeOut', opcion, lista_opciones[x], dificultad)
                            x = x + 1 #x es ronda actual
                            current_window["-RONDA-"].update(f"Ronda Actual : {x+1} / {rondas}")
                            ################################ACTUALIZACION DE LA TARJETA##############################################################
                            i = random.randint(0,4)
                            current_window[f"-BOTON-{i}"].update(lista_opciones[x])#actualizo la opcion correcta
                            for j in range(0, 4):
                                if j != i:
                                    y = y + 1
                                    current_window[f"-BOTON-{j}"].update(incorrectas[y]) #actualizo las opciones incorrectas
                            for i in range(0,cant_caract):
                                current_window[f"-CARACTERISTICAS-{i}"].update(caracteristicas[x][i])
                            ################################ACTUALIZACION DEL COSO QUE TE DICE QUE OPCION TOCASTE##############################################################
                            opcion = "No selecciono nada"
                            current_window["-ELECCION-"].update(f"Su eleccion: {opcion}")
                            hora_inicial = time()#reinicio timer
                        else:
                            timestamp= int(time())
                            sg.popup("No hay mas rondas")#aca va la cantidad de puntajes
                            try: 
                                if opcion == lista_opciones[x]:
                                    respuesta = 'BIEN!'
                                elif opcion != lista_opciones[x]:
                                    respuesta = 'MAL!'
                                else:
                                    respuesta = 'TimeOut'
                            except:
                                respuesta = 'TimeOut'
                            aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, respuesta, opcion, lista_opciones[x], dificultad)
                            evento = 'Fin'
                            timestamp= int(time())
                            aniadir_ronda(timestamp, id_partida, evento,nick, puntos_total, 'Finalizada', '-', '-', dificultad)
                            ok = False
                            sg.popup("Su puntaje es: " + str(puntos_total))
                            last_window = crear_ventana_principal(nombres,dificultad,elegido)
                            current_window.close()
                except:
                    sg.popup("Seleccione una opcion!") # si no selecciono una opcion, es decir, opcion no va a estar definida, indica que se seleccione una