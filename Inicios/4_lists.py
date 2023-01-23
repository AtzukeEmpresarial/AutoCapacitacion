#listas
my_list = list()
my_list2 = []

print(len(my_list))

my_list = [13,"hola",45,56,"haaaa"]
print(my_list)

print(type(my_list))

#podemos ir a las posiciones de las listas desde adelante como hacia atras
print(my_list[1])
print(my_list[-1])
print(my_list[-3])

#algunos metodos
print(my_list.count("hola")) #cuenta el numero de elementos que coincidan
my_list.append("nooo") #insertar al final
my_list.insert(0,"sii")
print(my_list)
my_list.remove("sii") #Elimina el valor que coincida, no elimina todos
print(my_list)
my_list.pop() #Elimina el ultimo valor o en el indice que le indiquemos y nos lo retorna.
print(my_list)
del my_list[2] #Elimina el valor en el indice que le indicamos y no lo retorna.
print(my_list)

#se pueden crear variables con el contenido de una lista, necesita el mismo numero de variables que elementos de la lista.
numero1, saludo, numero3, grito = my_list
print(numero1)

#se pueden sumar listas
my_list2 = [1,2,3,4,5,6,"hola"]
print(my_list + my_list2)

#podemos copiar y limpiarlas listas
my_list3 = my_list.copy()
my_list.clear()
print(my_list)
print(my_list3)

#como tambien podemos voltearla y ordenarla
my_list3.reverse()
print(my_list3)
my_list3.sort()
#print(my_list3) #ordena peor no puede ornedar si hay mezclados int y sting
