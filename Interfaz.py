#Paquetes y funciones necesarios
from guizero import App, Text, TextBox, PushButton, Box, error, warn, yesno, CheckBox, info, Combo, Picture

from registroSaltos import leerRegistro, updateRegistro, registrarSalto
from Historial import inputNombre, mostrarSaltos, inputsMostrarSaltos, eliminarSalto, inputsEliminarSalto
from conexion_servidor import login, get_lb, listar, guardar, salir, send_data, comparativa
from estadisticasSaltos import calculoPercentiles, datos_registro, datos_correctos_estadisticas, grafica, eliminar_archivo
from analizarSaltos import main_analizar
from extra_stats import extra_stats

import os
import pandas as pd
from datetime import date

# App ---------------------------------------------------------------------
app = App(bg = "#DBDBDB",
          title ="INTERFAZ DE USUARIO V1.3",
          height = 554,
          width = 1024,
          layout= "grid")


# Functions and variables -------------------------------------------------
def cambia_color(boton): #Cambia el color del botón cuando haces un click
    global ide_acceso
    global ide_enviado
    
    if ide_acceso:
        if boton.text != "Estadísticas" and boton.text != "Historial de salto":
            #Reset color
            b1.bg= "#42F2F7"
            b2.bg= "#42F2F7"
            b3.bg= "#42F2F7"
            b4.bg= "#42F2F7"
            b5.bg= "#42F2F7"
        
            #Rest color del texto
            b1.text_color= "black"
            b2.text_color= "black"
            b3.text_color= "black"
            b4.text_color= "black"
            b5.text_color= "black"
        
            #Cambiar el color del boton pulsado y del texto
            boton.bg= "#00076B"
            boton.text_color= "white"
        
        elif ide_enviado:
            #Reset color
            b1.bg= "#42F2F7"
            b2.bg= "#42F2F7"
            b3.bg= "#42F2F7"
            b4.bg= "#42F2F7"
            b5.bg= "#42F2F7"
        
            #Rest color del texto
            b1.text_color= "black"
            b2.text_color= "black"
            b3.text_color= "black"
            b4.text_color= "black"
            b5.text_color= "black"
            
            #Cambiar el color del boton pulsado y del texto
            boton.bg= "#00076B"
            boton.text_color= "white"
        
    elif boton.text=="Iniciar sesión":
        boton.bg= "#00076B"
        boton.text_color= "white"

def cambia_titulo(boton): #Cambia el título del menú principal cuando haces click a un botón.
    global ide_acceso
    global ide_guardado
    global ide_enviado
    
    if boton.text== "Iniciar sesión":
        if not ide_acceso:
            titulo.value= "IDENTIFICACIÓN DEL USUARIO"
        else:
            titulo.value= "INFORMACIÓN PERSONAL"
    
    if ide_acceso:
        if boton.text== "Analizar el salto":
            titulo.value= "ANALIZADOR DEL SALTO"

        elif boton.text== "Leaderboard":
            titulo.value= "LEADERBOARD"
            
        elif ide_enviado and boton.text== "Historial de salto":
            titulo.value= "HISTORIAL"
        
        elif ide_enviado and boton.text== "Estadísticas":
            titulo.value= "ESTADÍSTICAS"

def reset_contenido(): #Convertir todos los componentes en invisibles.
    #Iniciar sesión
    nombre_txt.visible= False
    nombre.visible= False
    psw_txt.visible= False
    psw.visible= False
    psw_visible.visible= False
    boton_iniciar.visible= False
    
    cuenta.visible= False
    box_perfil.visible= False
    usuario_txt.visible= False
    usuario.visible= False
    grupo_txt.visible= False
    grupo.visible= False
    sexo_txt.visible= False
    sexo.visible= False
    text_informativo.visible= False
    box_boton.visible= False
    espacio_entre_boton.visible= False
    boton_guardar.visible= False
    boton_cerrar.visible= False
    
    
    #Analizar saltos
    ruta.visible= False
    espacio_ruta.visible= False
    peso_box.visible= False
    peso_txt.visible= False
    peso.visible= False
    boton_analizar.visible= False
    espacio_datos.visible= False
    datos_box.visible= False
    v_max.visible= False
    f_max.visible= False
    p_max.visible= False
    a_max.visible= False
    v_sol.visible= False
    f_sol.visible= False
    p_sol.visible= False
    a_sol.visible= False
    boton_enviar.visible= False
    boton_info.visible= False
    
    
    #Leaderboard
    L_column1.visible= False
    L_column2.visible= False
    L_column3.visible= False
    L_column4.visible= False
    L_column5.visible= False
    L_r1.visible= False
    L_r2.visible= False
    L_r3.visible= False
    L_r4.visible= False
    L_r5.visible= False
    L_n1.visible= False
    L_n2.visible= False
    L_n3.visible= False
    L_n4.visible= False
    L_n5.visible= False
    L_g1.visible= False
    L_g2.visible= False
    L_g3.visible= False
    L_g4.visible= False
    L_g5.visible= False
    L_a1.visible= False
    L_a2.visible= False
    L_a3.visible= False
    L_a4.visible= False
    L_a5.visible= False
    L_f1.visible= False
    L_f2.visible= False
    L_f3.visible= False
    L_f4.visible= False
    L_f5.visible= False
    
    L_cambia_box.visible= False
    L_anterior.visible= False
    L_siguiente.visible= False
    
    #Historial
    column1.visible= False
    column2.visible= False
    column3.visible= False
    borrar.visible= False
    
    n1.visible= False
    n2.visible= False
    n3.visible= False
    n4.visible= False
    n5.visible= False
    
    a1.visible= False
    a2.visible= False
    a3.visible= False
    a4.visible= False
    a5.visible= False
    
    f1.visible= False
    f2.visible= False
    f3.visible= False
    f4.visible= False
    f5.visible= False
    
    x1.visible= False
    x2.visible= False
    x3.visible= False
    x4.visible= False
    x5.visible= False
    
    cambia_box.visible= False
    anterior.visible= False
    siguiente.visible= False
    
    #Estadísticas
    txt_altura.visible= False
    txt_potencia.visible= False
    txt_fuerza.visible= False
    
    flecha1.visible= False
    flecha2.visible= False
    flecha3.visible= False
    
    percentil1.visible= False
    percentil2.visible= False
    percentil3.visible= False
    
    grafica_estadistica.visible= False

