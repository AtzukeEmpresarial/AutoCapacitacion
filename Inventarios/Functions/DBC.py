import pyodbc
import pandas as pd
import requests
from Screens.message.message import alert_message
import re

#______________________________GLOBAL_______________________________________________________
def find_indexes(cnx_nac,index_name: str, tabla: str):
    '''Consulta los registros existentes en la tabla dada 
    según el indice indicado recibiendo:
    tabla = string con el nombre de la tabla a consultar
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de la tabla.'''
    sql = '''SELECT * FROM CISLIBPR.{}'''.format(tabla)
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,index_name] # type: ignore
    return(indexes)

def find_indexes_where(cnx_nac,index_name: str, tabla: str, index_condition: str, equal: str):
    '''Consulta los registros existentes en la tabla dada 
    según el indice indicado y las condiciones recibidas, recibiendo:
    tabla = string con el nombre de la tabla a consultar
    index_condition = columna a la que se le aplicara la condición
    equal = a lo que debe ser igual la condición
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de la tabla.'''
    sql = """SELECT * FROM CISLIBPR.{} WHERE {} = '{}'""".format(tabla, index_condition, equal)
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,index_name] # type: ignore
    return(indexes)

def find_indexes_where_int(cnx_nac,index_name: str, tabla: str, index_condition: str, equal: int):
    '''Consulta los registros existentes en la tabla dada 
    según el indice indicado y las condiciones recibidas, recibiendo:
    tabla = string con el nombre de la tabla a consultar
    index_condition = columna a la que se le aplicara la condición
    equal = a lo que debe ser igual la condición
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de la tabla.'''
    sql = """SELECT * FROM CISLIBPR.{} WHERE {} = {}""".format(tabla, index_condition, equal)
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,index_name] # type: ignore
    return(indexes)

def import_from_excel (self, path: str, nombre_hoja: str):
    """
    Función que se encarga de importar los datos de un excel
    a un formato que le pueda dar uso Pandas, esta función recibe:
    path = dirección o ruta del archivo excel.
    """
    try:
        df_excel = pd.read_excel(path,sheet_name= nombre_hoja) #, skiprows= 1
        return (df_excel)
    except Exception:
        self.login_message = alert_message(self,self, "La ruta ingresada es incorrecta o el archivo no es compatiple")

def import_from_excel_reporte_semanal (self, path: str, nombre_hoja: str):
    """
    Función (propia del reporte semanal) que se encarga de importar los datos de un excel
    a un formato que le pueda dar uso Pandas, esta función recibe:
    path = dirección o ruta del archivo excel.
    """
    try:
        df_excel = pd.read_excel(path,sheet_name= nombre_hoja, skiprows= 1)
        return (df_excel)
    except Exception:
        self.login_message = alert_message(self,self, "La ruta ingresada es incorrecta o el archivo no es compatiple")

def df_to_sql_bulk_insert(df: pd.DataFrame, table: str, **kwargs) -> str:
    """Metodo que convierte un dataframe valido en una sentencia SQL
    para insertar en la base de datos, recibe:
    df = Dataframe a convertir en sentencia insert de SQL
    tabla = Tabla de la base de datos en donde se realizará la inserción.
    return:
    String  que contiene la sentencia insert de SQL para agregar los datos del Dataframe"""
    df = df.copy().assign(**kwargs)
    columns = ", ".join(df.columns)
    tuples = map(str, df.itertuples(index=False, name=None))
    values = re.sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))
    return f"INSERT INTO {table} ({columns})\nVALUES {values}"

def df_to_sql_bulk_update(df: pd.DataFrame,index: int, table: str, **kwargs) -> str:
    """Metodo que convierte un dataframe valido en una sentencia SQL
    para actualizar en la base de datos, recibe:
    df = Dataframe a convertir en sentencia update de SQL
    index = ID del registro que se debe actualizar
    table = tabla en la base de datos donde se realizará la actualización
    return:
    String  que contiene la sentencia insert de SQL para actualizar los datos del Dataframe"""
    df = df.copy().assign(**kwargs)
    columns = ", ".join(df.columns)
    tuples = map(str, df.itertuples(index=False, name=None))
    values = re.sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))
    return f"UPDATE {table} SET ({columns})\n= {values} WHERE ID = {index} "

