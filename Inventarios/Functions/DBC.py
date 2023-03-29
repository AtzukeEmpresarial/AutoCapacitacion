import pyodbc
import pandas as pd
from Screens.message.message import alert_message
import re


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

def import_from_excel (self, path: str):
    """
    Función que se encarga de importar los datos de un excel
    a un formato que le pueda dar uso Pandas, esta función recibe:
    path = dirección o ruta del archivo excel.
    """
    try:
        df_excel = pd.read_excel(path,sheet_name="Feb 06", skiprows= 1)
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


def insert(cnx_nac , dataframe: pd.DataFrame, tabla: str):
    '''Metodo que se encarga de guardar datos de un Dataframe 
    en una tabla en especifico de la base de datos (NACIONAL):
    cnx_nac = Conexión a nacional.
    dataframe = DataFrame que se insertará en la base de datos
    tabla = string con el nombre de la tabla a consultar'''
    cursor = cnx_nac.cursor()# type: ignore
    sql_str = df_to_sql_bulk_insert(dataframe,"CISLIBPR.{}".format(tabla))
    print(sql_str)
    cursor.execute(sql_str)
    cnx_nac.commit()# type: ignore
    cursor.close()

def update(cnx_nac , dataframe: pd.DataFrame, index: int, tabla: str):
    '''Metodo que se encarga de actualizar los datos de un Dataframe 
    en una tabla en especifico de la base de datos (NACIONAL):
    cnx_nac = Conexión a nacional.
    dataframe = DataFrame que se insertará en la base de datos
    index = Indice a actualizar.
    tabla = string con el nombre de la tabla a consultar'''
    cursor = cnx_nac.cursor()# type: ignore
    sql_str = df_to_sql_bulk_update(dataframe,index,"CISLIBPR.{}".format(tabla))
    print(sql_str)
    cursor.execute(sql_str)
    cnx_nac.commit()# type: ignore
    cursor.close()

def find_by(cnx_nac, columna: str, id: int, tabla: str):
    '''Metodo que se encaga de consultar desde la base de datos según el ID
    y retorna un DataFrame recibiendo:
    user = string con el usuario
    password = string con la contraseña
    id = int con el id del registro que se busca
    tabla = string con el nombre de la tabla a consultar
    return:
    DataFrame que contiene el registro correspondiente al ID'''
    sql = '''SELECT * FROM CISLIBPR.{} WHERE {} = {}'''.format(tabla, columna, id)
    ids_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    return(ids_df)

def find_indexes(cnx_nac,index_name: str, tabla: str):
    '''Consulta los registros existentes en la tabla Plasticos 
    según el indice indicado recibiendo:
    user = string con el usuario
    password = string con la contraseña
    tabla = string con el nombre de la tabla a consultar
    return:
    Serie de pandas que contiene todos registros según el indice 
    indicado de la tabla.'''
    sql = '''SELECT * FROM CISLIBPR.{}'''.format(tabla)
    indexes_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
    indexes = indexes_df.loc[:,index_name] # type: ignore
    return(indexes)

def delete(cnx_nac,column: str, reg: int, tabla: str):
    '''Elimina el registro indicado.
    column = la en la que se buscara el registro
    reg = registro que se buscara
    tabla = string con el nombre de la tabla a consultar'''
    cursor = cnx_nac.cursor()
    sql = '''DELETE FROM CISLIBPR.{} WHERE {} = {}'''.format(tabla, column, reg)
    cursor.execute(sql)
    cursor.commit()
    cursor.close()

    
    

    

    