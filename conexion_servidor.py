"""
@author: from Smirnoff Shots: [MarcMasters]

Este programa almacena las funciones que se encargan del inicio de sesión, la obtención de la leaderboard y
el registro de un salto todo esto manteniendo una conexión con el servidor.

Para ello, pide al usuario introducir manualmente su usuario y contraseña registrados previamente en el 
servidor y un 'Nickname' o apodo con el que este será reconocido en sus saltos.
"""
# Paquetes -----------------------------------------------------------------------------------------------------------------------
from socket import *
from json import *
import numpy as np
import time
from datetime import date

# Datos necesarios para la conexión TCP-------------------------------------------------------------------------------------------

dir_IP_serv = '158.42.188.200'                                                 # Dirección IP del servidor
puerto_serv = 64010                                                            # Puerto del servidor
dir_socket_servidor = (dir_IP_serv, puerto_serv)                               # Socket

s = socket(AF_INET, SOCK_STREAM)                                               # TCP: SOCK_STREAM
s.connect(dir_socket_servidor)                                                 # Conexión del socket al servidor


# Funciones------------------------------------------------------------------------------------------------------------------------

# Función para obtener IPv4 actual del cliente
def get_ip():
    return s.getsockname()[0]

# Función de inicio de sesión
def login(user,passw):
    global s
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(dir_socket_servidor)
    
    # HELLO
    mensaje_tx = "HELLO "+get_ip()+"\n"                                        # Primer contacto con el servidor 'HELLO 158.42.46.79' (p.ej)
    s.send(mensaje_tx.encode())                                                # Se envía el mensaje con el método 'send'
    mensaje_rx = s.recv(2048)                                                  # Cada vez que se envía un mensaje al servidor, este responde
                                                                               #  y el programa lo recibe con el método 'recv'
    # USER
    mensaje_rx = "".encode()
    fhand = open("user_data.txt","w",encoding="utf-8")                         # Se crea un fichero para guardar el nombre de usuario para el 
                                                                               # uso de este por otras funciones.
    while mensaje_rx.decode()[0:3] != "200":                                   # Se pide al usuario su 'nombre de usuario' y 'contraseña' registrados                                                                      #  en el servidor. Si estos no lo están lo vuelve a hacer
        mensaje_tx = "USER "+user+"\n"                                         # en el servidor. Si estos no lo están lo vuelve a hacer.
        s.send(mensaje_tx.encode())                                            # Estos se envian al servidor con 'USER (nombre)' y 'PASS (contraseña)'
        mensaje_rx = s.recv(2048)
        if mensaje_rx.decode()[0:3] != "200":
            return True
        else:                                                                  # Se escribe en el fichero el nombre de usuario una vez el programa
            fhand.write(user)                                                  # detecta mediante la respuesta del servidor que es correcto.
    fhand.close()
            
    # PASSWORD
    mensaje_rx = "".encode()
    while mensaje_rx.decode()[0:3] != "200":
        mensaje_tx = "PASS "+passw+"\n"
        s.send(mensaje_tx.encode())
        mensaje_rx = s.recv(2048)
        if mensaje_rx.decode()[0:3] != "200":
            return True
        
# Esta función muestra el ranking de los 10 mejores saltos y
#  los almacena en un fichero "ranking.txt" para su posterior uso.
#
# Tiene un parámetro de entrada 'show=True' por defecto.
# Esto es debido a que para ejecutar otra función más adelante ('comparativa()'),
#  esta requiere el fichero 'ranking.txt' que se genera, y mediante el booleano
#  'show' se evita mostrar todo lo que la función muestra al ejecutarse.

def get_lb():                                                        
    mensaje_tx = "GET_LEADERBOARD\n"                                          # Se envía el comando para obtener el TOP 10: 'GET_LEADERBOARD'
    s.send(mensaje_tx.encode())
    mensaje_rx = s.recv(2048)
                                                  
    fhand = open("ranking.txt","w",encoding="utf-8")
    while mensaje_rx.decode()[0:3] != "202":                                  # Bucle que recibe todas las entradas del ranking hasta
        mensaje_rx = s.recv(2048)                                             # que el servidor devuelve el último mensaje ('202 NO MORE RECORDS')
        if mensaje_rx.decode()[0:3] != "202":
            fhand.write(mensaje_rx.decode())
    fhand.close()


