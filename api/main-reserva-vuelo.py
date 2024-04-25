import logging

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel

# Configuración del registro de eventos
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./Reservas.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  
Base = declarative_base()

# Definiciones de Tablas y Base de Datos
class Flight(Base):
    __tablename__ = "vuelo"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    number = Column(Integer)
    departure_city = Column(Text)
    arrival_city = Column(Text)
    
class Reservation(Base):
    __tablename__ = "reserva"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    flight_number = Column(String, ForeignKey('vuelo.number'))
    passenger_name = Column(String)
    seat_number = Column(String)
    flight = relationship("Flight")

# Crea la tabla si no existe
Base.metadata.create_all(bind=engine)

# Operaciones sobre la Base de Datos
def get_db():
    logger.info("Obteniendo sesion de Base de Datos")
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        
class FlightReservation:
    def add_flight(self, db, flight: Flight):
        db.add(flight)
        db.commit()
        logger.info(f"Vuelo agregado : {flight.number}")

    def get_flight_by_number(self, db, flight_number: str) -> Flight:
        flight = db.query(Flight).filter(Flight.number == flight_number).first()
        
        if flight:
            logger.info(f"Vuelo consultado: {flight.number}")
            return flight
        
        raise HTTPException(status_code=404, detail="Flight not found")

    def make_reservation(self, db, reservation: Reservation) -> Reservation:
        db.add(reservation)
        db.commit()
        logger.info(f"Reserva realizada : {reservation.flight_number} - {reservation.passenger_name}")
        return reservation

flight_system = FlightReservation()


# Definiciones de Modelos y Servicios de FastAPI
class FligthView(BaseModel):
    id: int
    number: str
    departure_city: str
    arrival_city: str
    
app = FastAPI()

@app.get("/flights/")
async def list_flight(db=Depends(get_db)):
    logging.info("Realizando consulta de todos los vuelos")
    
    query = db.query(Flight).all()
    
    if query is None or not query:
        raise HTTPException(status_code=404, detail="flights not found")
    
    return query 

