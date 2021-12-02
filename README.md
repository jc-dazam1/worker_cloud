# Grupo24_Cloud_Software_Delopment
Repositorio del grupo 24 de MISO

## Integrantes

* Carlos Andrés Echeverri Delgado
* Fabian Andrés Rojas Polania
* Juan Camilo Daza Medina
* William Fernando Sánchez Pulido 

## Ejecución

Las carpetas autorizador_service, convertidor_audio_service, tareas_cola son proyectos de Python independientes, que requieren su propio virtual environment, tienen dependencias cada una y por lo tanto es mejor iniciar un venv por cada carpeta.

Orden de Ejecución (desde una nueva terminal):

- Ejecutar el microservicio de **autorizador** (desde una nueva terminal):

* Acceder a la carpeta `autorizador_service`,
* iniciar el ambiente (previamente creado) con `source ./venv/bin/activate`,
* instalar dependencias con `pip install -r ./requirements.txt`,
* ejecutar flask con `cd autorizador_microserv && flask run --port 5003`

- Ejecutar el microservicio de **convertidor_audio** (desde una nueva terminal):

* Acceder a la carpeta `convertidor_audio_service`,
* iniciar el ambiente (previamente creado) con `source ./venv/bin/activate`,
* instalar dependencias con `pip install -r ./requirements.txt`,
* ejecutar flask con `cd convertidor_audio_microserv && flask run --port 5002`

- Ejecutar el microservicio de **convertidor_cmd** (desde una nueva terminal):

* Acceder a la carpeta `convertidor_cmd_service`,
* iniciar el ambiente (previamente creado) con `source ./venv/bin/activate`,
* instalar dependencias con `pip install -r ./requirements.txt`,
* ejecutar flask con `cd convertidor_cmd_microserv && flask run --port 5000`
* en una nueva terminal ubicarse en el directorio `convertidor_cmd_microserv`
* iniciar la tarea en celery `celery -A tarea_convertidor.tarea_convertidor worker -l info`

- Ejecutar el microservicio de **convertidor_query** (desde una nueva terminal):

* Acceder a la carpeta `convertidor_query_service`,
* iniciar el ambiente (previamente creado) con `source ./venv/bin/activate`,
* instalar dependencias con `pip install -r ./requirements.txt`,
* ejecutar flask con `cd convertidor_query_microserv && flask run --port 5001`

## Para probar alguno de los servicios: 

* ingresa a: [Postman WorkSpace](https://github.com/MISW-4204-ComputacionEnNube/Proyecto-Grupo24-202120/wiki/Postman-Workspace)

