from sqlalchemy import create_engine, MetaData
from sqlalchemy import Column, CHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import ibm_db_sa

import sys


"""SE EDITA LA LIBRERIA DE IBM_DB_SA, EL ARCHIVO REFLECTION.
LA CLASE DE AS400 Y DE DB2 ESTABAN INTERCALADAS Y MAL DEFINIDOS
LOS PARAMETROS, ESTE SE ENCUENTRA EN: 
C:\Users\SU_USUARIO\AppData\Local\Programs\Python\Python311\Lib\site-packages\ibm_db_sa"""
try:  
    engine = create_engine(
        'ibm_db_sa+pyodbc://NSERPOSAD:ATZUKE24@QDSN_NACIONALET01;CurrentSchema=CISLIBPR',
        echo = True
    )
    conection = engine.connect()
    print("conexión exitosa")
except Exception:
    print("usuario y/o contraseña no validos")
    sys.exit()
metadata = MetaData(bind=engine)
Base = declarative_base(bind=engine, metadata=metadata)
#tabla de prueba
class Atzuke(Base):
    __tablename__ = "ATZUKE"
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    COMPOPOS = Column(CHAR, nullable = False)
    

    def __init__(self, id, compopos):
        self.ID = id
        self.COMPOPOS = compopos

    def __repr__(self):
        return f"Atzukes({self.ID}, {self.COMPOPOS})"

Base.metadata.create_all(bind = engine)
Session = sessionmaker(bind  =engine)
session = Session()
atzukes = session.query(Atzuke)


for atzuke in atzukes:
    print(atzuke.ID, atzuke.COMPOPOS)


