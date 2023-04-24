import pyodbc
import pandas as pd
import sys
from os import makedirs

#Tomamos el excel con los datos
df_excel = pd.read_excel("Plantas.xlsx",sheet_name="nombre")
#Conexión a Nacional
cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=nserposad;PWD=atzuke24', autocommit=True )
cursor = cnx_nac.cursor()
for index, row in df_excel.iterrows():
    cursor.execute("INSERT INTO CISLIBPR.PLANTAS (UBICACION,DESCRIPCION,OPERADOR,ACTIVA, PRODUCCION) VALUES('{}','{}','{}',{},{})".format(row["UBICACION"], row["DESCRIPCION"], row["OPERADOR"], int(row["ACTIVA"]), int(row["PRODUCCION"])))
cursor.commit()
cursor.close()
cnx_nac.close()
print(df_excel)