def muestra_contenido(boton): #Activiar la visibilidad de determinados componentes según el botón que has apretado.
    global ide_acceso         #y muestra el contenido que pide el usuario.
    global ide_guardado
    global ide_analizado
    global ide_enviado
    
    if boton.text== "Iniciar sesión":
        reset_contenido()
        
        if not ide_acceso: 
            nombre_txt.visible= True
            nombre.visible= True
            psw_txt.visible= True
            psw.visible= True
            psw_visible.visible= True
            boton_iniciar.visible= True
        
        else:
            cuenta.visible= True
            box_perfil.visible= True
            usuario_txt.visible= True
            usuario.visible= True
            grupo_txt.visible= True
            grupo.visible= True
            sexo_txt.visible= True
            sexo.visible= True
            text_informativo.visible= True
            box_boton.visible= True
            espacio_entre_boton.visible= True
            boton_guardar.visible= True
            boton_cerrar.visible= True
    
    elif ide_acceso and boton.text== "Analizar el salto":
        reset_contenido()
        ruta.visible= True
        espacio_ruta.visible= True
        peso_box.visible= True
        peso_txt.visible= True
        peso.visible= True
        boton_analizar.visible= True
        
        if ide_analizado:
            espacio_datos.visible= True
            datos_box.visible= True
            v_max.visible= True
            f_max.visible= True
            p_max.visible= True
            a_max.visible= True
            v_sol.visible= True
            f_sol.visible= True
            p_sol.visible= True
            a_sol.visible= True
            boton_enviar.visible= True
            boton_info.visible= True
        

    elif ide_acceso and boton.text== "Leaderboard":
        reset_contenido()
        
        #Comando principal
        leaderboard(0,5)
        
        L_column1.visible= True
        L_column2.visible= True
        L_column3.visible= True
        L_column4.visible= True
        L_column5.visible= True
        L_r1.visible= True
        L_r2.visible= True
        L_r3.visible= True
        L_r4.visible= True
        L_r5.visible= True
        L_n1.visible= True
        L_n2.visible= True
        L_n3.visible= True
        L_n4.visible= True
        L_n5.visible= True
        L_g1.visible= True
        L_g2.visible= True
        L_g3.visible= True
        L_g4.visible= True
        L_g5.visible= True
        L_a1.visible= True
        L_a2.visible= True
        L_a3.visible= True
        L_a4.visible= True
        L_a5.visible= True
        L_f1.visible= True
        L_f2.visible= True
        L_f3.visible= True
        L_f4.visible= True
        L_f5.visible= True
        L_cambia_box.visible= True
        L_anterior.visible= True
        L_siguiente.visible= True
        
        
    elif ide_acceso and boton.text== "Historial de salto":
        if ide_enviado:
            reset_contenido()
            
            #Comando principal
            tabla_historial(0,5)
            
            column1.visible= True
            column2.visible= True
            column3.visible= True
            borrar.visible= True
            n1.visible= True
            n2.visible= True
            n3.visible= True
            n4.visible= True
            n5.visible= True
            a1.visible= True
            a2.visible= True
            a3.visible= True
            a4.visible= True
            a5.visible= True
            f1.visible= True
            f2.visible= True
            f3.visible= True
            f4.visible= True
            f5.visible= True
            x1.visible= True
            x2.visible= True
            x3.visible= True
            x4.visible= True
            x5.visible= True
            cambia_box.visible= True
            anterior.visible= True
            siguiente.visible= True
            
        else:
            warn("Tips","Aun no has realizado ningún salto")

    elif ide_acceso and boton.text== "Estadísticas":
        if ide_enviado:
            reset_contenido()
            percentil()
            pinta_grafica()
            
            txt_altura.visible= True
            txt_potencia.visible= True
            txt_fuerza.visible= True
            flecha1.visible= True
            flecha2.visible= True
            flecha3.visible= True
            percentil1.visible= True
            percentil2.visible= True
            percentil3.visible= True
            
            grafica_estadistica.visible= True
            grafica_estadistica.image= "temp_plot.png"
            
        else:
            warn("Tips","Aun no has realizado ningún salto")
        
    else:
        warn("Identificación obligatorio","Debes iniciar sesión para acceder otras ventanas")

