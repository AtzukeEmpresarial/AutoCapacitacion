import pyodbc
import pandas as pd
import openpyxl
from os import makedirs, path 
from Screens.file_message import file_message

def check_credentials (user, password):
    """
    Función que se encarga de verificar si un usuario existe 
    en el sistema de Nacional o Medellín segun se configure,
    a esta función entran:
    user = Usuario.
    password = Contraseña del usuario.
    """
    try:
        cnx_nac = pyodbc.connect('DSN=QDSN_MEDELLINET01;UID='+ user +';PWD='+ password, autocommit=True )
        return(True)
    except pyodbc.InterfaceError:
        return(False)

def import_from_excel (self, path):
    """
    Función que se encarga de importar los datos de un excel
    a un formato que le pueda dar uso Pandas, esta función recibe:
    path = dirección o ruta del archivo excel.
    """
    try:
        df_excel = pd.read_excel(path,sheet_name="Feb 06", skiprows= 1)
        return (df_excel)
    except FileNotFoundError:
         self.login_message = file_message(self,self)