def insert(self, cnx_nac , dataframe: pd.DataFrame, tabla: str):
    '''Metodo que se encarga de guardar datos de un Dataframe 
    en una tabla en especifico de la base de datos (NACIONAL):
    cnx_nac = Conexión a nacional.
    dataframe = DataFrame que se insertará en la base de datos
    tabla = string con el nombre de la tabla a consultar'''
    try:
        cursor = cnx_nac.cursor()# type: ignore
        sql_str = df_to_sql_bulk_insert(dataframe,"CISLIBPR.{}".format(tabla))
        print(sql_str)
        cursor.execute(sql_str)
        cnx_nac.commit()# type: ignore
        cursor.close()
        self.login_message = alert_message(self,self, "¡Se creó correctamente el registro!")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "El registro no se pudo crear correctamente\npor favor verifique su conexión y los datos ingresados")

def update(self, cnx_nac , dataframe: pd.DataFrame, index: int, tabla: str):
    '''Metodo que se encarga de actualizar los datos de un Dataframe 
    en una tabla en especifico de la base de datos (NACIONAL):
    cnx_nac = Conexión a nacional.
    dataframe = DataFrame que se insertará en la base de datos
    index = Indice a actualizar.
    tabla = string con el nombre de la tabla a consultar'''
    try:
        cursor = cnx_nac.cursor()# type: ignore
        sql_str = df_to_sql_bulk_update(dataframe,index,"CISLIBPR.{}".format(tabla))
        print(sql_str)
        cursor.execute(sql_str)
        cnx_nac.commit()# type: ignore
        cursor.close()
        self.login_message = alert_message(self,self, "¡El registro se actualizó correctamente!")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "El registro no se pudo actualizar\npor favor verifique su conexión y los datos ingresados")

def find(self,cnx_nac, tabla: str):
    """Se encarga de traer en un Dataframe toda la información de una tabla, recibe:
    tabla = Tabla a la que hace referencia la busqueda
    retorna:
    df = Dataframe con toda la info de la tabla"""
    try:
        sql = f"SELECT * FROM CISLIBPR.{tabla}"
        df = pd.read_sql(sql, con = cnx_nac)
        return (df)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo obtener la información solicitada \npor favor verifique su conexión")
       

def find_by(cnx_nac, columna: str, id: int, tabla: str):
    '''Metodo que se encaga de consultar desde la base de datos según el ID
    y retorna un DataFrame recibiendo:
    id = int con el id del registro que se busca
    tabla = string con el nombre de la tabla a consultar
    return:
    DataFrame que contiene el registro correspondiente al ID'''
    sql = '''SELECT * FROM CISLIBPR.{} WHERE {} = {}'''.format(tabla, columna, id)
    ids_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    return(ids_df)

def delete(self, cnx_nac,column: str, reg: int, tabla: str):
    '''Elimina el registro indicado.
    column = la en la que se buscara el registro
    reg = registro que se buscara
    tabla = string con el nombre de la tabla a consultar'''
    try:
        cursor = cnx_nac.cursor()
        sql = '''DELETE FROM CISLIBPR.{} WHERE {} = {}'''.format(tabla, column, reg)
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
        self.login_message = alert_message(self,self, "¡El registro se eliminó correctamente!")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "El registro no se pudo eliminar\npor favor verifique su conexión y los datos ingresados")

def TRM (self):
    url = "https://www.datos.gov.co/resource/32sa-8pi3.json?$order=vigenciadesde%20DESC&$limit=1"

    response = requests.get(url)

    if response.status_code == 200:
        trm = response.json()[0]["valor"]
        return(trm)
    else:
        self.login_message = alert_message(self,self, "No se pudo obtener el TRM actual\npor favor verifique su conexión")

def excel(df: pd.DataFrame, nombre: str):
    with pd.ExcelWriter(nombre + '.xlsx') as writer: 
            df.to_excel(writer, sheet_name = nombre, index = False)






#__________________________________________LOG_IN______________________________________________
def check_credentials (user: str, password: str):
    """
    Función que se encarga de verificar si un usuario existe 
    en el sistema de Nacional o Medellín segun se configure,
    a esta función entran:
    user = Usuario.
    password = Contraseña del usuario.
    """
    try:
        cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID={};PWD={}'.format(user,password), autocommit=True )
        print("conexión exitosa")
        cnx_nac.close()
        return(True)
    except pyodbc.InterfaceError:
        print("usuario y/o contraseña no validos")
        return(False)
    







