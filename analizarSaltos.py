#FISICA PROMU

#Librerias----------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz
from scipy.ndimage import gaussian_filter1d as gf

#Fichero-------------------------------------------------------------------------------------------
fichero = "muestras_2.xlsx"                                                       #Seleccionar un fichero

df = pd.read_excel(fichero)                                                       #Guardar contenido del fichero en una variable

#Funciones de cálculo para gráfica------------------------------------------------------------------------------
def datos(df):                                                                    #Función que extrae datos del fichero y los guarda en variables
    tiempo = df.values[:,0].astype(float)                                         #Guardar datos de tiempo
    aceleracion_abs = df.values[:,1].astype(float)                                #Guardar datos de aceleracion abs
    aceleracion_y = df.values[:,3].astype(float)                                  #Guardar datos de aceleracion en eje y

    #Se le resta la gravedad
    aceleracion = (aceleracion_abs * np.sign(aceleracion_y))-9.7                  #Calcular aceleracion normal
    
    return tiempo, aceleracion


tiempo = datos(df)[0]
aceleracion = datos(df)[1]


# Funcion Primitiva Numerica utilizando Trapecios
def primitivaNumerica(variable, tiempo, y0=0):                                    #Función que integra
    return cumtrapz(variable,x=tiempo,initial=y0)


velocidad = primitivaNumerica(aceleracion, tiempo, y0=0)


# Variables necesarias para el "step detection"
diferencias = np.diff(aceleracion)
coef = 2
dispersion = coef*diferencias.std()

#Funcion que suaviza la Aceleracion y la Velocidad
def suavizar_funciones(aceleracion, velocidad):                                   #Función que suaviza la aceleracion y la velocidad mediante el filtro de Gauss
    ac_gauss = gf(aceleracion,dispersion)
    vl_gauss = primitivaNumerica(ac_gauss, tiempo)
    return ac_gauss, vl_gauss

ac_gauss, vl_gauss = suavizar_funciones (aceleracion, velocidad)
 
#Funcion para ajustar el inicio del salto
def normalizar_velocidad_inicio(velocidad, tiempo, tiempo_max):                    #Función que arregla el inicio para que el reposo sea 0
    nueva_velocidad = []
    for i,(v,t) in enumerate(zip(velocidad, tiempo)):                              #Recorre velocidad y tiempo y guarda el valor en v y t además del índice de cada uno como i
        if t < tiempo_max:
            nueva_velocidad.append(0)                                              #Si el tiempo es menor al deseado la velocidad es 0
        else:
            nueva_velocidad.append(v)                                              #Si el tiempo es mayor al deseado la velocidad es la misma           
    return nueva_velocidad
            
            
vl_gauss = normalizar_velocidad_inicio(vl_gauss, tiempo, 0.8)

#Funcion para ajustar el final del salto
def normalizar_velocidad_final(velocidad, tiempo, tiempo_max):                     #Función que arregla el final para que el reposo sea 0
    nueva_velocidad = []
    for i,(v,t) in enumerate(zip(velocidad, tiempo)):
        if t > tiempo_max:
            nueva_velocidad.append(0)                                              #Si el tiempo es mayor al deseado la velocidad es 0
        else:
            nueva_velocidad.append(v)                                              #Si el tiempo es menor al deseado la velocidad es la misma          
    return nueva_velocidad

vl_gauss = normalizar_velocidad_final(vl_gauss, tiempo, 3.64)

#Funcion sacar el punto maximo y minimo de la grafica
def maximo_minimo(vl_gauss):                                                       #Función que devuelve los valores máximo y mínimo de la velocidad
    return np.argmax(vl_gauss), np.argmin(vl_gauss)
    
    
maximo, minimo = maximo_minimo(vl_gauss)

#Funcion sacar el punto en el que se incia el salto
def inicio_salto(vl_gauss):                                                        #Función que devuelve el punto donde se inicia el salto
    for val in vl_gauss:
        if val<0:                                                                  #Si la velocidad empieza a distanciarse de 0, esta comenzando el salto
            S = val
            indice = list(vl_gauss).index(val)
            break
    return indice

