from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Estadia(Base):
    __tablename__ = "estadias"
    id_estadia = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer)
    tipo = Column(String(20))
    costo = Column(Integer)
    dias_estadia = Column(Integer)
    forma_de_pago = Column(String(20))
    estado = Column(String(20))


def start_connection():
    engine = create_engine(
        "mysql+pymysql://root@localhost/hotel_db"
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()