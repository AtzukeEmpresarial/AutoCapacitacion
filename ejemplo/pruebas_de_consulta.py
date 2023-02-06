import pyodbc
import pandas as pd
import sys
from os import makedirs, path 


try:
    cnx_nac = pyodbc.connect('DSN=QDSN_MEDELLINET01;UID=MSERPOSAD;PWD=Q9XLH6KM', autocommit=True )
    print("conexión exitosa")
except pyodbc.InterfaceError:
    print("usuario y/o contraseña no validos")
    sys.exit()
sql_prueba = f'''SELECT OFICINA FROM MATLIBRAMD.MATFFGNPLA '''
query1 = pd.read_sql(sql_prueba,cnx_nac)

save_path = 'salidas/'    
if not path.isdir(save_path):
    print(f'La ruta {save_path} no existe, se creará en esta carpeta...')
    makedirs(save_path)
    query1.to_csv(save_path + 'Ohsy.csv',index=False,)

print('El archivo ha sido guardado en la ruta ' + save_path + '.csv')

print(query1)