def mostra_psw(): #Mostrar el número de contraseñas.
        if psw_visible.value==0:
            psw.hide_text= True
        else:
            psw.hide_text= False

def inicia_sesion(): #Enviar la cuenta y la contraseña al servidor para conseguir permiso.
    global ide_acceso
    global ide_guardado
    
    user= nombre.value
    passw= psw.value

    if login(user,passw):
        warn("Tips","Comprueba tu cuenta o contraseña")
    
    else:
        title= "Bienvenido",user
        info(title,"Ya tienes acceso a otras ventanas")
        ide_acceso= True
        nombre.value=""
        psw.value=""
        psw_visible.value=0
        
        #Mostrar Perfil
        reset_contenido()
        titulo.value= "INFORMACIÓN PERSONAL"
        
        fhand= open("user_data.txt","r",encoding="utf-8")
        contenido= fhand.read()
        fhand.close()
        cuenta.value= "Bienvenido, " + contenido
        
        
        cuenta.visible= True
        box_perfil.visible= True
        usuario_txt.visible= True
        usuario.visible= True
        grupo_txt.visible= True
        grupo.visible= True
        sexo_txt.visible= True
        sexo.visible= True
        text_informativo.visible= True
        box_boton.visible= True
        espacio_entre_boton.visible= True
        boton_guardar.visible= True
        boton_cerrar.visible= True

def cerra_sesion(): #Volver a conectar el servidor y quitar todos los permisos obtenidos.
    global ide_acceso
    global ide_guardado
    global ide_analizado
    global ide_enviado
    
    #Reset usuario y contenido
    login("","")
    reset_contenido()
    ide_acceso= False
    ide_guardado= False
    ide_analizado= False
    ide_enviado= False
    usuario.value=""
    grupo.value=""
    peso.value=""
    
    titulo.value= "IDENTIFICACIÓN DEL USUARIO"
    nombre_txt.visible= True
    nombre.visible= True
    psw_txt.visible= True
    psw.visible= True
    psw_visible.visible= True
    boton_iniciar.visible= True
    
def guarda_datos(): #Guarda la información personal en un fichero "user_data.txt"
    global ide_guardado
    
    if len(usuario.value)!=0 and len(grupo.value)!=0 and len(sexo.value)!=0:
        guardar(usuario.value,grupo.value,sexo.value)
        info("Guardado correctamente","Ya puedes enviar tu salto al servidor")
        ide_guardado= True
    else:
        warn("Tips","Falta completar los datos")
        ide_guardado= False

def analizar(): #Analizar el archivo Excel, muestra los valores calculados y la gráfica.
    global ide_analizado
    
    if peso.value.isdigit():
        fichero= ruta.value
        masa= float(peso.value)
        
        velocidad,fuerza,potencia,altura= main_analizar(fichero,masa)
        
        v_sol.value= velocidad + " m/s"
        f_sol.value= fuerza + " N"
        p_sol.value= potencia + " W"
        a_sol.value= altura + " mm"
        
        espacio_datos.visible= True
        datos_box.visible= True
        v_max.visible= True
        f_max.visible= True
        p_max.visible= True
        a_max.visible= True
        v_sol.visible= True
        f_sol.visible= True
        p_sol.visible= True
        a_sol.visible= True
        boton_enviar.visible= True
        boton_info.visible= True
        
        ide_analizado= True
        
    else:
        error("ERROR","Valor de peso inválido")

