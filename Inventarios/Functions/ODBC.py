import pyodbc
import pandas as pd
import sys
import openpyxl
from os import makedirs, path 

def check_credentials (user, password):
    try:
        cnx_nac = pyodbc.connect('DSN=QDSN_MEDELLINET01;UID='+ user +';PWD='+ password, autocommit=True )
        return(True)
    except pyodbc.InterfaceError:
        return(False)

def import_from_excel (path):
    try:
        df_excel = pd.read_excel(path,sheet_name="Feb 06", skiprows= 1)
        return (df_excel)
    except FileNotFoundError:
        print("La dirección es erronea")