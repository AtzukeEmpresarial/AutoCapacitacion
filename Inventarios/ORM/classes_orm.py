from sqlalchemy import Column, CHAR, INTEGER, NUMERIC, DATE, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#tabla de prueba
class Atzuke(Base):
    __tablename__ = 'ATZUKE'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    COMPOPOS = Column(CHAR)

class Plasticos(Base):
    __tablename__ = 'PLASTICOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    CODINV = Column(INTEGER,nullable = False)
    CODFRANQ = Column(INTEGER,nullable = False)
    TIPOTARJETA = Column(CHAR,nullable = False)
    BIN = Column(INTEGER,nullable = False)
    LOGO = Column(INTEGER)
    TIPOPRODUCTO = Column(CHAR)
    CLASE = Column(CHAR,nullable = False)
    NOMBRE = Column(CHAR,nullable = False)
    ACUMULACION = Column(CHAR)
    TIPOREALCE = Column(CHAR)
    OBSERVACIONES = Column(CHAR)
    SEGMENTO = Column(CHAR)
    DESCONTINUADO = Column(NUMERIC,nullable = False)
    CANTIDAD = Column(INTEGER,nullable = False)
    FECHA = Column(DATE,nullable = False)
    IDOPERADOR = Column(INTEGER,nullable = False)

class Franquicias(Base):
    __tablename__ = 'FRANQUICIAS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    CODIGO = Column(INTEGER,nullable = False)
    NOMBRE = Column(CHAR,nullable = False)
    ACTIVA = Column(NUMERIC,nullable = False)

class Plantas(Base):
    __tablename__ = 'PLANTAS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    UBICACION = Column(CHAR,nullable = False)
    DESCRIPCION = Column(CHAR)
    IDOPERADOR = Column(INTEGER,nullable = False)
    ACTIVA = Column(NUMERIC,nullable = False)

class Operadores(Base):
    __tablename__ = 'OPERADORES'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    NOMBRE = Column(CHAR,nullable = False)
    DESCRIPCION = Column(CHAR)
    ACTIVA = Column(NUMERIC,nullable = False)

class Movimientos(Base):
    __tablename__ = 'MOVIMIENTOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    CODINVPLASTICOS = Column(INTEGER,nullable = False)
    IDPLANTA = Column(INTEGER,nullable = False)
    IDPLANTAFINAL = Column(INTEGER,nullable = False)
    IDTIPOMOV = Column(INTEGER,nullable = False)
    FECHA = Column(DATE,nullable = False)
    CANTIDAD = Column(INTEGER,nullable = False)

class TipoMovimientos(Base):
    __tablename__ = 'TIPOMOVIMIENTOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    MOVIMIENTO = Column(CHAR,nullable = False)
    DESCRIPCION = Column(CHAR)

class PedidosTj(Base):
    __tablename__ = 'PEDIDOSTJ'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    IDOPERADOR = Column(INTEGER,nullable = False)
    CODINVPLASTICOS = Column(INTEGER,nullable = False)
    FECHA = Column(DATE,nullable = False)
    TRM = Column(DECIMAL,nullable = False)
    FECHAESTIMADA = Column(DATE,nullable = False)
    CANTIDAD = Column(INTEGER,nullable = False)
    PRECIO = Column(DECIMAL,nullable = False)
    CANTIDADDESP = Column(INTEGER)
    FECHASOPO = Column(DATE,nullable = False)
    IDESTADO = Column(INTEGER,nullable = False)
    VALORAPAGAR = Column(DECIMAL,nullable = False)
    FECHAPAGO = Column(DATE)
    OBSERVACION = Column(CHAR)

class TipoEstados(Base):
    __tablename__ = 'TIPOESTADOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    NOMBRE = Column(CHAR,nullable = False)
    DESCRIPCION = Column(CHAR,nullable = False)

class Insumos(Base):
    __tablename__ = 'INSUMOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    CUSTODIA = Column(INTEGER,nullable = False)
    RESPONSABLE = Column(CHAR,nullable = False)
    CONTROL = Column(NUMERIC,nullable = False)
    USO = Column(NUMERIC,nullable = False)
    DESCRIPCION = Column(CHAR,nullable = False)

class Danos(Base):
    __tablename__ = 'DANOS'
    __table_args__ = {"schema": "CISLIBPR"}
    ID = Column(INTEGER, primary_key = True)
    CODINVPLASTICOS = Column(INTEGER,nullable = False)
    CANTIDAD = Column(INTEGER,nullable = False)
    FECHA = Column(DATE,nullable = False)