def enviar(): #Enviar tu salto analizado al servidor y guarda tu salto en un fichero json.
    global ide_analizado
    global ide_guardado
    global ide_enviado
    global sTotal
    
    if ide_guardado and ide_analizado:
        fhand= open("user_data.txt","r",encoding="utf-8")
        
        count= 0
        for line in fhand:
            if count==1:
                nombre= line.strip("\n")
            elif count==2:
                grupo= line.strip("\n")
            count += 1
        
        fhand.close()
        
        send_data(nombre,grupo,int(float(a_sol.value[:-3])))

        #Información adicional
        get_lb()
        info_txt= comparativa(int(float(a_sol.value[:-3])))
        
        info("Tips",info_txt)
        ide_enviado= True
    
        #Guardar saltos
        nombre= inputNombre()
        altura= int(float(a_sol.value[:-3]))
        potencia= float(p_sol.value[:-2])
        fuerza= float(f_sol.value[:-2])
        fecha= date.today().strftime("[%d-%m-%Y]")
        
        s= [{"nombre": nombre, "altura": altura, "potencia": potencia, "fuerza": fuerza, "fecha": fecha}]
        
        saltos = {}
        sTotal += s
        
        leerRegistro()
        for salto in sTotal:
            registrarSalto(salto,saltos)
    
    else:
        warn("Tips","Antes de enviar, debes completar el perfil y analizar tu salto")

def info_extra(): #Para informar al usuario unos datos divertidos como referencia.
    potencia= float(p_sol.value[:-2])
    
    info_a,info_b= extra_stats(potencia)
    
    info("Tips",info_a)
    info("Tips",info_b)

def leaderboard(a,b,ide=True): #Muestra el leaderboard que nos da el servidor.
    if ide:
        get_lb()
    datos= listar()

    for i in range(a,b):
        if len(datos)>i:
            rank= datos[i][0]
            nombre= datos[i][1]
            grupo= datos[i][2]
            altura= datos[i][3]
            fecha= datos[i][4]
            
            j=0
            for x in datos[i]:
                if len(str(x))>7:
                    if j==0:
                        rank= datos[i][j][:6]+"..."
                    elif j==1:
                        nombre= datos[i][j][:6]+"..."
                    elif j==2:
                        grupo= datos[i][j][:6]+"..."                        
                    elif j==3:
                        altura= str(datos[i][j])[:6]+"..."                        
                    elif j==4:
                        fecha= datos[i][j][:6]+"..."
                j += 1
            
        else:
            rank= "---"
            nombre= "---"
            grupo= "---"
            altura= "---"
            fecha= "---"
         
        if i==a:
            L_r1.value= str(rank)
            L_n1.value= str(nombre)
            L_g1.value= str(grupo)
            L_a1.value= str(altura)
            L_f1.value= str(fecha)
        elif i==a+1:
            L_r2.value= str(rank)
            L_n2.value= str(nombre)
            L_g2.value= str(grupo)
            L_a2.value= str(altura)
            L_f2.value= str(fecha)
        elif i==a+2:
            L_r3.value= str(rank)
            L_n3.value= str(nombre)
            L_g3.value= str(grupo)
            L_a3.value= str(altura)
            L_f3.value= str(fecha)
        elif i==a+3:
            L_r4.value= str(rank)
            L_n4.value= str(nombre)
            L_g4.value= str(grupo)
            L_a4.value= str(altura)
            L_f4.value= str(fecha)                             
        elif i==a+4:
            L_r5.value= str(rank)
            L_n5.value= str(nombre)
            L_g5.value= str(grupo)
            L_a5.value= str(altura)
            L_f5.value= str(fecha)

def L_cambia_pagina(boton): #Cambia la pagina de Leaderboard
    datos= listar()
    if boton.text==">":
        if L_r5.value=="---" or len(datos)<=int(L_r5.value):
            warn("Tips","Ya estás en la última página")
        else:
            leaderboard(5,10,False)
        
    else:
        if (L_r1.value=="---") and (len(datos)!=0):
            leaderboard(0,5,False)
        elif len(datos)<=5 or L_r1.value=="1":
            warn("Tips","Ya estás en la primera página")
        else:  
            leaderboard(0,5,False)

def tabla_historial(a,b): #Muestra los saltos anteriores enviados.
    datos= inputsMostrarSaltos()
    
    for i in range(a,b):
        if len(datos)>i:
            n_salto= datos[i][0]
            altura= datos[i][1]
            fecha= datos[i][2]
        else:
            n_salto= "---"
            altura= "---"
            fecha= "---"
         
        if i==a:
            n1.value= str(n_salto)
            a1.value= str(altura)
            f1.value= str(fecha)
        elif i==a+1:
            n2.value= str(n_salto)
            a2.value= str(altura)
            f2.value= str(fecha)
        elif i==a+2:
            n3.value= str(n_salto)
            a3.value= str(altura)
            f3.value= str(fecha)
        elif i==a+3:
            n4.value= str(n_salto)
            a4.value= str(altura)
            f4.value= str(fecha)                             
        elif i==a+4:
            n5.value= str(n_salto)
            a5.value= str(altura)
            f5.value= str(fecha)

