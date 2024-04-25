import logging

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from pydantic import BaseModel
from typing import List

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
    number = Column(Integer)
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

    def get_flight_by_number(self, db, flight_number: int) -> Flight:
        flight = db.query(Flight).filter(Flight.number == flight_number).first()
        
        if flight:
            logger.info(f"Vuelo consultado: {flight.number}")
            return flight
        
        raise HTTPException(status_code=404, detail="Flight not found")
    
    def get_reservation_by_number(self, db, reservation_number: int) -> Reservation:
        reservation = db.query(Reservation).filter(Reservation.number == reservation_number).first()
        
        if reservation:
            logger.info(f"Reserva encontrada: {reservation.number}")
            return reservation
        
        raise HTTPException(status_code=404, detail="Reservation not found")

    def make_reservation(self, db, reservation: Reservation) -> Reservation:
        db.add(reservation)
        db.commit()
        logger.info(f"Reserva realizada : {reservation.flight_number} - {reservation.passenger_name}")
        return reservation

flight_system = FlightReservation()


# Definiciones de Modelos y Servicios de FastAPI
class FlightView(BaseModel):
    id: int
    number: int
    departure_city: str
    arrival_city: str
    
class ReservationView(BaseModel):
    id: int
    number: int
    flight_number: str
    passenger_name: str
    seat_number: str
    flight: FlightView
    
class ReservationsResponse(BaseModel):
    reservations: List[ReservationView]
    
app = FastAPI(swagger_ui_parameters={"syntaxHighlight.theme": "obsidian"})

""" Consultar todos los vuelos """
@app.get("/flights/")
async def list_flight(db=Depends(get_db)):
    logging.info("Realizando consulta de todos los vuelos")
    
    query = db.query(Flight).all()
    
    if query is None or not query:
        raise HTTPException(status_code=404, detail="flights not found")
    
    return query 

""" Consultar todos las reservas """
@app.get("/reservations/")
async def list_reservations(db=Depends(get_db)):
    logging.info("Realizando consulta de todos las reservas")    
    query = db.query(Reservation).all()
    
    if query is None or not query:
        raise HTTPException(status_code=404, detail="Reservations not found")
    
    reservations = []
    
    for reservation in query:
        reservation_info = ReservationView(
            flight=FlightView(
                id=reservation.flight.id,
                number=reservation.flight.number,
                departure_city=reservation.flight.departure_city,
                arrival_city=reservation.flight.arrival_city
            ),
            id=reservation.id,
            number=reservation.number,
            passenger_name=reservation.passenger_name,
            seat_number=reservation.seat_number,
            flight_number=reservation.flight_number
        )
        
        reservations.append(reservation_info)
    
    return reservations 

""" Consultar una reserva por su id """
@app.get("/reservations/{number}", response_model=ReservationView)
async def read_reservation(number: int, db=Depends(get_db)):
    logger.info(f"Buscando reserva con: {number}")
    
    return flight_system.get_reservation_by_number(db, number)

""" Crear una reserva """
@app.post("/reservations/", response_model=ReservationView)
async def create_reservation(reservation_data: ReservationView, db=Depends(get_db)):
    logger.info(f"Creando la reserva con info: {reservation_data}")
    
    flight_data = reservation_data.flight
    
    flight = Flight(
        number=flight_data.number,
        departure_city=flight_data.departure_city,
        arrival_city=flight_data.arrival_city
    )
        
    # Crear la nueva reserva
    reservation_data = Reservation(
        flight=flight,
        number=reservation_data.number,
        passenger_name=reservation_data.passenger_name,
        seat_number=reservation_data.seat_number,
        flight_number=reservation_data.flight_number 
    )
    
    # Guardar la nueva reserva en la base de datos
    db.add(reservation_data)
    db.commit()
    db.refresh(reservation_data)
    
    # Devolver la reserva creada
    return reservation_data