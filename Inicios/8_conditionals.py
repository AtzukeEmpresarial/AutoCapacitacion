#Condicionales
#Es el if de toda la vida... unos ejemplitos de la sintaxis

un_true = 1

if un_true == 1:
    print("En efecto, es 1")
elif un_true == 2:
    print("Cuidado, es 2")
else:
    print("hay pa', no es ninguno")

texto_vacio = "" #se entiende entonces que el valor booleano de un texto vacio es F
if texto_vacio:
    print("cucho, ese texto está llenito")
if not texto_vacio:
    print("cucho, ese texto está vacio") #Así se hace la negación
    