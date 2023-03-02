from sqlalchemy import create_engine
from sqlalchemy import Column, CHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import sys

try:  
    engine = create_engine('ibm_db_sa+pyodbc://NSERPOSAD:ATZUKE24@QDSN_NACIONALET01', database = "NACIONAL")
    conection = engine.connect()
    print("conexión exitosa")
except Exception:
    print("usuario y/o contraseña no validos")
    sys.exit()

Base = declarative_base()
#tabla de prueba
class Atzuke(Base):
    __tablename__ = "ATZUKE"
    ID = Column(INTEGER, primary_key = True)
    COMPOPOS = Column(CHAR, nullable = False)

    def __init__(self, ID, COMPOPOS):
        self.ID = ID
        self.COMPOPOS = COMPOPOS

    def __repr__(self):
        return f"Atzukes({self.ID}, {self.COMPOPOS})"

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
atzukes = session.query(Atzuke)


for atzuke in atzukes:
    print(atzuke.ID, atzuke.COMPOPOS)


