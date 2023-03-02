import pyodbc
import pandas as pd
import sys
from os import makedirs, path 


try:
    cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=NSERPOSAD;PWD=ATZUKE23', autocommit=True )
    print("conexión exitosa")
except pyodbc.InterfaceError:
    print("usuario y/o contraseña no validos")
    sys.exit()
sql_prueba = f'''INSERT INTO CISLIBPR.TIPOESTADOS (NOMBRE, DESCRIPCION) VALUES ('Primero', 'Este es el primer registro') '''
query1 = pd.read_sql(sql_prueba,cnx_nac)# type: ignore
'''save_path = 'salidas/'    
if not path.isdir(save_path):
    print(f'La ruta {save_path} no existe, se creará en esta carpeta...')
    makedirs(save_path)
query1.to_csv(save_path + 'registros.csv',index=False)

print(query1)
print('El archivo ha sido guardado en la ruta ' + save_path + '.csv')'''
