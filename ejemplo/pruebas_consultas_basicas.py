import pyodbc
import pandas as pd


#Conexión a Nacional
cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=nserposad;PWD=atzuke24', autocommit=True )
#Querys
sql_credito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = 20230321"
sql_debito = "SELECT * FROM CISLIBPR.ACREALCEDB WHERE FECNOV = 20230321"
sql_plantas = "SELECT * FROM CISLIBPR.SUCURSALES"
sql_sucursales_cerradas = "SELECT * FROM CISLIBPR.SUCURSALESCERRADAS"
sql_tarjetas_credito = "select CODIGOINVENTARIO, CLASETARJETA, NOMBRE from cislibpr.CODIGOSINVENTARIO where tipotarjeta = 'CREDITO'"
sql_tarjetas_debito = "select CODIGOINVENTARIO, CLASETARJETA, NOMBRE from cislibpr.CODIGOSINVENTARIO where tipotarjeta = 'DEBITO'"
sql_codigo_clase_credito = "select CODIGOINVENTARIO, CLASETARJETA, NOMBRE from cislibpr.CODIGOSINVENTARIO where tipotarjeta = 'CREDITO'"
sql_codigo_clase_debito = "select CODIGOINVENTARIO, CLASETARJETA, NOMBRE from cislibpr.CODIGOSINVENTARIO where tipotarjeta = 'DEBITO'"
#creamos los 6 dataframes principales
df_alimentacion_credito_sucio = pd.read_sql(sql_credito,con = cnx_nac) # type: ignore
df_alimentacion_debito_sucio = pd.read_sql(sql_debito,con = cnx_nac) # type: ignore
df_plantas = pd.read_sql(sql_plantas,con = cnx_nac) # type: ignore
df_sucursales_cerradas = pd.read_sql(sql_sucursales_cerradas,con = cnx_nac) # type: ignore
df_tarjetas_credito = pd.read_sql(sql_tarjetas_credito,con = cnx_nac) # type: ignore
df_tarjetas_debito = pd.read_sql(sql_tarjetas_debito,con = cnx_nac) # type: ignore
#Creamos una lista con las clases de tarjeta para identificar si son CREDITO o DEBITO
lista_credito = df_tarjetas_credito.CLASETARJETA.to_list()
lista_debito = df_tarjetas_debito.CLASETARJETA.to_list()
#Con las listas creamos filtros para eliminar de cada dataframe
#(credito y debito) lo que no es correspondiente
filter_credito = df_alimentacion_credito_sucio.CLSTRJ.isin(lista_credito)
filter_debito = df_alimentacion_debito_sucio.CLSTRJ.isin(lista_debito)
df_alimentacion_credito = df_alimentacion_credito_sucio[filter_credito]
df_alimentacion_debito = df_alimentacion_debito_sucio[filter_debito]
#Separamos todos los registros basados en los operadores
#THALES
filter_credito_thales = df_alimentacion_credito.DSCFBR.isin(["THALES              ","THALES.             "])
filter_debito_thales = df_alimentacion_debito.DSCFBR.isin(["THALES              ","THALES.             "])
df_credito_thales = df_alimentacion_credito[filter_credito_thales]
df_debito_thales = df_alimentacion_debito[filter_debito_thales]
#IDEMIA
filter_credito_idemia = df_alimentacion_credito.DSCFBR.isin(["IDEMIA              ","IDEMIA.             "])
filter_debito_idemia = df_alimentacion_debito.DSCFBR.isin(["IDEMIA              ","IDEMIA.             "])
df_credito_idemia = df_alimentacion_credito[filter_credito_idemia]
df_debito_idemia = df_alimentacion_debito[filter_debito_idemia]

#Cambiamos el nombre de una columna en debito que no concuerda
df_debito_thales.rename(columns={"OFICINA": "OFICLI"}, inplace= True)
df_debito_idemia.rename(columns={"OFICINA": "OFICLI"}, inplace= True)
#Unimos credito y debito de cada operador
df_thales = pd.concat([df_credito_thales, df_debito_thales], ignore_index = True)
df_idemia = pd.concat([df_credito_idemia, df_debito_idemia],  ignore_index = True)
#Verificamos que la sucursal esté actualizada, sino, la remplazamos
for index, row in df_idemia.iterrows():
    if df_sucursales_cerradas.CODIGOOFICINA.isin([row["OFICLI"]]).any():
          for index, row2 in df_sucursales_cerradas.iterrows():
               if row2["CODIGOOFICINA"] == row["OFICLI"]:
                    if row2["CODIGORECEPTOR"] != -2147483648:
                         df_idemia.OFICLI.replace({row["OFICLI"] : row2["CODIGORECEPTOR"]}, inplace = True)
for index, row in df_thales.iterrows():
    if df_sucursales_cerradas.CODIGOOFICINA.isin([row["OFICLI"]]).any():
          for index, row2 in df_sucursales_cerradas.iterrows():
               if row2["CODIGOOFICINA"] == row["OFICLI"]:
                    if row2["CODIGORECEPTOR"] != -2147483648:
                         df_thales.OFICLI.replace({row["OFICLI"] : row2["CODIGORECEPTOR"]}, inplace = True)
#Agregamos plantas a cada registro según nuestra tabla de plantas por sucursales.
df_thales_completo = pd.merge(df_thales, df_plantas, left_on="OFICLI", right_on="CODIGOOFICINA", how = "left")
df_idemia_completo = pd.merge(df_idemia, df_plantas, left_on="OFICLI", right_on="CODIGOOFICINA", how = "left")




print(lista_debito)
print(df_alimentacion_debito_sucio)
print(df_alimentacion_debito)
print(lista_credito)
print(df_alimentacion_credito_sucio)
print(df_alimentacion_credito)


