# -*- coding: utf-8 -*-
"""
Created on Thu May 18 08:19:26 2023

@author: from Smirnoff Shots: [G___S____]
"""

# v0.1
    
"""
Este programa debería informar al usuario de ciertas estadísticas basándose en los datos del
registro de saltos anteriores.

Algunas de estas estadísticas podrían ser:
    
    Percentil en el que se encuentra en base a la altura conseguida en base a la media de sus saltos
    
    Gráficas donde se muestren la fuerza, potencia, altura, etc. Los datos deberían ser organizados por
    fecha.
"""

#####################################################################################################
# Importación de paquetes y ficheros
#####################################################################################################

# Fichero que contiene las funciones para leer el registro de saltos

import registroSaltos as rs

# Resto de paquetes

import numpy as np
import matplotlib.pyplot as plt
import tempfile
import os

# v1.0

#####################################################################################################
                                                                                                    #
# Variable con el contenido del registro de satos; IMPORTANTE                                       #
                                                                                                    #
saltos_por_usuario = rs.leerRegistro()                                                              #
                                                                                                    #
#####################################################################################################


#####################################################################################################
# Funciones para saber el percentil correspondiente a distintas facultades
#####################################################################################################

# Con esta función podemos saber a qué percentil se aproxima más un usuario en una categoría.
#
# Recoge: un valor numérico que corresponde con una magnitud medida y/o calculada,
# un lista con los valores clave de los percentiles de la categoría deseada
# 
# Devuleve: un número entero que se corresponde con el percentil al que más 
# se ajusta 

def clasificacionPercentil(magnitud_media, tabla_percentiles):
    try:
        if  not np.issubdtype(type(magnitud_media), np.float64):
            raise ValueError
        
        if magnitud_media <= tabla_percentiles[0]:
            percentil = "5%"
        elif magnitud_media <= tabla_percentiles[1]:
            percentil = "10%"
        elif magnitud_media <= tabla_percentiles[2]:
            percentil = "25%"
        elif magnitud_media <= tabla_percentiles[3]:
            percentil = "50%"
        elif magnitud_media <= tabla_percentiles[4]:
            percentil = "75%"
        elif magnitud_media <= tabla_percentiles[5]:
            percentil = "90%"
        elif magnitud_media <= tabla_percentiles[6]:
            percentil = "95%"
        else:
            percentil = "100%"

        return percentil

    except TypeError:
        mensajError = "Error: TypeError"
        return mensajError
    
    except ValueError:
        mensajError = "Error: ValueError"
        return mensajError
    
    except IndexError:
        mensajError = "Error: IndexError"
        return mensajError
    
# La siguiente función recoge los datos correspondientes a una magnitud de un salto guardado
# en el registro y calcula la media total de estos. Esto se hace porque se quiere determinar
# el percentil al que más se ajusta el usuario y necesitamos un solo valor para hacerlo.
# La media de los valores parece la mejor opción.
#
# Recoge: la magnitud deseada, el nombre de usuario en el registro de saltos y una variable con el registro
#
# Devuelve: un valor numérico que corresponde a la media de los valores

def magnitudMedia(magnitud, username, diccionario_con_saltos):
    valores = []
    
    for saltos in diccionario_con_saltos[username]:
        valor = saltos[magnitud]
        valores.append(valor)
        
    media = np.mean(valores)
        
    return media

# Función en la que se guardan los resultados de las funciones anteriores
# y la información relativa a cada magnitud que deseamos analizar.
#
# Recoge: el nombre del usuario del que se analizan sus datos
#
# Devuelve: el percentil al que corresponde la media de su:
# altura máxima alcanzada, potencia máxima relativa y 
# fuerza máxima relativa

