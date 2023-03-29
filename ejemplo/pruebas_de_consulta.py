import pyodbc
import pandas as pd

#Obtenemos los datos necesarios del usuario
user = input("Ingrese su usuario de Nacional: ")
password = input("Ingrese su contraseña de Nacional: ")
fecha = input("Ingrese la fecha de los realces que desea cargar en formato YYYYmmdd: ")
#Conexión a Nacional
try:
     cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(user,password), autocommit=True )
     print("conexión exitosa")
     cnx_nac.close()
except pyodbc.InterfaceError:
     print("usuario y/o contraseña no validos")
     quit()
cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(user,password), autocommit=True )
#Alerta que nos indicará si hay manillas o stickers en IDEMIA
alerta = False 
#Querys
sql_credito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = {}".format(fecha)
sql_debito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = {}".format(fecha)
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
#Agregamos la columna con el proceso
df_alimentacion_credito["PROCESO"] = "CREDITO"
df_alimentacion_debito["PROCESO"] = "DEBITO"
#Los Stickers y manillas NO deben salir por IDEMIA
# además cambiamos todos los carbajal por IDEMIA
for index,row in df_alimentacion_credito.iterrows():
     if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
          df_alimentacion_credito.DSCFBR.at[index, "DSCFBR"] = "THALES              "
          alerta = True
for index,row in df_alimentacion_debito.iterrows():
     if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
          df_alimentacion_debito.DSCFBR.at[index, "DSCFBR"] = "THALES              "
          alerta = True
     if row["DSCFBR"] in ["CARVAJALBG          ", "CARVAJALCL          ", "CARVAJALMD          "]:
          df_alimentacion_debito.at[index, "DSCFBR"] = "IDEMIA              "
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
          for index2, row2 in df_sucursales_cerradas.iterrows():
               if row2["CODIGOOFICINA"] == row["OFICLI"]:
                    if row2["CODIGORECEPTOR"] != -2147483648:
                         df_idemia.at[index,"OFICLI"] = row2["CODIGORECEPTOR"]
for index, row in df_thales.iterrows():
    if df_sucursales_cerradas.CODIGOOFICINA.isin([row["OFICLI"]]).any():
          for index2, row2 in df_sucursales_cerradas.iterrows():
               if row2["CODIGOOFICINA"] == row["OFICLI"]:
                    if row2["CODIGORECEPTOR"] != -2147483648:
                         df_thales.at[index, "OFICLI"] = row2["CODIGORECEPTOR"]
#Agregamos plantas a cada registro según nuestra tabla de plantas por sucursales.
df_thales_completo = pd.merge(df_thales, df_plantas, left_on="OFICLI", right_on="CODIGOOFICINA", how = "left")
df_idemia_completo = pd.merge(df_idemia, df_plantas, left_on="OFICLI", right_on="CODIGOOFICINA", how = "left")
#Cambiamos la planta de realce a THALES porque siempre será BOGOTA
# la clase 104 tambien debe ser siempre BOGOTA
#Transmilenio, transmetro, megabus, Metrolinea debe ser BOGOTA
for index, row in df_thales_completo.iterrows():
     #Thales Siempre se realza en Bogotá
     if row["PLANTAREALCE"] != "BOGOTA":
          df_thales_completo.at[index, "PLANTAREALCE"] = "BOGOTA"
for index, row in df_idemia_completo.iterrows():
     if row["CLSTRJ"] == 110:
          df_idemia_completo.at[index, "PLANTAREALCE"] = "MEDELLIN"
     if row["CIUDAD"] == "BUCARAMANGA":
          if row["CLSTRJ"] == 104:
               df_idemia_completo.at[index, "PLANTAREALCE"] = "BOGOTA"
     if row["CLSTRJ"] == 107:
          df_idemia_completo.at[index, "PLANTAREALCE"] = "CALI"
for index, row in df_idemia_completo.iterrows():    
     if row["CLSTRJ"] in [115,111,105,112,106]:
          df_idemia_completo.at[index, "PLANTAREALCE"] = "BOGOTA"
     
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
df_thales_agrupado = df_thales_completo.groupby(['CODINV','NOMBRETARJETA'])['PLANTAREALCE'].count()
df_idemia_agrupado = df_idemia_completo.groupby(['CODINV','NOMBRETARJETA'])['CODINV'].count()
#eliminamos y agregamos columnas de los dataframes especificados
# (editable, puede cambiar con el tiempo)
#Necesitamos dataframes de credito, de debito, dataframe con cada proveedor y el agrupado.
#Debito y credito, con columna adicional de CLASE TARJETA y PLANTA
df_alimentacion_credito["CLASE TARJETA"] = ""
df_alimentacion_credito["PLANTA"] = ""
df_alimentacion_debito["PLANTA"] = ""
df_alimentacion_debito["CLASE TARJETA"] = ""
#Thales e IDEMIA completos no necesitamos DSCCLS y OFICLI ya que tenemos nuevos.
df_thales_completo.drop(["OFICLI"], axis=1, inplace= True)
df_idemia_completo.drop(["OFICLI"], axis=1, inplace = True)
#Reordenamos credito y debito para facilitar la comprensión y uso de datos.
df_alimentacion_credito = df_alimentacion_credito[["PROCESO","CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICLI","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
df_alimentacion_debito = df_alimentacion_debito[["PROCESO","CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICLI","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
#Reordenamos thales e idemia completos para facilitar comprensión y uso de datos.
df_thales_completo = df_thales_completo[["PROCESO","CODINV","CLSTRJ","DSCCLS", "NOMBRETARJETA", "DSCTRN", "FECNOV", "CDGPED","CODIGOOFICINA", "NIT", "NOMBRE","PLANTAREALCE", "DSCFBR", "SUCURSAL", "CIUDAD" ]]
df_idemia_completo = df_idemia_completo[["PROCESO","CODINV","CLSTRJ","DSCCLS", "NOMBRETARJETA", "DSCTRN", "FECNOV", "CDGPED","CODIGOOFICINA", "NIT", "NOMBRE","PLANTAREALCE", "DSCFBR", "SUCURSAL", "CIUDAD" ]]
#Exportamos a excel el resultado en un solo documento
with pd.ExcelWriter('Output.xlsx') as writer: 
    df_alimentacion_credito.to_excel(writer, sheet_name='Credito', index= False)
    df_alimentacion_debito.to_excel(writer, sheet_name='Debito', index= False) 
    df_thales_completo.to_excel(writer, sheet_name='Thales Completo', index = False)
    df_idemia_completo.to_excel(writer, sheet_name='Idemia Completo', index= False)
    df_thales_agrupado.to_excel(writer, sheet_name='Thales Cargue')
    df_idemia_agrupado.to_excel(writer, sheet_name='Idemia Cargue')
    df_thales_agrupado_clase.to_excel(writer, sheet_name='Thales planta y clase')
    df_idemia_agrupado_clase.to_excel(writer, sheet_name='Idemia planta y clase')
    df_thales_agrupado_planta.to_excel(writer, sheet_name='Thales planta')
    df_idemia_agrupado_planta.to_excel(writer, sheet_name='Idemia planta')
cnx_nac.close
if alerta:
     print ("Cuidado, hay manillas y tarjetas vinculadas a IDEMIA, consulte con el encargado.")
input("Presiona cualquier tecla para salir")
