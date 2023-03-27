import pyodbc
import pandas as pd


#Conexión a Nacional
cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=nserposad;PWD=atzuke24', autocommit=True )
#Alerta que nos indicará si hay manillas o stickers en IDEMIA
alerta = False 
#Querys
sql_credito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = 20230324"
sql_debito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = 20230324"
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
#Los Stickers y manillas NO deben salir por IDEMIA
# además cambiamos todos los carbajal por IDEMIA
for index,row in df_alimentacion_credito.iterrows():
     if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
          df_alimentacion_credito.DSCFBR.replace({row["DSCFBR"]: "THALES              "}, inplace = True)
          alerta = True
for index,row in df_alimentacion_debito.iterrows():
     if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
          df_alimentacion_debito.DSCFBR.replace({row["DSCFBR"]: "THALES              "}, inplace= True)
          alerta = True
     if row["DSCFBR"] in ["CARVAJALBG          ", "CARVAJALCL          ", "CARVAJALMD          "]:
          df_alimentacion_debito.DSCFBR.replace({row["DSCFBR"]: "IDEMIA              "}, inplace= True)
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
#Cambiamos la planta de realce a THALES porque siempre será BOGOTA
# la clase 104 tambien debe ser siempre BOGOTA
#Transmilenio, transmetro, megabus, Metrolinea debe ser BOGOTA
for index, row in df_thales_completo.iterrows():
     #Thales Siempre se realza en Bogotá
     if row["PLANTAREALCE"] != "BOGOTA":
          df_thales_completo.PLANTAREALCE.replace({row["PLANTAREALCE"] : "BOGOTA"}, inplace = True)
for index, row in df_idemia_completo.iterrows():
     if row["CLSTRJ"] in [115,111,105,112,106]:
          df_idemia_completo.PLANTAREALCE.replace({row["PLANTAREALCE"]: "BOGOTA"}, inplace = True)
     if row["CLSTRJ"] == 110:
          df_idemia_completo.PLANTAREALCE.replace({row["PLANTAREALCE"]: "MEDELLIN"}, inplace = True)
     if row["CLSTRJ"] == 104 and row["CIUDAD"] == "BUCARAMANGA":
          df_idemia_completo.PLANTAREALCE.replace({row["PLANTAREALCE"]: "BOGOTA"}, inplace = True)
     if row["CLSTRJ"] == 107:
          df_idemia_completo.PLANTAREALCE.replace({row["PLANTAREALCE"]: "CALI"}, inplace = True)
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
df_thales_completo["NOMBRETARJETA"] = lista_thales_name
for index, row in df_idemia_completo.iterrows():
     if df_tarjetas.CLASETARJETA.isin([row["CLSTRJ"]]).any():
          for index, row2 in df_tarjetas.iterrows():
               if row2["CLASETARJETA"] == row["CLSTRJ"]:
                    lista_idemia_codinv.append(row2["CODIGOINVENTARIO"])
                    lista_idemia_name.append(row2["NOMBRE"])
                    break
df_idemia_completo["CODINV"] =lista_idemia_codinv
df_idemia_completo["NOMBRETARJETA"] =lista_idemia_name
#agrupamos por clase de tarjeta para contar sus registros.
df_thales_agrupado_clase = df_thales_completo.groupby(['PLANTAREALCE', 'CODINV', 'NOMBRETARJETA'])['PLANTAREALCE'].count()
df_idemia_agrupado_clase = df_idemia_completo.groupby(['PLANTAREALCE', 'CODINV', 'NOMBRETARJETA'])['PLANTAREALCE'].count()
df_thales_agrupado_planta = df_thales_completo.groupby(['PLANTAREALCE'])['PLANTAREALCE'].count()
df_idemia_agrupado_planta = df_idemia_completo.groupby(['PLANTAREALCE'])['PLANTAREALCE'].count()
#eliminamos y agregamos columnas de los dataframes especificados
# (editable, puede cambiar con el tiempo)
#Necesitamos dataframes de credito, de debito, dataframe con cada proveedor y el agrupado.
#Debito y credito, con columna adicional de CLASE TARJETA y PLANTA
df_alimentacion_credito["CLASE TARJETA"] = ""
df_alimentacion_credito["PLANTA"] = ""
df_alimentacion_debito["CLASE TARJETA"] = ""
df_alimentacion_debito["PLANTA"] = ""
#Thales e IDEMIA completos no necesitamos DSCCLS y OFICLI ya que tenemos nuevos.
df_thales_completo.drop(["DSCCLS", "OFICLI"], axis=1)
df_idemia_completo.drop(["DSCCLS", "OFICLI"], axis=1)
#Reordenamos para facilitar la comprensión y uso de datos.
df_alimentacion_credito = df_alimentacion_credito[["CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICLI","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
df_alimentacion_debito = df_alimentacion_debito[["CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICLI","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
#Exportamos a excel el resultado en un solo documento
with pd.ExcelWriter('Output.xlsx') as writer: 
    df_alimentacion_credito.to_excel(writer, sheet_name='Credito', index= False)
    df_alimentacion_debito.to_excel(writer, sheet_name='Debito', index= False) 
    df_thales_completo.to_excel(writer, sheet_name='Thales Completo')
    df_idemia_completo.to_excel(writer, sheet_name='Idemia Completo')
    df_thales_agrupado_clase.to_excel(writer, sheet_name='Thales agrupado por clase')
    df_idemia_agrupado_clase.to_excel(writer, sheet_name='Idemia agrupado por clase')
    df_thales_agrupado_planta.to_excel(writer, sheet_name='Thales agrupado por planta')
    df_idemia_agrupado_planta.to_excel(writer, sheet_name='Idemia agrupado por planta')
cnx_nac.close
if alerta:
     print ("Cuidado, hay manillas y tarjetas vinculadas a IDEMIA, consulte con el encargado.")
