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
#insertamos el codigo de inventario y cambiamos el nombre




print(lista_debito)
print(df_alimentacion_debito_sucio)
print(df_alimentacion_debito)
print(lista_credito)
print(df_alimentacion_credito_sucio)
print(df_alimentacion_credito)


