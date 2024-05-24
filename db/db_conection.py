from sqlalchemy import create_engine, Column, String, Integer, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Estadia(Base):
    __tablename__ = 'estadias'
    id_estadia = Column(Integer, primary_key=True)
    numero_habitacion = Column(String(20))
    tipo_habitacion = Column(String(20))
    costo = Column(Integer)
    dias_estadia = Column(Integer)
    descuento = Column(Integer)
    sub_total = Column(Integer)
    total = Column(Integer)
    forma_de_pago = Column(String(10))
    state = Column(String(10))

class Habitacion(Base):
    __tablename__ = 'habitaciones'
    id_habitacion = Column(Integer, primary_key=True)
    tipo = Column(String(20))
    costo = Column(Integer)


def start_connection():
    engine = create_engine(
        "mysql+pymysql://root@localhost/hotel_db"
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

#! Octener la suma de ingresos totales por tipo de abitacion:
def get_total_finalizado(tipo_habitacion):
    session = start_connection()
    total = session.query(func.sum(Estadia.total)).filter(
        Estadia.state == 'finalizado',
        Estadia.tipo_habitacion == tipo_habitacion
    ).scalar()
    session.close()
    return total if total else 0