def borra_salto(boton): #Eliminar un salto determinado o todos los saltos.
    ide=True;num=0;si_no=True
    
    if n1.value!="---":
        if boton.text=="x" and str(boton.grid)=="[3, 1]":
            num= int(n1.value)-1
        elif boton.text=="x" and str(boton.grid)=="[3, 2]":
            num= int(n1.value)
        elif boton.text=="x" and str(boton.grid)=="[3, 3]":
            num= int(n1.value)+1
        elif boton.text=="x" and str(boton.grid)=="[3, 4]":
            num= int(n1.value)+2
        elif boton.text=="x" and str(boton.grid)=="[3, 5]":
            num= int(n1.value)+3
    
        elif boton.text=="Borrar Historial":
            ide=False
            datos= inputsMostrarSaltos()
            
            if len(datos)==0:
                error("ERROR","Aún no has realizado ningún salto")
            else:
                si_no= yesno("Borrar Historial","¿Estás seguro de que quieres eliminar todos los saltos?")
                if si_no:
                    for i in range(len(datos)):
                        inputsEliminarSalto(0)
    
    if ide and inputsEliminarSalto(num)==True:
        """
        Este comando condicional se ejecuta en todos los casos (se elimina un determinado salto)
        pero lo de dentro sólo se ejecuta cuando produce un IndexError(eliminando un salto que no existe)
        """
        error("ERROR","No puedes eliminar un salto que no existe")
    
    if ide and n1.value!="---":
        a= int(n1.value)-1
        b= a+5
    else:
        if si_no:
            a=0
            b=5
        else:
            a= int(n1.value)-1
            b= a+5
    
    tabla_historial(a,b)
    

def cambia_pagina(boton): #Cambiar la página del Historial.
    datos= inputsMostrarSaltos()
    if boton.text==">":
        if n5.value=="---" or len(datos)<=int(n5.value):
            warn("Tips","Ya estás en la última página")
        else:
            a= int(n5.value)
            b= a+5
            tabla_historial(a,b)
        
    else:
        if (n1.value=="---") and (len(datos)!=0):
            b= len(datos)
            a= b-5
            tabla_historial(a,b)
        elif len(datos)<=5 or n1.value=="1":
            warn("Tips","Ya estás en la primera página")
        else:  
            b= int(n1.value)-1
            a= b-5
            tabla_historial(a,b)

def percentil(): #Calcula el percentil que estás y muestra una gráfica relacionada.
    fhand= open("user_data.txt","r",encoding="utf-8")
    
    count= 0
    for line in fhand:
        if count==0:
            user= line.strip("\n")
        elif count==3:
            sexo= line.strip("\n")
        count += 1
    
    fhand.close()
    
    if leerRegistro()[user]!=[]:
    
        p1,p2,p3= calculoPercentiles(user,sexo)

        percentil1.value= "Percentil",p1
        percentil2.value= "Percentil",p2
        percentil3.value= "Percentil",p3
    
    else:
        error("ERROR","Aun no has realizado ningún salto")
        reset_contenido()

def pinta_grafica(): #Dibujar la gráfica de percentil.
    fhand= open("user_data.txt","r",encoding="utf-8")
    
    nombre= inputNombre()
    
    datos = datos_registro(leerRegistro(), nombre)
    datosRevisados = datos_correctos_estadisticas(datos[0], datos[1], datos[2])
    
    temp_file = grafica(datosRevisados[0], datosRevisados[1], datosRevisados[2], nombre)
    
def eliminar(): #Eliminar los archivos creados utilizando el programa.
    archivos= os.listdir()
    
    try:
        if 'user_data.txt' in archivos:
            eliminar_archivo('user_data.txt')
                
        if 'ranking.txt' in archivos:
            eliminar_archivo('ranking.txt')
            
        if 'temp_plot.png' in archivos:
            eliminar_archivo('temp_plot.png')
            
        if 'saltosAnteriores.json' in archivos:
            eliminar_archivo('saltosAnteriores.json')
            
    except:
        1
        
def main(boton): #Función principal para cambiar contenidos entre botones del menú.
    cambia_color(boton)
    cambia_titulo(boton)
    muestra_contenido(boton)


# Widgets ---------------------------------------------------------------------

#Parte de Opciones
opciones= Box(app,layout="grid",align="top",border=False,grid=[0,1])

border = Box(app,border=True,grid=[0,0],width=204,height=80)
border.bg= "#3F49CA"
text_opcion = Text(border, text="OPCIONES",size=20,color="white",width="fill",height="fill")

b1 = PushButton(opciones, text = "Iniciar sesión",grid=[0,1],width=16,height=2,command=lambda:main(b1))
b1.bg= "#42F2F7"
b1.text_size=15

b2 = PushButton(opciones, text = "Analizar el salto",grid=[0,2],width=16,height=2,command=lambda:main(b2))
b2.bg= "#42F2F7"
b2.text_size=15

b3 = PushButton(opciones, text = "Leaderboard",grid=[0,3],width=16,height=2,command=lambda:main(b3))
b3.bg= "#42F2F7"
b3.text_size=15

b4 = PushButton(opciones, text = "Historial de salto",grid=[0,4],width=16,height=2,command=lambda:main(b4))
b4.bg= "#42F2F7"
b4.text_size=15

