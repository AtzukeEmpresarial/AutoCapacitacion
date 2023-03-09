import pyodbc
import pandas as pd
import openpyxl
import sqlalchemy as sqla
from sqlalchemy import create_engine
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
        engine = create_engine('ibm_db_sa+pyodbc://NSERPOSAD:ATZUKE23@QDSN_NACIONALET01')
        conection = engine.connect()
        return(True)
    except Exception:
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
    except Exception:
        self.login_message = file_message(self,self)
    