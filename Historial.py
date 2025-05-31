# -*- coding: utf-8 -*-
"""
Created on Sun May 14 11:42:00 2023

@author: from Smirnoff Shots: [G___S____]
"""

"""
Con este programa el usuario debería poder ver los resultados de sus anteriores saltos.
El funcionamientos es el siguiente:
    
    Cada vez que el usuario registra un salto y lo envía el programa recogerá los datos
    que se van a enviar al servidor en formato JSON y los registrará en un fichero .csv
    que contendrá tantos objetos como usuarios hayan enviado un salto desde la aplicación.
    Cada objeto tendrá un diccionario con la información relativa al salto.
    
    La estructura del fichero sería la siguiente:
        
        jumps_by_users = {
            username1: [
                {"altura": altura,
                 "fecha": fecha},
                
                {"altura": altura,
                 "fecha": fecha},
                
                {"altura": altura,
                 "fecha": fecha}],
            
            username2: [
                {"altura": altura,
                 "fecha": feha},
                
                ...],
            ...
            }
        
    Las funcionalidades que debería tener el programa son:
        
        Mostrar los saltos de un usuario con el nombre de este,
        
        Borrar un salto de un usuario, 
        
        """

# Importamos el paquete para trabajar con JSON
import json
from registroSaltos import leerRegistro, updateRegistro

saltos_por_usuario = None


#----------------FUNCIONES------------------------------------------------------------------------------------------------#

#Funciones fundamentales
def inputNombre():
    conseguirNombre = True
    while conseguirNombre:
        fhand= open("user_data.txt","r",encoding="utf-8")
        
        count= 0
        for line in fhand:
            if count==0:
                nombre= line.strip("\n")
            count+=1
    
        fhand.close()
        
        conseguirNombre = False
            
    return nombre


#Funciones para mostrar saltos
def inputsMostrarSaltos():                                                      # Esta función recoge el nombre de un usuario
    nombre = inputNombre()                                                      # para enseñar sus saltos. HACER CON GUI
    datos= mostrarSaltos(nombre)                                                       
    return datos

def mostrarSaltos(username):                                                    # Esta función muestra los saltos de un usuario    
    datos= []
    saltos_por_usuario = leerRegistro()
    
    for i in range(len(saltos_por_usuario[username])):
        altura = saltos_por_usuario[username][i]["altura"]
        fecha = str(saltos_por_usuario[username][i]["fecha"])
        datos.append([i+1,altura,fecha])

    return datos


#Funciones para eliminar saltos
def eliminarSalto(username, numeroSalto):                                       # Esta función elimina el salto de un usuario
    saltos_por_usuario = leerRegistro()
    
    del saltos_por_usuario[username][numeroSalto]                               # a partir de su nombre y el número del salto
    updateRegistro(saltos_por_usuario)
    return None

def inputsEliminarSalto(numSalto):
    saltos_por_usuario = leerRegistro()
    nombre = inputNombre()
    conseguirNumero = True
    while conseguirNumero:
        try:
            salto = saltos_por_usuario[nombre][numSalto]
            conseguirNumero = False
        except IndexError:
            return True

    eliminarSalto(nombre, numSalto)
    return None