b5 = PushButton(opciones, text = "Estadísticas",grid=[0,5],width=16,height=2,command=lambda:main(b5))
b5.bg= "#42F2F7"
b5.text_size=15


parte_principal= Box(app,layout="grid",align="top",border=False,grid=[1,1],width="fill",height="fill")


#Titulo de las opciones
border_titulo = Box(app,border=True,grid=[1,0],width=820,height=80)
border_titulo.bg= "#3F49CA"
titulo= Text(border_titulo, text="ELIGE UNA OPCIÓN",size=36,color="white",width="fill",height="fill")
titulo.font= "Impact"


#Iniciar sesión
ide_acceso= False

nombre_txt= Text(parte_principal,text="Nombre de cuenta",size=25,grid=[0,0],width=16,height=2,visible=False)
nombre_txt.font="Arial"
nombre= TextBox(parte_principal,grid=[0,1],width=29,visible=False)
nombre.text_size=25
nombre.bg="white"
nombre.font="Calibri"

psw_txt= Text(parte_principal,text="Contraseña",size=25,grid=[0,2],width=16,height=2,visible=False)
psw_txt.font="Arial"
psw= TextBox(parte_principal,grid=[0,3],width=29,visible=False,hide_text=True)
psw.text_size=25
psw.bg="white"
psw.font="Calibri"

psw_visible= CheckBox(parte_principal,grid=[0,4],text="Mostrar contraseña",height=2,visible=False,command=mostra_psw)
psw_visible.text_size=15

boton_iniciar= PushButton(parte_principal,grid=[0,5],text="Iniciar",width=10,visible=False,command=inicia_sesion)
boton_iniciar.text_size=20

#Información personal
ide_guardado= False

cuenta= Text(parte_principal,text="",size=28,grid=[0,0],width=16,height=2,visible=False)

box_perfil= Box(parte_principal,border=False,grid=[0,1],layout="grid",visible=False)

usuario_txt= Text(box_perfil,text="Nombre de usuario",size=20,grid=[0,0],width=16,height=2,visible=False)
usuario_txt.font="Arial"
usuario= TextBox(box_perfil,grid=[1,0],width=35,visible=False)
usuario.text_size=20
usuario.bg="white"
usuario.font="Calibri"

grupo_txt= Text(box_perfil,text="Grupo ProMu",size=20,grid=[0,1],width=12,height=2,align="right",visible=False)
grupo_txt.font="Arial"
grupo= TextBox(box_perfil,grid=[1,1],width=35,visible=False)
grupo.text_size=20
grupo.bg="white"
grupo.font="Calibri"

sexo_txt= Text(box_perfil,text="Sexo",size=20,grid=[0,2],width=6,height=2,align="right",visible=False)
sexo_txt.font="Arial"
sexo= Combo(box_perfil,grid=[1,2],width=12,visible=False,options=["Hombre","Mujer"],align="left")
sexo.text_size=20
sexo.bg="white"
sexo.font="Calibri"

text_informativo= Text(parte_principal,text="Tips:\nnecesitas completar tu perfil para enviar saltos y ver estadísticas.",size=15,grid=[0,3],height=2,visible=False)
text_informativo.text_color="red"

box_boton= Box(parte_principal,border=False,grid=[0,4],layout="grid",visible=False)
boton_guardar= PushButton(box_boton,grid=[0,0],text="Guardar",width=10,visible=False,command=guarda_datos)
boton_guardar.text_size=20
espacio_entre_boton= Text(box_boton,grid=[1,0],width=15,height=7,visible=False)
boton_cerrar= PushButton(box_boton,grid=[2,0],text="Cerrar sesión",width=10,visible=False,command=cerra_sesion)
boton_cerrar.text_size=20


#Analizar salto
ide_analizado= False
ide_enviado= False
sTotal= []

opciones= os.listdir()
opcion=[]
for fichero in opciones:
    if fichero[-5:]==".xlsx":
        opcion.append(fichero)

ruta= Combo(parte_principal,grid=[0,0],width=28,visible=False,options=opcion)
ruta.text_size=20
ruta.font="Calibri"

espacio_ruta= Text(parte_principal,grid=[1,0],width=6,height=6,visible=False)

peso_box= Box(parte_principal,border=False,grid=[0,1],layout="grid",visible=False)
peso_txt= Text(peso_box,text="Peso (kg) ",size=20,grid=[0,0],width=8,height=1,visible=False,align="left")
peso= TextBox(peso_box,grid=[1,0],width=21,visible=False)
peso.text_size=20
peso.bg="white"
peso.font="Calibri"

boton_analizar= PushButton(parte_principal,grid=[2,0,3,2],text="Analizar",width=13,height=2,visible=False,align="bottom",command=analizar)
boton_analizar.text_size=20

espacio_datos= Text(parte_principal,grid=[0,2],height=1,visible=False)

