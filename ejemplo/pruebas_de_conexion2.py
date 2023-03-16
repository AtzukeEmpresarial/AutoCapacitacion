from sqlalchemy import create_engine, text
from sqlalchemy import Column, CHAR, INTEGER,VARCHAR
from sqlalchemy.orm import sessionmaker, declarative_base
from iaccess.dialect import IAccessDialect
import sys

try:  
    engine = create_engine(
        'iaccess+pyodbc://NSERPOSAD:ATZUKE24@QDSN_NACIONALET01',
        isolation_level = "REPEATABLE READ",
        echo=True
    )
    conection = engine.connect()
    print("conexión exitosa")
except Exception:
    print("usuario y/o contraseña no validos")
    sys.exit()

Base = declarative_base()
#tabla de prueba
class Atzuke(Base):
    __tablename__ = "ATZUKE"
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True,autoincrement = True)
    COMPOPOS = Column(CHAR(50), nullable = False)
    def __init__(self, compopos):
        self.COMPOPOS = compopos
    def __repr__(self):
        return (self.COMPOPOS)

atzuke = Atzuke(compopos = "hola")
#Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
session.add(atzuke)
session.commit()
atzukes = session.query(Atzuke)


for atzuke in atzukes:
    print(atzuke.ID, atzuke.COMPOPOS)



