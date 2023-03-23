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
sql_tarjetas = "select CODIGOINVENTARIO, CLASETARJETA, NOMBRE from cislibpr.CODIGOSINVENTARIO"
#creamos los 6 dataframes principales
df_alimentacion_credito_sucio = pd.read_sql(sql_credito,con = cnx_nac) # type: ignore
df_alimentacion_debito_sucio = pd.read_sql(sql_debito,con = cnx_nac) # type: ignore
df_plantas = pd.read_sql(sql_plantas,con = cnx_nac) # type: ignore
df_sucursales_cerradas = pd.read_sql(sql_sucursales_cerradas,con = cnx_nac) # type: ignore
df_tarjetas_credito = pd.read_sql(sql_tarjetas_credito,con = cnx_nac) # type: ignore
df_tarjetas_debito = pd.read_sql(sql_tarjetas_debito,con = cnx_nac) # type: ignore
df_tarjetas = pd.read_sql(sql_tarjetas,con = cnx_nac) # type: ignore
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
#Agregamos el codigo de inventario
lista_thales_codinv = []
lista_idemia_codinv = []
lista_thales_name = []
lista_idemia_name = []
for index, row in df_thales_completo.iterrows():
     if df_tarjetas.CLASETARJETA.isin([row["CLSTRJ"]]).any():
          for index, row2 in df_tarjetas.iterrows():
               if row2["CLASETARJETA"] == row["CLSTRJ"]:
                    lista_thales_codinv.append(row2["CODIGOINVENTARIO"])
                    lista_thales_name.append(row2["NOMBRE"])
                    break 
df_thales_completo["CODINV"] = lista_thales_codinv
df_thales_completo["NOMBRE"] = lista_thales_name
for index, row in df_idemia_completo.iterrows():
     if df_tarjetas.CLASETARJETA.isin([row["CLSTRJ"]]).any():
          for index, row2 in df_tarjetas.iterrows():
               if row2["CLASETARJETA"] == row["CLSTRJ"]:
                    lista_idemia_codinv.append(row2["CODIGOINVENTARIO"])
                    lista_idemia_name.append(row2["NOMBRE"])
                    break
df_idemia_completo["CODINV"] =lista_idemia_codinv
df_idemia_completo["NOMBRE"] =lista_idemia_name
#agrupamos por clase de tarjeta para contar sus registros.
df_thales_agrupado = df_thales_completo.groupby(['CDGPED', 'CLSTRJ', 'DSCCLS'])['CDGPED'].count()
df_idemia_agrupado = df_idemia_completo.groupby(['CDGPED', 'CLSTRJ', 'DSCCLS'])['CDGPED'].count()
print(df_thales_agrupado)
print(df_idemia_agrupado)
#Exportamos a excel el resultado en un solo documento
with pd.ExcelWriter('Output.xlsx') as writer:  
    df_thales_completo.to_excel(writer, sheet_name='Thales Completo')
    df_idemia_completo.to_excel(writer, sheet_name='Idemia Completo')
    df_thales_agrupado.to_excel(writer, sheet_name='Thales agrupado')
    df_idemia_agrupado.to_excel(writer, sheet_name='Idemia agrupado')
cnx_nac.close