datos_box= Box(parte_principal,border=False,grid=[0,3,1,4],layout="grid",visible=False)

v_max= Text(datos_box,text="Velocidad máxima:",size=20,grid=[0,0],height=2,visible=False,align="right")
f_max= Text(datos_box,text="Fuerza máxima:",size=20,grid=[0,1],height=2,visible=False,align="right")
p_max= Text(datos_box,text="Potencia máxima:",size=20,grid=[0,2],height=2,visible=False,align="right")
a_max= Text(datos_box,text="Altura máxima:",size=20,grid=[0,3],height=2,visible=False,align="right")

v_sol= Text(datos_box,text="                 ",size=20,grid=[1,0],height=2,visible=False,align="left")
f_sol= Text(datos_box,text="                 ",size=20,grid=[1,1],height=2,visible=False,align="left")
p_sol= Text(datos_box,text="                 ",size=20,grid=[1,2],height=2,visible=False,align="left")
a_sol= Text(datos_box,text="                 ",size=20,grid=[1,3],height=2,visible=False,align="left")

boton_enviar= PushButton(parte_principal,grid=[2,3],text="Enviar",width=13,height=2,visible=False,command=enviar)
boton_enviar.text_size=20
boton_info= PushButton(parte_principal,grid=[2,4],text="Info extra",width=9,visible=False,align="bottom",command=info_extra)
boton_info.text_size=13

#Leaderboard
L_column1= Text(parte_principal,text="Rango",size=25,grid=[0,0],width=8,height=2,visible=False)
L_column2= Text(parte_principal,text="Nombre",size=25,grid=[1,0],width=8,height=2,visible=False)
L_column3= Text(parte_principal,text="Grupo",size=25,grid=[2,0],width=8,height=2,visible=False)
L_column4= Text(parte_principal,text="Altura",size=25,grid=[3,0],width=8,height=2,visible=False)
L_column5= Text(parte_principal,text="Fecha",size=25,grid=[4,0],width=8,height=2,visible=False)

#column1
L_r1= Text(parte_principal,text="",size=20,grid=[0,1],width=8,height=2,visible=False)
L_r2= Text(parte_principal,text="",size=20,grid=[0,2],width=8,height=2,visible=False)
L_r3= Text(parte_principal,text="",size=20,grid=[0,3],width=8,height=2,visible=False)
L_r4=  Text(parte_principal,text="",size=20,grid=[0,4],width=8,height=2,visible=False)
L_r5=  Text(parte_principal,text="",size=20,grid=[0,5],width=8,height=2,visible=False)
#column2
L_n1= Text(parte_principal,text="",size=20,grid=[1,1],width=8,height=2,visible=False)
L_n2= Text(parte_principal,text="",size=20,grid=[1,2],width=8,height=2,visible=False)
L_n3= Text(parte_principal,text="",size=20,grid=[1,3],width=8,height=2,visible=False)
L_n4= Text(parte_principal,text="",size=20,grid=[1,4],width=8,height=2,visible=False)
L_n5= Text(parte_principal,text="",size=20,grid=[1,5],width=8,height=2,visible=False)
#column3
L_g1= Text(parte_principal,text="",size=20,grid=[2,1],width=8,height=2,visible=False)
L_g2= Text(parte_principal,text="",size=20,grid=[2,2],width=8,height=2,visible=False)
L_g3= Text(parte_principal,text="",size=20,grid=[2,3],width=8,height=2,visible=False)
L_g4= Text(parte_principal,text="",size=20,grid=[2,4],width=8,height=2,visible=False)
L_g5= Text(parte_principal,text="",size=20,grid=[2,5],width=8,height=2,visible=False)
#column4
L_a1= Text(parte_principal,text="",size=20,grid=[3,1],width=8,height=2,visible=False)
L_a2= Text(parte_principal,text="",size=20,grid=[3,2],width=8,height=2,visible=False)
L_a3= Text(parte_principal,text="",size=20,grid=[3,3],width=8,height=2,visible=False)
L_a4= Text(parte_principal,text="",size=20,grid=[3,4],width=8,height=2,visible=False)
L_a5= Text(parte_principal,text="",size=20,grid=[3,5],width=8,height=2,visible=False)
#column5
L_f1= Text(parte_principal,text="",size=20,grid=[4,1],width=8,height=2,visible=False)
L_f2= Text(parte_principal,text="",size=20,grid=[4,2],width=8,height=2,visible=False)
L_f3= Text(parte_principal,text="",size=20,grid=[4,3],width=8,height=2,visible=False)
L_f4= Text(parte_principal,text="",size=20,grid=[4,4],width=8,height=2,visible=False)
L_f5= Text(parte_principal,text="",size=20,grid=[4,5],width=8,height=2,visible=False)
#columnExtra
L_cambia_box= Box(parte_principal,border=False,grid=[2,6],layout="grid",visible=False)
L_anterior= PushButton(L_cambia_box,text="<",grid=[0,0],visible=False,command=lambda:L_cambia_pagina(L_anterior))
L_siguiente= PushButton(L_cambia_box,text=">",grid=[1,0],visible=False,command=lambda:L_cambia_pagina(L_siguiente))


