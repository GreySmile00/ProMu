# -*- coding: utf-8 -*-
"""
Created on Thu May 18 08:44:53 2023

@author: from Smirnoff Shots: [G___S____]
"""

"""
Como las funciones que leen el histroial de saltos van a ser usadas en otros programas,
pondré esas funciones en este fichero para beneficiar la organización a la hora de 
importar programas.
"""

# Importamos el paquete para trabajar con JSON

import json

###############################################################################
# Función para leer el fichero con el registro de saltos
###############################################################################

#ESTO SE TIENE QUE EJECUTAR NADA MÁS UTILIZAR CUALQUIER FUNCIÓN QUE MODIFIQUE EL REGISTRO

def leerRegistro():                                                             # Esta es una función esencial para este programa.
    saltos = {}                                                                 # Se busca el fichero .json con el registro de
    buscaRegistro = True                                                        # los saltos que se han enviado.
    while buscaRegistro:
        try:                                                                    
                                                                                
            fhand = open("saltosAnteriores.json","r")                           
            buscaRegistro = False                                               
            
        except FileNotFoundError:                                               # Si no existe se crea uno con un objeto vacío
            fhand = open("saltosAnteriores.json","w")                           # para poder trabajar con él.
            json.dump(saltos, fhand)
            fhand.close()
            
    saltos = json.load(fhand)                                                   # Cuando exista, toda la información del registro
    fhand.close()                                                               # se deposita en una variable como diccionario
            
    return saltos

###############################################################################
# Función para sobreescribir en el fichero del registro de saltos
###############################################################################

def updateRegistro(variable_con_registro):                                      # Esta función sobreescribe el contenido
                                                                                # del registro con la información de la
    fhand_write = open("saltosAnteriores.json","w")                             # variable que se le introduzca
    json.dump(variable_con_registro, fhand_write)
    
    fhand_write.close()
    return None

###############################################################################
# Función para añadir saltos
###############################################################################

def registrarSalto(saltoFormatoJSON, diccionarioSaltos):
    
    user = saltoFormatoJSON["nombre"] 
        
    nuevoSalto = {
        "altura": saltoFormatoJSON["altura"],
        "potencia": saltoFormatoJSON["potencia"],
        "fuerza":saltoFormatoJSON["fuerza"],
        "fecha": saltoFormatoJSON["fecha"]}
    
    if user not in diccionarioSaltos:
        diccionarioSaltos[user] = []
    
    diccionarioSaltos[user].append(nuevoSalto)
    
    updateRegistro(diccionarioSaltos)
    
    return None