# Función que registra los datos de un salto dados en el servidor
def send_data(nombre_alumn,cod_grupo,h):
    # Datos a introducir para el LOG-IN en el servidor
    fecha = date.today().strftime("%d-%m-%Y")
    
    data = {"nombre"      : nombre_alumn,                                      # Diccionario para almacenar los datos del salto (formato JSON)
            "grupo_ProMu" : cod_grupo,
            "altura"      : h,
            "fecha"       : fecha       }

    js = dumps(data)                                                           # Conversión de diccionario de Python a 'string de formato JSON'
    js = "".join(js.split())                                                   # y eliminación de los espacios para que tenga el formato que
                                                                               # exige el servidor.
                                                                               
    mensaje_tx = "SEND_DATA "+js+"\n"                                          # Se envían los datos del salto con el comando 'SEND_DATA "datos"'
    s.send(mensaje_tx.encode())    
    mensaje_rx = s.recv(2048)
    
# Función (EXTRA) que compara la altura de tu salto registrado con las del ranking
#
# Esta función tiene como parámetros la altura del salto a registrar 'user_h'
# y un fichero="ranking.txt" por defecto que es el que produce la función get_lb()
# como se ha comentado previamente. De este fichero se extraen los saltos registrados
# en el TOP 10 para compararlos con el salto registrado por el usuario.

def comparativa(user_h,fichero="ranking.txt"):
    fhand = open(fichero,"r",encoding="utf-8")
    for line in fhand:
        salto_registrado = line.strip()
        if line != "\n":
            salto_registrado = loads(line)                                     # Extracción de la altura del string en formato json convirtiéndolo a dict() de Python
            h_i = salto_registrado["altura"]                                   # Altura del salto del fichero que se trata según la iteración del bucle
            if user_h > h_i and salto_registrado["ranking"] == "1":
                return("¡ENHORABUENA! Te has convertido en el TOP 1 del ranking!!")
                break
            elif user_h > h_i:
                return("¡Enhorabuena! Has entrado en el TOP 10. Concretamente, te has situado en el TOP {0}, a {1} milímetro(s) del TOP {2}.".format(salto_registrado["ranking"],h_i_prev-user_h,int(salto_registrado["ranking"])-1 ))
                break
            elif user_h == h_i:
                if salto_registrado["ranking"] == "1":
                    return("¡ENHORABUENA! Te has convertido en el TOP 1 del ranking!!Pero no estás solo, ¡ha habido un empate!")
                    break
                else:
                    return("¡Enhorabuena! Has entrado en el TOP 10. Concretamente, has empatado en el TOP {0}, a {1} milímetro(s) del TOP {2}.".format(salto_registrado["ranking"],h_i_prev-user_h,int(salto_registrado["ranking"])-1 ))
                    break
            elif user_h < h_i and salto_registrado["ranking"] == "10":
                return("Lo lamento, no has entrado en el TOP 10. Para ello, tendrás que saltar {0} milímetro(s) más alto.".format(h_i-user_h))
            h_i_prev = salto_registrado["altura"]                              # Variable que almacena lo mismo que 'h_i' pero más tarde, de forma que sirve
                                                                               # para comparar con el anterior dato de altura tratado.
    fhand.close()

# Función para convertir en lista de listas el fichero 'ranking.txt'
#
# Esta función no se usa en este programa, pero es necesaria por
# cuestiones de formato para la interfaz.

def listar(fichero="ranking.txt"):
    fhand = open(fichero,"r",encoding="utf-8")
    rank_list = []
    for line in fhand:
        salto_registrado = line.strip()
        if line != "\n":
            salto_registrado = loads(line)
            salto_registrado = list(salto_registrado.values())
            rank_list.append(salto_registrado)
    return rank_list

# Función para guardar el nombre de usuario,el grupo y el sexo en el archivo "user_data.txt"
#
# Esta función no se usa en este programa, pero es necesario para el programa principal.

def guardar(nombre,grupo,sexo,fichero="user_data.txt"):
    fhand= open(fichero,"r",encoding="utf-8")
    
    for line in fhand:
        cuenta= line.strip("\n")
        break
    
    fhand.close()

    fhand2= open(fichero,"w",encoding="utf-8")
    fhand2.write(cuenta + "\n" + nombre + "\n" + grupo + "\n" + sexo)
    fhand2.close()

# Función para cerrar sesión
def salir():
    mensaje_tx = "QUIT\n"                                                      # Se envía el comando 'QUIT' al servidor para cerrar la sesión
    s.send(mensaje_tx.encode())
    mensaje_rx = s.recv(2048)