#______________________________Proveedores____________________________________________________________
def verificar_provedor(self, cnx_nac, nombre: str) :
    try:
        sql = f"SELECT * FROM CISLIBPR.PROVEEDORES WHERE NOMBRE = '{nombre}'"
        df_proveedor = pd.read_sql(sql, con = cnx_nac)
        return(df_proveedor)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar provedores \npor favor verifique su conexión")






#________________________________Sucursales__________________________________________
def load_in_sucursales (self, cnx_nac,  df_sucursales: pd.DataFrame):
    try:
        cursor = cnx_nac.cursor()
        cursor.execute("DELETE FROM CISLIBPR.SUCURSALES")
        for index, row in df_sucursales.iterrows():
            cursor.execute("INSERT INTO CISLIBPR.SUCURSALES (CODIGOOFICINA,SUCURSAL,CIUDAD,PLANTAREALCE) VALUES({},'{}','{}','{}')".format(row["CODIGOOFICINA"],row["SUCURSAL"],row["CIUDAD"],row["PLANTAREALCE"]))
        cursor.commit()
        cursor.close()
        self.login_message = alert_message(self,self, "Se cargaron las sucursales con exito")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "Los datos no se pudieron descargar\npor favor verifique su conexión y el excel seleccionado")











#________________________________Plantas_____________________________________________
def verificar_planta(self, cnx_nac, ubicacion: str, operador: str, produccion: int) :
    try:
        sql = f"SELECT * FROM CISLIBPR.PLANTAS WHERE UBICACION = '{ubicacion}' AND OPERADOR = '{operador}' AND PRODUCCION = {produccion}"
        df_planta = pd.read_sql(sql, con = cnx_nac)
        return(df_planta)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar plantas \npor favor verifique su conexión")








#______________________________________Plasticos__________________________________________
def find_planta_x_provedor(self, cnx_nac, provedor: str):
    '''consulta las plantas según su provedor.
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de la tabla.'''
    sql = f"""SELECT * FROM CISLIBPR.PLANTAS WHERE OPERADOR = '{provedor}' AND PRODUCCION = 0"""
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,"UBICACION"] # type: ignore
    return(indexes)




#__________________________________ITEMS______________________________________________
def find_codinv_by_nombre_item(cnx_nac, nombre: str):
    '''Metodo que se encaga de consultar el CODINV desde la base de datos según el nombre 
    de un plastico, recibiendo:
    nombre = nombre del plastico
    return:
    codinv = int que indica el codigo de inventario del plastico'''
    sql = """SELECT CODINV FROM CISLIBPR.PLASTICOS WHERE NOMBRE = '{}'""".format(nombre)
    ids_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    codinv = ids_df.loc[0,"CODINV"]
    return(codinv)

def genera_lista_planta_x_provedor(cnx_nac, provedor):
    """Metodo que se encarga de consultar la tabla de plantas"""
    sql = f"SELECT * FROM CISLIBPR.PLANTAS WHERE OPERADOR = '{provedor}'"
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,"UBICACION"] # type: ignore
    return(indexes)

    
        



#_________________________Reporte Semanal__________________________________________________

def comparar_inventarios_thales(self, cnx_nac, df: pd.DataFrame):
    """Función que se encarga de generar un dataframe con los valores comparados de
    el inventario reportado por THALES y el inventario registrado en el sistema"""
    sql = "SELECT * FROM CISLIBPR.INVENTARIOTJ WHERE PROVEDOR = 'THALES'"
    df_inventario = pd.read_sql(sql, con = cnx_nac)
    df_comparativo = pd.merge(df, df_inventario, left_on="CODIGO INVENTARIO", right_on="CODINV", how = "left")
    df_comparativo.drop(["CONSUMO SEMANAL", "DAÑOS","MUESTRAS O PRUEBAS ", "INGRESOS","ID","CODINV","NOMBRE","PROVEDOR","PLANTA"], axis = 1,inplace=True)
    return(df_comparativo)
    











def load_in_inventariostj (self, cnx_nac,  df_inventarios: pd.DataFrame):
    try:
        cursor = cnx_nac.cursor()
        cursor.execute("DELETE FROM CISLIBPR.INVENTARIOTJ")
        for index, row in df_inventarios.iterrows():
            cursor.execute("INSERT INTO CISLIBPR.INVENTARIOTJ (CODINV,NOMBRE,PROVEDOR,PLANTA,CANTIDAD) VALUES(?,?,?,?,?)", row.CODINV,row.NOMBRE,row.PROVEDOR,row.PLANTA,row.CANTIDAD)
        cursor.commit()
        cursor.close()
        self.login_message = alert_message(self,self, "Se cargó el inventario con exito")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "Los datos no se pudieron descargar\npor favor verifique su conexión y el excel seleccionado")


