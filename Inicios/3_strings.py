#tipos de string y metodos para manejarlos.

my_string = "Hola"
my_string_v2 = "Hola v2"

print(len(my_string))
print(len(my_string_v2))

print(my_string + " " + my_string_v2) #concatenación simple
print(my_string + " mi nombre es\n" + my_string_v2) #salto de linea
print("\tmi nombre es " + my_string_v2) #tabulación
print("\tmi nombre es\n " + my_string_v2) #tabulación y escape con salto de linea
print("\\t mi nombre es\\n " + my_string_v2) #obviamos los comandos

#formateo
name, surname, age = "sergio", "posada",25
print("Hola mi nombre es {} {} y mi edad es {} y estoy aplicando el .format".format(name, surname,age)) #se llama al objeto
print("Hola mi nombre es %s %s y mi edad es %d y estoy aplicanto el porcentaje" %(name, surname,age)) #aquí aseguramos que entre un determinado tipo de formato, más seguro.
print(f"Hola mi nombre es {name} {surname} y mi edad es {age} y estoy aplicando inferencia de datos") #inferencia de datos, la mejor.

#desempaquetado de caracteres
languaje = "python"
a,b,c,d,e,f =languaje
print(a + b + c + "\n" + d + e + f)

#división de caracteres
languaje_slice = languaje[1:3] #toma desde el caracter 1 y finaliza en el 3 (sin tomar el 3)
print(languaje_slice)
languaje_slice2 = languaje[1:] #toma desde el caracter 1 hasta finalizar la cadena.
print(languaje_slice2)
print(languaje[-2]) #toma de atras a adelante.
languaje_slice = languaje[0:6:2] #toma desde el caracter 0 y finaliza en el 6 saltando cada 2
print(languaje_slice)

#Reversed
reversed_languaje = languaje[::-1] #invierte la cadena de texto
print(reversed_languaje)

#algunas funciones (pasar el mouse sobre la función para conocer que hace)
print(languaje.capitalize())
print(languaje.upper())
print(languaje.count("t"))
print(languaje.isnumeric())
print(languaje.lower())
print(languaje.upper().isupper())
print(languaje.startswith("py"))