#Historial de salto
column1= Text(parte_principal,text="Nº salto",size=25,grid=[0,0],width=10,height=2,visible=False)
column2= Text(parte_principal,text="Altura",size=25,grid=[1,0],width=10,height=2,visible=False)
column3= Text(parte_principal,text="Fecha",size=25,grid=[2,0],width=10,height=2,visible=False)
borrar= PushButton(parte_principal,grid=[3,0],text="Borrar Historial",visible=False,command=lambda:borra_salto(borrar))
borrar.text_size=15
borrar.bg="red"

#column1
n1= Text(parte_principal,text="",size=20,grid=[0,1],width=10,height=2,visible=False)
n2= Text(parte_principal,text="",size=20,grid=[0,2],width=10,height=2,visible=False)
n3= Text(parte_principal,text="",size=20,grid=[0,3],width=10,height=2,visible=False)
n4=  Text(parte_principal,text="",size=20,grid=[0,4],width=10,height=2,visible=False)
n5=  Text(parte_principal,text="",size=20,grid=[0,5],width=10,height=2,visible=False)
#column2
a1= Text(parte_principal,text="",size=20,grid=[1,1],width=10,height=2,visible=False)
a2= Text(parte_principal,text="",size=20,grid=[1,2],width=10,height=2,visible=False)
a3= Text(parte_principal,text="",size=20,grid=[1,3],width=10,height=2,visible=False)
a4=  Text(parte_principal,text="",size=20,grid=[1,4],width=10,height=2,visible=False)
a5=  Text(parte_principal,text="",size=20,grid=[1,5],width=10,height=2,visible=False)
#column3
f1= Text(parte_principal,text="",size=20,grid=[2,1],width=10,height=2,visible=False)
f2= Text(parte_principal,text="",size=20,grid=[2,2],width=10,height=2,visible=False)
f3= Text(parte_principal,text="",size=20,grid=[2,3],width=10,height=2,visible=False)
f4=  Text(parte_principal,text="",size=20,grid=[2,4],width=10,height=2,visible=False)
f5=  Text(parte_principal,text="",size=20,grid=[2,5],width=10,height=2,visible=False)
#column4
x1= PushButton(parte_principal,grid=[3,1],text="x",visible=False,command=lambda:borra_salto(x1))
x2= PushButton(parte_principal,grid=[3,2],text="x",visible=False,command=lambda:borra_salto(x2))
x3= PushButton(parte_principal,grid=[3,3],text="x",visible=False,command=lambda:borra_salto(x3))
x4= PushButton(parte_principal,grid=[3,4],text="x",visible=False,command=lambda:borra_salto(x4))
x5= PushButton(parte_principal,grid=[3,5],text="x",visible=False,command=lambda:borra_salto(x5))
x1.text_size=10
x2.text_size=10
x3.text_size=10
x4.text_size=10
x5.text_size=10
x1.bg="red"
x2.bg="red"
x3.bg="red"
x4.bg="red"
x5.bg="red"
#columnExtra
cambia_box= Box(parte_principal,border=False,grid=[3,6],layout="grid",visible=False)
anterior= PushButton(cambia_box,text="<",grid=[0,0],visible=False,command=lambda:cambia_pagina(anterior))
siguiente= PushButton(cambia_box,text=">",grid=[1,0],visible=False,command=lambda:cambia_pagina(siguiente))


#Estadísticas
txt_altura= Text(parte_principal,text="Altura Media",size=25,grid=[0,0],width=10,height=1,visible=False,align="right")
txt_potencia= Text(parte_principal,text="Potencia Media",size=25,grid=[0,1],width=12,height=1,visible=False,align="right")
txt_fuerza= Text(parte_principal,text="Fuerza Media",size=25,grid=[0,2],width=11,height=1,visible=False,align="right")

flecha1= Text(parte_principal,text="===》",size=25,grid=[1,0],width=12,height=1,visible=False)
flecha2= Text(parte_principal,text="===》",size=25,grid=[1,1],width=12,height=1,visible=False)
flecha3= Text(parte_principal,text="===》",size=25,grid=[1,2],width=12,height=1,visible=False)

percentil1= Text(parte_principal,text="",size=25,grid=[2,0],width=12,height=1,visible=False)
percentil2= Text(parte_principal,text="",size=25,grid=[2,1],width=12,height=1,visible=False)
percentil3= Text(parte_principal,text="",size=25,grid=[2,2],width=12,height=1,visible=False)

grafica_estadistica= Picture(parte_principal,grid=[0,3,3,3],visible=False,width=420,height=315)

# Display ---------------------------------------------------------------------
app.display()

#Salir
app.when_closed= salir()
app.when_closed= eliminar()