def find_by_nombre(cnx_nac, columna: str, nombre: str, tabla: str):
    '''Metodo que se encaga de consultar desde la base de datos según el CODINV
    y retorna un DataFrame recibiendo:
    DataFrame que contiene el registro correspondiente al nombre'''
    sql = """SELECT * FROM CISLIBPR.{} WHERE {} = '{}'""".format(tabla, columna, nombre)
    codinv_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    return(codinv_df)

def find_by_id_traslados(self, cnx_nac, id: int):
    '''Metodo que se encaga de consultar desde la base de datos según el ID
    y retorna un DataFrame recibiendo:
    id = int con el id del registro que se busca
    return:
    DataFrame que contiene el registro correspondiente al ID'''
    try:
        sql = '''SELECT * FROM CISLIBPR.MOVIMIENTOS WHERE ID = {} AND IDTIPOMOV = 2'''.format(id)
        ids_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
        return(ids_df)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No existe el registro asociado a esa ID\npor favor verifique su conexión y el ID solicitado")
    
def find_plantas_x_proveedor(self, cnx_nac,index_name: str, provedor: str, produccion: int):
    '''Consulta la tabla de plantas para traer solo los indices indicados, recibiendo:
    self = objeto padre
    cnx_nac = cadena de conexión global
    index_condition = columna a la que se le aplicara la condición
    provedor = Provedor a consultar
    produccion = 0 o 1 para indicar si se busca o no plantas de produccion
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de plantas'''
    try:
        sql = f"""SELECT * FROM CISLIBPR.PLANTAS WHERE OPERADOR = '{provedor}' AND PRODUCCION = {produccion}"""
        indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
        indexes = indexes_df.loc[:,index_name] # type: ignore
        return(indexes)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo conectar a plantas\npor favor verifique su conexión")
    
def inventario_x_planta_provedor(self, cnx_nac, planta: str, provedor: str):
    """COnsulta el ivnentario según la planta y el provedor, 
    retorna un DF con estos datos"""
    sql = f"SELECT * FROM CISLIBPR.INVENTARIOTJ WHERE PLANTA = '{planta}' AND PROVEDOR = '{provedor}'"
    df = pd.read_sql(sql, con = cnx_nac)
    return(df)

def consultar_cantidad(self, cnx_nac, codinv: int, planta: str, proveedor: str):
    """Consulta la cantidad de plasticos disponibles en una planta de un proveedor 
    en especifico. Recibe:
    cnx_nac = cadena de conexión global
    codinv = codigo de inventario del plastico
    planta = planta de la que se desea hacer el traslado
    proveedor = proveedor del cual se va a hacer el traslado
    devuelve:
    candtidad = dato de tipo int que contiene la cantidad actual de plasticos referenciados"""
    try:
        cantidad = 0
        sql = "SELECT CANTIDAD FROM CISLIBPR.INVENTARIOTJ WHERE CODINV = {} AND PLANTA = '{}' AND PROVEDOR = '{}'".format(codinv, planta, proveedor)
        df_cantidad = pd.read_sql(sql, con = cnx_nac)
        for index, row in df_cantidad.iterrows():
            cantidad = row["CANTIDAD"]
            return(cantidad)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo verificar la cantidad actual de plasticos \npor favor verifique su conexión")
    

def consultar_ultimo_pedido_thales_idemia(self, cnx_nac):
    """Consulta la tabla de ultimo pedido y actualiza la lista
    con  el ultimo codigo de pedido de thales e idemia en su lista correspondiente,
    requiere:
    self = el objeto de donde se llama,
    cnx_nac = cadena de conexión global"""
    self.ls_pedidos[:] = []
    sql = """SELECT * FROM CISLIBPR.CODIGOPED"""
    df_pedidos = pd.read_sql(sql,con = cnx_nac)# type: ignore
    for index, row in df_pedidos.iterrows():
        self.ls_pedidos.append(row["ULTIMOTHALES"])
        self.ls_pedidos.append(row["ULTIMOIDEMIA"])
        self.ls_pedidos.append(row["ULTIMOMANANA"])
        self.ls_pedidos.append(row["ULTIMOTARDE"])

