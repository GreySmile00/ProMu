# Función para que cualquier persona pueda entender a qué equivalen
# los watts de potencia generados por el salto de una persona.
def extra_stats(p):
    caballos = p*1/735.499                          # Conversión de watts a caballos de fuerza/vapor
    bombilla_inc = p/60                             # Conversión de watts a bombilla incandescente
    bombilla_led_rango = (p/10, p/6)                # Conversión de watts a bombilla LED
    
    res= caballos,bombilla_inc,bombilla_led_rango
    
    a=("La potencia obtenida del salto ({0} watts) equivale a {1:.0f} caballos de fuerza".format(p,res[0]))
    b=("Además, se podrían enceder {0:.0f} bombillas incandescentes de 60 vatios y entre {1:.0f} y {2:.0f} bombillas LED de entre 6 y 10 vatios.".format(res[1],res[2][0],res[2][1]))
    
    return a,b

