import pyodbc
import pandas as pd
import sys
from os import makedirs, path 




cnx_nac = pyodbc.connect('DSN=QDSN_NACIONALET01;UID=NSERPOSAD;PWD=ATZUKE24', autocommit=True )
sql = '''SELECT * FROM CISLIBPR.{}'''.format("PLASTICOS")
ids_df = pd.read_sql(sql,con = cnx_nac)# type: ignore
cnx_nac.close()# type: ignore
id = ids_df.loc[:,"ID"]
id_list = id.to_list()
index = id_list.index(2)
print(index)