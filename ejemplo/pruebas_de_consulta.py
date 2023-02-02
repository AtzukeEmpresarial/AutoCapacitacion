import pyodbc
import pandas as pd
import sys
try:
    cnx_nac = pyodbc.connect('DSN=QDSN_MEDELLINET01;UID=MSERPOSAD;PWD=Q9XLH6KM', autocommit=True )
    print("conexión exitosa")
except pyodbc.InterfaceError:
    print("usuario y/o contraseña no validos")
    sys.exit()
sql_prueba = f'''SELECT CMNAMK FROM CMARK '''
query1 = pd.read_sql(sql_prueba,cnx_nac)