indice = inicio_salto(vl_gauss)

#Funciones de representación gráfica---------------------------------------------------------------

def graficas_originales(tiempo, aceleracion, velocidad):                            #Función de representación de las gráficas originales
    plt.figure()
    plt.subplot(211)                                                    
    plt.plot(tiempo,aceleracion,label="Aceleración Original")                       #Representar la ACELERACIÓN
    plt.title("Datos de salto originales")
    plt.ylabel("Aceleracion")
    plt.legend()
    plt.grid()

    plt.subplot(212)
    plt.plot(tiempo,velocidad,label="Velocidad Original",color="g")                 #Representar la VELOCIDAD
    plt.xlabel("Tiempo")
    plt.ylabel("Velocidad")
    plt.legend()
    plt.grid()
   

def graficas_suavizadas(tiempo, ac_gauss, vl_gauss, indice, maximo, minimo):        #Funcion representacion de la gráficas suavizadas
    plt.figure()
    plt.subplot(211)
    plt.plot(tiempo,ac_gauss,label="Aceleración Suavizada con Gauss")               #Representar la ACELERACION con Gauss
    plt.title("Salto (Aceleración y Velocidad)")
    plt.ylabel("Aceleración (m/s^2)")
    plt.legend()
    plt.grid()

    plt.subplot(212)
    plt.plot(tiempo, vl_gauss, "r")                                                 #Representar la VELOCIDAD modificada y filtrada con Gauss más sus valores máximo y mínimo
    plt.plot(tiempo[indice], vl_gauss[indice], "x", label="Inicio salto", color="Green")
    plt.plot(tiempo[maximo], vl_gauss[maximo], "x", label="Despegue", color="Black")
    plt.plot(tiempo[minimo], vl_gauss[minimo], "x", label="Aterrizaje", color="Blue")  
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Velocidad (m/s)')
    plt.legend()
    plt.grid()
    plt.show()


#Funciones de calculo fuerza, potencia y altura ---------------------------------------------------------------
def fuerza(ac_gauss, tiempo):                                                       #Función que calcula la fuerza realizada en el salto
    try:
        masa = int(input("Cual es tu masa: "))                                      #Se pide la masa del usuario para calcular la fuerza
        fuerza = masa * ac_gauss                                                    #Cálculo de la fuerza con fórmula
        
        maximo = np.argmax(fuerza)                                                  #Se calcula el valor máximo de la fuerza
        minimo = np.argmin(fuerza)                                                  #Se calcula el valor mínimo de la fuerza
        
        #Representar la ACELERACION Gauss
        plt.figure()
        plt.plot(tiempo,fuerza,label="Fuerza (N)")                                 #Representar toda la fuerza en función del tiempo más los valores máximo y mínimo
        plt.title("Fuerza")
        plt.plot(tiempo[maximo], fuerza[maximo], "x", label="Fuerza máxima", color="Black")
        plt.plot(tiempo[minimo], fuerza[minimo], "x", label="Fuerza minima", color="Blue")
        plt.xlabel("Tiempo")
        plt.ylabel("Fuerza")
        plt.legend()
        plt.grid()
        plt.show()
        
        fuerza_maxima = fuerza[maximo]
        print(f"La fuerza maxima es: {fuerza_maxima:.2f} N")    
        
    except ValueError:
        print("Error: Introduce un valor válido")                                  #Si introduce un valor erróneo de masa da error
    return fuerza, fuerza[maximo], fuerza[minimo]                                  #Devuelve el array de fuerza y el valor máximo y mínimo de la fuerza


def potencia(fuerza, vl_gauss, tiempo):                                            #Función que calcula la potencia realizada en el salto
 
    potencia = fuerza * vl_gauss                                                   #Cálculo de la potencia con fórmula 
        
    maximo = np.argmax(potencia)                                                   #Obtener el valor máximo de potencia 
        
    #Representar la ACELERACION Gauss
    plt.figure()
    plt.plot(tiempo, potencia, label="Potencia")                                   #Representar toda la potencia en función del tiempo más los valores máximos y mínimos
    plt.title("Potencia(t)")
    plt.plot(tiempo[maximo], potencia[maximo], "x", label="Potencia máxima", color="Black")
    plt.xlabel("Tiempo")
    plt.ylabel("Potencia")
    plt.legend()
    plt.grid()
    plt.show()
    
    potencia_maxima = potencia[maximo]
    print(f"La potencia maxima es: {potencia_maxima:.2f} W")
    
    return potencia[maximo]                                                        #Devuelve válor máximo de la potencia