def actualizar_ultimo_pedido_thales_idemia(self, cnx_nac, ultimo_thales_actual: int, ultimo_idemia_actual: int, ultimo_manana_actual: int, ultimo_tarde_actual: int):
    """Consulta la tabla de ultimo pedido y actualiza la lista
    con  el ultimo codigo de pedido de thales e idemia en su lista correspondiente,
    requiere:
    self = el objeto de donde se llama,
    cnx_nac = cadena de conexión global,
    ultimo_thales_actual = ultimo codigo de thales actual, despues de subir los datos,
    ultimo_idemia_actual = ultimo codigo de thales actual, despues de subir los datos"""
    try:
        cursor = cnx_nac.cursor()
        self.ls_pedidos[:] = []
        sql1 = """DELETE FROM CISLIBPR.CODIGOPED"""
        sql2 = '''INSERT INTO CISLIBPR.CODIGOPED (ULTIMOTHALES, ULTIMOIDEMIA, ULTIMOMANANA, ULTIMOTARDE) VALUES ({},{},{},{})'''.format(ultimo_thales_actual, ultimo_idemia_actual, ultimo_manana_actual, ultimo_tarde_actual)
        cursor.execute(sql1)
        cursor.execute(sql2)
        cursor.commit()
        cursor.close()
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo verificar el ultimo consecutivo \npor favor verifique su conexión")

def traslado_salida(self, cnx_nac, codinv: int, planta: str, proveedor: str, cantidad: int):
    """Actualiza el inventario con la salida de los plasticos solicitados en el traslado"""
    try:
        cursor = cnx_nac.cursor()
        sql = "UPDATE CISLIBPR.INVENTARIOTJ SET CANTIDAD = CANTIDAD - {} WHERE CODINV = {} AND PLANTA = '{}' AND PROVEDOR = '{}'".format(cantidad, codinv, planta, proveedor)
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo actualizar el inventario \npor favor verifique su conexión")

def deshacer_traslado_salida(self, cnx_nac, codinv: int, planta: str, proveedor: str, cantidad: int):
    """deshace un traslado, tambien utilizado para completar un traslado al sumar la
    cantidad especidifcada en el traslado a la planta final"""
    try:
        cursor = cnx_nac.cursor()
        sql = "UPDATE CISLIBPR.INVENTARIOTJ SET CANTIDAD = CANTIDAD + {} WHERE CODINV = {} AND PLANTA = '{}' AND PROVEDOR = '{}'".format(cantidad, codinv, planta, proveedor)
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo deshacer el traslado \npor favor verifique su conexión y el ID de traslado ingresado") 

def pedidos_parciales(self, cnx_nac, id_pedido: int, cantidad: int, codinv: int, planta: str, proveedor: str):
    """Actualiza la cantidad de plasticos entregados del pedido, y alimenta el inventario"""
    try:
        cursor = cnx_nac.cursor()
        sql = f"UPDATE CISLIBPR.PEDIDOSTJ SET CANTIDADDESP = CANTIDADDESP + {cantidad} WHERE ID = {id_pedido}"
        sql2 = f"UPDATE CISLIBPR.INVENTARIOTJ SET CANTIDAD = CANTIDAD + {cantidad} WHERE CODINV = {codinv} AND PLANTA = '{planta}' AND PROVEDOR = '{proveedor}'"
        cursor.execute(sql)
        cursor.execute(sql2)
        cursor.commit()
        cursor.close()
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo agregar el despacho parcial del pedido \npor favor verifique su conexión y el ID de traslado ingresado")  

def completar_pedido(self, cnx_nac, id_pedido: int):
    """Marca un pedido como completo"""
    try:
        cursor = cnx_nac.cursor()
        sql = f"UPDATE CISLIBPR.PEDIDOSTJ SET ESTADO = 'Cerrado' WHERE ID = {id_pedido}"
        cursor.execute(sql)
        cursor.commit()
        cursor.close()
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo marcar el pedido como completo \npor favor verifique su conexión y el ID de traslado ingresado")  


def marcar_traslado_completo(self, cnx_nac, id: int, fecha_final:str):
    """Marca el traslado identificado con la ID ingresada como completo"""
    try: 
        cursor = cnx_nac.cursor()
        sql = "UPDATE CISLIBPR.MOVIMIENTOS SET COMPLETO = 1, FECHALLEGADA = {} WHERE ID = {} ".format(fecha_final, id)
        cursor.execute(sql)
        cursor.commit()
        cursor.close()   
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo marcar el traslado como completo \npor favor verifique su conexión y el ID de traslado ingresado")   

