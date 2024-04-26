# MASTER-FAST_API-TASK

**Autor**: Javier Llinares

**Comentarios**: Para simplicidad de la tarea la relacion entre el vuelo y la reserva se mantuvo simple, dandole mas importancia al objeto relacionado con la misma reserva.


------------

### Proyecto y Dockerizacion

Se anexa la evidencias que el proyecto se ejecuta con sus correspondientes contenedor, adicionalmente se ejecuta tambien con la orquestación desde kubernetes

![Imagen Docker](images/Prueba_Ejecucion_Docker.png?raw=true)


![Imagen Docker](images/Prueba_Push_DockerHub.png?raw=true)


![Imagen Docker](images/Prueba_Proceso_FastAPI.png?raw=true)


![Imagen Docker](images/Prueba_Dockerhub.png?raw=true)


![Imagen Kubernetes](images/Prueba_Kubernetes.png?raw=true)


![Imagen Llamado Kubernetes](images/Prueba_Kubernetes_Llamados.png?raw=true)


![Imagen Llamado BD](images/Prueba_Base_de_Datos.png?raw=true)



------------

### Pruebas Postman



**Path base del API**: http://127.0.0.1:7070/


![Imagen Swagger](images/Prueba_Swagger.png?raw=true)


------------


**Prueba de Listado de vuelos (GET):** http://127.0.0.1:7070/flights
**Data de prueba:**
```bash
curl --location 'http://127.0.0.1:7070/flights' \
--header 'Accept: application/json'
```

![Imagen Llamado](images/Prueba_Listado_Vuelos.png?raw=true)

------------


**Prueba de Listado de reservas (GET):** http://127.0.0.1:7070/reservations
**Data de prueba:**
```bash
curl --location 'http://127.0.0.1:7070/reservations' \
--header 'Accept: application/json'
```

![Imagen Llamado](images/Prueba_Listado_Reservas.png?raw=true)

------------
**Prueba de creación de reserva (POST):** http://127.0.0.1:7070/reservations
**Data de prueba:**
```bash
curl --location 'http://127.0.0.1:7070/reservations' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
  "id": 2,
  "number": 2,
  "flight_number": 2,
  "passenger_name": "Ida Pitti",
  "seat_number": "Ventana Izquierda",
  "flight": {
    "id": 2,
    "number": 2,
    "departure_city": "COSTA RICA",
    "arrival_city": "SALVADOR"
  }
}'
```


![Imagen Llamado](images/Prueba_Crear_Reserva.png?raw=true)

------------

**Prueba de consulta de reserva por su ID (GET):** http://127.0.0.1:7070/reservations/{id}
**Data de prueba:**
```bash
curl --location 'http://127.0.0.1:7070/reservations/2' \
--header 'Accept: application/json'
```

![Imagen Llamado](images/Prueba_Consultar_Reserva.png?raw=true)

------------

**Prueba de actualizacion de reserva por su ID (PUT):** http://127.0.0.1:7070/reservations/{id}
**Data de prueba:**
```bash
curl --location --request PUT 'http://127.0.0.1:7070/reservations/2' \
--header 'Content-Type: application/json' \
--header 'Accept: application/json' \
--data '{
  "passenger_name": "Piedad Carrillo",
  "seat_number": "Salida de Emergencia"
}'
```

![Imagen Llamado](images/Prueba_Actualizar_Reversa.png?raw=true)


------------

**Prueba de borrado de cliente por su ID (DELETE):**
http://127.0.0.1:7070/reservations/{id}?reservation_id={id}
**Data de prueba:**
```bash
curl --location --request DELETE 'http://127.0.0.1:7070/reservations/2?reservation_id=2' \
--header 'Accept: application/json'
```

![Imagen Llamado](images/Prueba_Eliminacion_Reserva.png?raw=true)


------------