def altura(vl_gauss, tiempo):                                                      #Función que calcula la altura máxima alcanzada en el salto
    g = 9.8                                                                        #Variable de gravedad necesario
    velocidad = np.array(vl_gauss)                                                 
    altura = (velocidad**2)/(2*g)*1000                                             #Calculo de la altura mediante fórmula (en milimetros)
        
    maximo = np.argmax(altura)                                                     #Valor de la altura máxima alcanzada
         
    #Representar la ACELERACION Gauss
    plt.figure()
    plt.plot(tiempo, altura, label="Altura")                                       #Representacion de la altura en funcion del tiempo más el valor máximo de la altura

    plt.title("Altura(t)")
    plt.plot(tiempo[maximo], altura[maximo], "x", label="Altura máxima", color="Black")
    plt.xlabel("Tiempo")
    plt.ylabel("Altura")
    plt.legend()
    plt.grid()
    plt.show()
    
    altura_maxima = int(altura[maximo])                                            #Queremos el valor entero calculado de la altura máxima
    print(f"La altura maxima es: {altura_maxima} milimetros")
    
    return altura[maximo]


##Funcion de datos para la interfaz--------------------------------------------------------------
def main_analizar(fichero,masa):                                                   #Función que recoge todos los datos importantes calculados para facilitar la interfaz
    #Variable necesaria para analizar
    df = pd.read_excel(fichero)
    
    tiempo = datos(df)[0]
    aceleracion = datos(df)[1]
    velocidad = primitivaNumerica(aceleracion, tiempo, y0=0)
    
    diferencias = np.diff(aceleracion)
    coef = 2
    dispersion = coef*diferencias.std()
    
    ac_gauss, vl_gauss = suavizar_funciones (aceleracion, velocidad)
    vl_gauss = normalizar_velocidad_inicio(vl_gauss, tiempo, 0.8)
    vl_gauss = normalizar_velocidad_final(vl_gauss, tiempo, 3.64)
    
    maximo_vl, minimo_vl = maximo_minimo(vl_gauss)
    indice = inicio_salto(vl_gauss)
    
    fuerza = masa * ac_gauss
    potencia = fuerza * vl_gauss
        
    maximo_f = np.argmax(fuerza)
    maximo_p = np.argmax(potencia)
    
    g = 9.8
    velocidad_array = np.array(vl_gauss)
    altura = (velocidad_array**2)/(2*g)*1000 
        
    maximo_a = np.argmax(altura)
    
    #Datos analizados
    velocidad_maxima = "{:.2f}".format(vl_gauss[maximo_vl])

    fuerza_maxima = "{:.2f}".format(fuerza[maximo_f])

    potencia_maxima = "{:.2f}".format(potencia[maximo_p])
    
    altura_maxima = "{:.2f}".format(int(altura[maximo_a]))

    #Gráfica de velocidad
    graficas_suavizadas(tiempo, ac_gauss, vl_gauss, indice, maximo_vl, minimo_vl)

    return velocidad_maxima,fuerza_maxima,potencia_maxima,altura_maxima

#Funciones iniciadora del programa---------------------------------------------------------------
def main():                                                                     #Funciones main que ejecuta el programa y llama a las demás funciones
    graficas_originales(tiempo, aceleracion, velocidad)
    graficas_suavizadas(tiempo, ac_gauss, vl_gauss, indice, maximo, minimo)
    Fuerza, fuerza_max, fuerza_min = fuerza(ac_gauss, tiempo)
    potencia(Fuerza, vl_gauss, tiempo)
    altura(vl_gauss, tiempo)


if __name__=="__main__":
    main()