def Traslados_pendientes(self, cnx_nac):
    """Consulta los traslados pendientes, recibe:
    cnx_nac = cadena de conexión
    retorna:
    df_pendientes = dataframe que contiene los traslados pendientes (no marcados como
    completos)"""
    try: 
        sql = """SELECT * FROM CISLIBPR.MOVIMIENTOS WHERE IDTIPOMOV = 2 AND COMPLETO = 0"""
        df_pendientes = pd.read_sql(sql,con = cnx_nac)# type: ignore
        return(df_pendientes) 
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar los traslados pendientes \npor favor verifique su conexión") 

def pedidos_pendientes(self, cnx_nac):
    """Consulta los pedidos pendientes, recibe:
    cnx_nac = cadena de conexión
    retorna:
    df_pendientes = dataframe que contiene los traslados pendientes (no marcados como
    completos)"""
    try: 
        sql = """SELECT * FROM CISLIBPR.PEDIDOSTJ WHERE ESTADO = 'Abierto'"""
        df_pendientes = pd.read_sql(sql,con = cnx_nac)# type: ignore
        return(df_pendientes) 
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar los pedidos pendientes \npor favor verifique su conexión")  
    

def alimentar_inventario(self, cnx_nac, df_thales: pd.DataFrame, df_idemia: pd.DataFrame, fecha: str):
    """COnsulta que se encarga de agregar a la tabla de movimeintos todos los realces
    que se realizaron en el día especificado, debe restar al inventario total. requiere:
    cnx_nac = cadena de conexión global.+
    df_thales = Dataframe correctamente agrupado de thales para tener el total de 
    realzados por codigo de inventario y planta.
    df_idemia = Dataframe correctamente agrupado de idemia para tener el total de 
    realzados por codigo de inventario y planta.
    fecha = fecha que se usó para la consulta de los datos en Nacional, es la del día 
    de los realces."""
    cursor = cnx_nac.cursor()
    try:
        sql = "SELECT * FROM CISLIBPR.INVENTARIOTJ"
        df_inventario = pd.read_sql(sql, con = cnx_nac)
        with pd.ExcelWriter('Copias De Inventario.xlsx') as writer: 
            df_inventario.to_excel(writer, sheet_name=fecha, index= False)
        for index, row in df_thales.iterrows():
            sql ="INSERT INTO CISLIBPR.MOVIMIENTOS (CODINV, PROVEEDOR, PLANTA,PLANTAFINAL, IDTIPOMOV, FECHA, FECHALLEGADA, CANTIDAD, COMPLETO) VALUES  ({},'{}','{}','{}',{},'{}','{}', {}, {})".format(int(row["CODINV"]), "THALES",row["PLANTA"],"", 1, fecha, "", int(row["REALZADO"]), 1)
            cursor.execute(sql)
            sql = "UPDATE cislibpr.INVENTARIOTJ SET CANTIDAD = CANTIDAD - {} WHERE CODINV = {} AND PROVEDOR = '{}' AND PLANTA = '{}'".format(int(row["REALZADO"]),int(row["CODINV"]), "THALES", row["PLANTA"] )
            cursor.execute(sql)
        for index, row in df_idemia.iterrows():
            sql ="INSERT INTO CISLIBPR.MOVIMIENTOS (CODINV, PROVEEDOR, PLANTA,PLANTAFINAL, IDTIPOMOV, FECHA, FECHALLEGADA, CANTIDAD, COMPLETO) VALUES  ({},'{}','{}','{}',{},'{}','{}', {}, {})".format(int(row["CODINV"]), "IDEMIA" ,row["PLANTA"],"", 1, fecha, "", int(row["REALZADO"]), 1)
            cursor.execute(sql)
            sql = "UPDATE cislibpr.INVENTARIOTJ SET CANTIDAD = CANTIDAD - {} WHERE CODINV = {} AND PROVEDOR = '{}' AND PLANTA = '{}'".format(int(row["REALZADO"]),int(row["CODINV"]), "IDEMIA", row["PLANTA"] )
            cursor.execute(sql)
        cursor.commit()
        cursor.close()
        self.login_message = alert_message(self,self, "Los datos se cargaron correctamente en el inventario")
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo actualizar el inventario\npor favor verifique su conexión, fecha y consecutivos ingresados")

