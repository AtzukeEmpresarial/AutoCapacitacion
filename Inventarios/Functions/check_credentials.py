import pyodbc
import pandas as pd
import sys
from os import makedirs, path 

def check_credentials (user, password):
    try:
        cnx_nac = pyodbc.connect('DSN=QDSN_MEDELLINET01;UID='+ user +';PWD='+ password, autocommit=True )
        return(True)
    except pyodbc.InterfaceError:
        return(False)
    