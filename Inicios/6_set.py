my_set = set()
my_set2= {} #inicialmente es un diccionario

print(type(my_set))
print(type(my_set2))

my_set2 = {"Sergio", "Andres", 25} #al rellenarlo así, sí es un set.
print(type(my_set2))
print(my_set2) #un set no es una estructura ordenada
my_set2.add("Atzuke")
my_set2.add("Atzuke")
print(my_set2) #un set no repite elementos

print("Sergio" in my_set2)
print("Andre" in my_set2) #esta es la sintaxis para realizar busquedad en listas, tuplas y sets.

my_set.add("Esto")

print(my_set.union(my_set2)) #union une dos conjuntos... existen todas las operaciones de conjuntos.