def calculoPercentiles(username, sexo):
    saltos_por_usuario = rs.leerRegistro()
    
    tablaPercentilesAlturaHombres = [245,267,299,332,369,411,434]
    tablaPercentilesPotenciaHombres = [35.96,38.17,41.78,45.90,50.60,55.34,58.14]
    tablaPercentilesFuerzaHombres = [19.37,20.50,21.60,23.20,25.31,27.34,28.75]
    
    tablaPercentilesAlturaMujeres = [180,201,217,246,268,303,327]
    tablaPercentilesPotenciaMujeres = [28.28,29.57,32.47,35.74,39.59,43.93,47.03]
    tablaPercentilesFuerzaMujeres = [17.94,18.46,19.65,21.08,23.01,24.99,26.16]
    
    alturaMedia = magnitudMedia("altura",username,saltos_por_usuario)
    potenciaMedia = magnitudMedia("potencia",username,saltos_por_usuario)
    fuerzaMedia = magnitudMedia("fuerza",username,saltos_por_usuario)
    
    if sexo == "Hombre":
        percentilAltura = clasificacionPercentil(alturaMedia,tablaPercentilesAlturaHombres)
        percentilPotencia = clasificacionPercentil(potenciaMedia,tablaPercentilesPotenciaHombres)
        percentilFuerza = clasificacionPercentil(fuerzaMedia,tablaPercentilesFuerzaHombres)
        
    else:
        percentilAltura = clasificacionPercentil(alturaMedia,tablaPercentilesAlturaMujeres)
        percentilPotencia = clasificacionPercentil(potenciaMedia,tablaPercentilesPotenciaMujeres)
        percentilFuerza = clasificacionPercentil(fuerzaMedia,tablaPercentilesFuerzaMujeres)
    
    return percentilAltura, percentilPotencia, percentilFuerza

#####################################################################################################
# Funciones para mostrar las estadísticas de los saltos del usuario de forma histórica
#####################################################################################################

def datos_registro(diccionario_con_saltos,username):
    
    saltos_usuario = diccionario_con_saltos[username]
    
    alturas = []
    potencias = []
    fuerzas = []
    
    for salto in saltos_usuario:
        alturas.append(salto["altura"])
        potencias.append(salto["potencia"])
        fuerzas.append(salto["fuerza"])
        
    return alturas, potencias, fuerzas

def datos_correctos_estadisticas(alturas, potencias, fuerzas):
    try:
        
        if not(len(alturas) == len(potencias) and len(potencias) == len(fuerzas)):
            raise IndexError
            
        alturas_f = [float(milimetros) for milimetros in alturas]
        potencias_f = [float(vatios) for vatios in potencias]
        fuerzas_f = [float(newtons) for newtons in fuerzas]
        
    except ValueError:
        mensaje = "Comprueba que sean del tipo correcto: una lista con solo números."
        return (False, mensaje)
        
    except IndexError:
        mensaje = "Comprueba que tengas la misma cantidad de datos en todas las magnitudes."
        return (False, mensaje)
    
    return alturas_f, potencias_f, fuerzas_f, True

def grafica(datosAltura, datosPotencia, datosFuerza, username):
    
    datosCheck = datos_correctos_estadisticas(datosAltura, datosPotencia, datosFuerza)[-1]
    
    if datosCheck:
        ejeX = list(range(len(datosAltura)))
        
        plt.figure()
        plt.subplot(311)
        plt.bar(ejeX,datosAltura,label="Alturas alcanzadas",color="red")
        plt.xlabel("Salto")
        plt.ylabel("Altura (mm)")
        plt.title("Estadísticas de {0}".format(username))
        plt.grid(True)
        plt.subplot(312)
        plt.bar(ejeX,datosAltura,label="Potencia consumida",color="blue")
        plt.xlabel("Salto")
        plt.ylabel("Potencia (W)")
        plt.grid(True)
        plt.subplot(313)
        plt.bar(ejeX,datosAltura,label="Fuerza desarrollada",color="green")
        plt.xlabel("Salto")
        plt.ylabel("Fuerza (N)")
        plt.grid(True)

        temp_file = os.path.join('temp_plot.png')
        plt.savefig(temp_file)
        plt.close()
    
        return temp_file
    
    else:
        mensajError = "Uy...\nHa habido un problema con los datos introducidos."
        mensajError += datosCheck[1]


# LO QUE VIENE AHORA ES PARA LA INTERFAZ GRÁFICA

# CUANDO SE ENSEÑE LA IMGEN SE DEBERÍA ACTIVAR ESTA FUNCIÓN PARA QUE NO OCUPE ESPACIO EN EL PC

def eliminar_archivo(temp_file):
    os.remove(temp_file)
    return None
    
"""#AQUÍ ES NECESARIO UN NOMBRE DE USUARIO. HACE FALTA UNA FUNCIÓN QUE NOS DEVUELVA EL NOMBRE DE USUARIO

datos = datos_registro(saltos_por_usuario,"dhong")

datosRevisados = datos_correctos_estadisticas(datos[0], datos[1], datos[2])

temp_file = grafica(datosRevisados[0], datosRevisados[1], datosRevisados[2],"dhong")"""