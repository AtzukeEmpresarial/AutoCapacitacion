import pyodbc
import pandas as pd
import sys
from os import makedirs

#Tomamos el excel con los datos
df_excel = pd.read_excel("Codigos.xlsx",sheet_name="Hoja1")
#Conexión a Nacional
cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=nserposad;PWD=atzuke24', autocommit=True )
cursor = cnx_nac.cursor()
for index, row in df_excel.iterrows():
    cursor.execute("INSERT INTO CISLIBPR.CODIGOSINVENTARIO (CODIGOINVENTARIO,TIPOTARJETA,CLASETARJETA,NOMBRE,PROVEEDOR) VALUES(?,?,?,?,?)", row.CODIGOINVENTARIO,row.TIPOTARJETA,row.CLASETARJETA,row.NOMBRE,row.PROVEEDOR)
cursor.commit()
cursor.close()
cnx_nac.close()
print(df_excel)