def daily(self, cnx_nac, fecha: str, pedido_thales: int, ls_pedidos_idemia, ls_pedidos_manana, ls_pedidos_tarde):
    """Consulta en nacional todos los realces que se realizaron el día seleccionado y
    devuelve varios Dataframe en una lista"""
    try:
        #Definimos una Alerta que nos indicará si hay manillas o stickers en IDEMIA
        alerta = False 
        #Querys
        sql_credito = "SELECT * FROM CISLIBPR.ACREALCECR WHERE FECNOV = {}".format(fecha)
        sql_debito = "SELECT * FROM CISLIBPR.ACREALCEDB WHERE FECNOV = {}".format(fecha)
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
        #Los Stickers y manillas NO deben salir por IDEMIA, se genera alerta
        # además cambiamos todos los carbajal por IDEMIA
        for index,row in df_alimentacion_credito.iterrows():
            if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
                alerta = True
        for index,row in df_alimentacion_debito.iterrows():
            if row["CLSTRJ"] in [118,117] and row["DSCFBR"] in ["IDEMIA              ","IDEMIA.             "]:
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
            if row["OFICLI"] in df_sucursales_cerradas.CODIGOOFICINA.values:
                for index2, row2 in df_sucursales_cerradas.iterrows():
                    if row2["CODIGOOFICINA"] == row["OFICLI"]:
                            if row2["CODIGORECEPTOR"] != -2147483648:
                                df_idemia.at[index,"OFICLI"] = row2["CODIGORECEPTOR"]
        for index, row in df_thales.iterrows():
            if row["OFICLI"] in df_sucursales_cerradas.CODIGOOFICINA.values:
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
            if row["CLSTRJ"] in [110,116]:
                df_idemia_completo.at[index, "PLANTAREALCE"] = "MEDELLIN"
            if row["CLSTRJ"] == 104 and row["PLANTAREALCE"] == "BUCARAMANGA":
                df_idemia_completo.at[index, "PLANTAREALCE"] = "BOGOTA"
            if row["CLSTRJ"] in [107,113]:
                df_idemia_completo.at[index, "PLANTAREALCE"] = "CALI"
        for index, row in df_idemia_completo.iterrows():    
            if row["CLSTRJ"] in [115,109,111,105,112,106, 83]:
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
        #creamos un filtro para que solo sean los pedidos deseados
        filter_thales = df_thales_completo.CDGPED.isin([pedido_thales])
        ls_pedidos = ls_pedidos_idemia + ls_pedidos_manana + ls_pedidos_tarde
        filter_idemia = df_idemia_completo.CDGPED.isin(ls_pedidos)
        df_thales_completo2 = df_thales_completo[filter_thales]
        print(df_thales_completo2)
        df_idemia_completo2 = df_idemia_completo[filter_idemia]
        print(df_idemia_completo2)
        #agrupamos por clase de tarjeta para contar sus registros.
        df_thales_agrupado_clase = df_thales_completo2.groupby(['PLANTAREALCE', 'CODINV', 'NOMBRETARJETA'])['PLANTAREALCE'].count()
        df_idemia_agrupado_clase = df_idemia_completo2.groupby(['PLANTAREALCE', 'CODINV', 'NOMBRETARJETA'])['PLANTAREALCE'].count()
        #eliminamos y agregamos columnas de los dataframes especificados
        # (editable, puede cambiar con el tiempo)
        #Necesitamos dataframes de credito, de debito, dataframe con cada proveedor y el agrupado.
        #Debito y credito, con columna adicional de CLASE TARJETA y PLANTA
        df_alimentacion_credito["CLASE TARJETA"] = ""
        df_alimentacion_credito["PLANTA"] = ""
        df_alimentacion_debito["PLANTA"] = ""
        df_alimentacion_debito["CLASE TARJETA"] = ""
        #Thales e IDEMIA completos no necesitamos DSCCLS y OFICLI ya que tenemos nuevos.
        df_thales_completo2.drop(["OFICLI"], axis=1, inplace= True)
        df_idemia_completo2.drop(["OFICLI"], axis=1, inplace = True)
        #Reordenamos credito y debito para facilitar la comprensión y uso de datos.
        df_alimentacion_credito = df_alimentacion_credito[["PROCESO","CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICLI","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
        df_alimentacion_debito = df_alimentacion_debito[["PROCESO","CLSTRJ","DSCCLS","CLASE TARJETA", "DSCTRN", "FECNOV", "CDGPED","OFICINA","PLANTA", "NIT", "NOMBRE", "DSCFBR"]]
        #Reordenamos thales e idemia completos para facilitar comprensión y uso de datos.
        df_thales_completo2 = df_thales_completo2[["PROCESO","CODINV","CLSTRJ","DSCCLS", "NOMBRETARJETA", "DSCTRN", "FECNOV", "CDGPED","CODIGOOFICINA","PLANTAREALCE", "NIT", "NOMBRE", "DSCFBR", "SUCURSAL", "CIUDAD" ]]
        df_idemia_completo2 = df_idemia_completo2[["PROCESO","CODINV","CLSTRJ","DSCCLS", "NOMBRETARJETA", "DSCTRN", "FECNOV", "CDGPED","CODIGOOFICINA","PLANTAREALCE", "NIT", "NOMBRE", "DSCFBR", "SUCURSAL", "CIUDAD" ]]
        df_thales_completo2.rename(columns={"NOMBRETARJETA": "CLASE TARJETA"}, inplace= True)
        df_thales_completo2.rename(columns={"CODIGOOFICINA": "OFICLI"}, inplace= True)
        df_thales_completo2.rename(columns={"PLANTAREALCE": "PLANTA"}, inplace= True)
        df_idemia_completo2.rename(columns={"NOMBRETARJETA": "CLASE TARJETA"}, inplace= True)
        df_idemia_completo2.rename(columns={"CODIGOOFICINA": "OFICLI"}, inplace= True)
        df_idemia_completo2.rename(columns={"PLANTAREALCE": "PLANTA"}, inplace= True)
        #Exportamos a excel el resultado en un solo documento
        with pd.ExcelWriter('Output.xlsx') as writer: 
            df_alimentacion_credito.to_excel(writer, sheet_name='Credito', index= False)
            df_alimentacion_debito.to_excel(writer, sheet_name='Debito', index= False) 
            df_thales_completo.to_excel(writer, sheet_name='Thales Completo1', index = False)
            df_idemia_completo.to_excel(writer, sheet_name='Idemia Completo1', index= False)
            df_thales_completo2.to_excel(writer, sheet_name='Thales Completo2', index = False)
            df_idemia_completo2.to_excel(writer, sheet_name='Idemia Completo2', index= False)
            df_thales_agrupado_clase.to_excel(writer, sheet_name='Thales planta y clase')
            df_idemia_agrupado_clase.to_excel(writer, sheet_name='Idemia planta y clase')
        df_thales_agrupado_clase.index.names = ["PLANTA", "CODINV", "NOMBRE"]
        df_idemia_agrupado_clase.index.names = ["PLANTA", "CODINV", "NOMBRE"]
        self.df_thales_agrupado = df_thales_agrupado_clase.reset_index()
        self.df_thales_agrupado.rename(columns={"PLANTAREALCE": "REALZADO"}, inplace= True)
        self.df_idemia_agrupado = df_idemia_agrupado_clase.reset_index()
        self.df_idemia_agrupado.rename(columns={"PLANTAREALCE": "REALZADO"}, inplace = True)
        self.login_message = alert_message(self,self, "Los datos se descargaron correctamente\n por favor verifique su integridad")
        return(alerta)
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "Los datos no se pudieron descargar\npor favor verifique su conexión, fecha y consecutivos ingresados")
    
def verificar_inventario(self, cnx_nac, codinv: int, provedor: str, planta:str):
    try: 
        sql = f"""SELECT * FROM CISLIBPR.INVENTARIOTJ WHERE CODINV = {codinv} AND PROVEDOR = '{provedor}' AND PLANTA = '{planta}'"""
        df_items = pd.read_sql(sql,con = cnx_nac)# type: ignore
        return(df_items) 
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar en items \npor favor verifique su conexión")

def items(self, cnx_nac):
    """Consulta los pedidos items, recibe:
    cnx_nac = cadena de conexión
    retorna:
    df_pendientes = dataframe que contiene todos los items (inventario)"""
    try: 
        sql = """SELECT * FROM CISLIBPR.INVENTARIOTJ"""
        df_items = pd.read_sql(sql,con = cnx_nac)# type: ignore
        return(df_items) 
    except pyodbc.InterfaceError:
        self.login_message = alert_message(self,self, "No se pudo consultar los pedidos pendientes \npor favor verifique su conexión")


#_______________________________________________INFORMES__________________________________________________________
def movimientos_plastico(self, cnx_nac,):
    sql = "SELECT * FROM CISLIBPR.MOVIMIENTOS WHERE FECHA >= '20230401' AND FECHA <= '20230407' AND CODINV = 31 AND PLANTA = 'BOGOTA' AND PROVEEDOR = 'IDEMIA'"