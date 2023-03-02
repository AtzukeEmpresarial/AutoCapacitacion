from sqlalchemy import Column, CHAR, INTEGER, NUMERIC, DATE, DECIMAL
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

#tabla de prueba
class Atzuke(Base):
    __tablename__ = 'ATZUKE'
    ID = Column(INTEGER, primary_key = True)
    COMPOPOS = Column(CHAR)

class Plasticos(Base):
    __tablename__ = 'PLASTICOS'
    ID = Column(INTEGER, primary_key = True)
    CODINV = Column(INTEGER)
    CODFRANQ = Column(INTEGER)
    TIPOTARJETA = Column(CHAR)
    BIN = Column(INTEGER)
    LOGO = Column(INTEGER)
    TIPOPRODUCTO = Column(CHAR)
    CLASE = Column(CHAR)
    NOMBRE = Column(CHAR)
    ACUMULACION = Column(CHAR)
    TIPOREALCE = Column(CHAR)
    OBSERVACIONES = Column(CHAR)
    SEGMENTO = Column(CHAR)
    DESCONTINUADO = Column(NUMERIC)
    CANTIDAD = Column(INTEGER)
    FECHA = Column(DATE)
    IDOPERADOR = Column(INTEGER)

class Franquicias(Base):
    __tablename__ = 'FRANQUICIAS'
    ID = Column(INTEGER, primary_key = True)
    CODIGO = Column(INTEGER)
    NOMBRE = Column(CHAR)
    ACTIVA = Column(NUMERIC)

class Plantas(Base):
    __tablename__ = 'PLANTAS'
    ID = Column(INTEGER, primary_key = True)
    UBICACION = Column(CHAR)
    DESCRIPCION = Column(CHAR)
    IDOPERADOR = Column(INTEGER)
    ACTIVA = Column(NUMERIC)

class Operadores(Base):
    __tablename__ = 'OPERADORES'
    ID = Column(INTEGER, primary_key = True)
    NOMBRE = Column(CHAR)
    DESCRIPCION = Column(CHAR)
    ACTIVA = Column(NUMERIC)

class Movimientos(Base):
    __tablename__ = 'MOVIMIENTOS'
    ID = Column(INTEGER, primary_key = True)
    CODINVPLASTICOS = Column(INTEGER)
    IDPLANTA = Column(INTEGER)
    IDPLANTAFINAL = Column(INTEGER)
    IDTIPOMOV = Column(INTEGER)
    FECHA = Column(DATE)
    CANTIDAD = Column(INTEGER)

class TipoMovimientos(Base):
    __tablename__ = 'TIPOMOVIMIENTOS'
    ID = Column(INTEGER, primary_key = True)
    MOVIMIENTO = Column(CHAR)
    DESCRIPCION = Column(CHAR)

class PedidosTj(Base):
    __tablename__ = 'PEDIDOSTJ'
    ID = Column(INTEGER, primary_key = True)
    IDOPERADOR = Column(INTEGER)
    CODINVPLASTICOS = Column(INTEGER)
    FECHA = Column(DATE)
    TRM = Column(DECIMAL)
    FECHAESTIMADA = Column(DATE)
    CANTIDAD = Column(INTEGER)
    PRECIO = Column(DECIMAL)
    CANTIDADDESP = Column(INTEGER)
    FECHASOPO = Column(DATE)
    IDESTADO = Column(INTEGER)
    VALORAPAGAR = Column(DECIMAL)
    FECHAPAGO = Column(DATE)
    OBSERVACION = Column(CHAR)

class TipoEstados(Base):
    __tablename__ = 'TIPOESTADOS'
    ID = Column(INTEGER, primary_key = True)
    NOMBRE = Column(CHAR)
    DESCRIPCION = Column(CHAR)

class Insumos(Base):
    __tablename__ = 'INSUMOS'
    ID = Column(INTEGER, primary_key = True)
    CUSTODIA = Column(INTEGER)
    RESPONSABLE = Column(CHAR)
    CONTROL = Column(NUMERIC)
    USO = Column(NUMERIC)
    DESCRIPCION = Column(CHAR)

class Danos(Base):
    __tablename__ = 'DANOS'
    ID = Column(INTEGER, primary_key = True)
    CODINVPLASTICOS = Column(INTEGER)
    CANTIDAD = Column(INTEGER)
    FECHA = Column(DATE)