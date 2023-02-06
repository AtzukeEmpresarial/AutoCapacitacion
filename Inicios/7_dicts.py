#diccionarios

my_dict = dict()
my_dict2= {}

print(type(my_dict))
print(type(my_dict2))

my_dict2 = {"Nombre":"Sergio", "Apellido":"Posada", "edad":25}
print(my_dict2["Nombre"]) #En el diccionario podemos definir la clave para cada dato.

my_dict3 = {
    "Nombre":"Sergio", 
    "Apellido":"Posada", 
    "edad":25,
    "Lenguajes": {"python", "Swift", "kotlin"},
    1:1.87
    } 
print(my_dict3)

print("Sergio" in my_dict3)
print("Nombre" in my_dict3) #esta comprobaciçon va por la clave, no por el elemento.
