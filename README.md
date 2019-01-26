# fifabus
fifabus info

# instalacion

clonar el proyecto

entrar en la carpeta frontfifa

Run `npm install`

Run `ng serve --proxy-config proxy.config.json`

Run `cd venv && source bin/activate`

(venv) $ pip install -r requirements.txt

`python app.py`

# API Documentation

- POST **/api/login**

realizar el login de los usuarios registrados
el body contiene JSON object con username y password
si el usuario no existe o la clave no concuerda retorna error 401

- POST **/api/users**

realisar el registro de usuarios nuevos
el body contiene JSON object con username y password
si el usuario existe o no hay data de username y password retorna error 401

- GET **/api/users**

retorna el total de jugadores registrados
agregar en el header `x-access-token` el token para consumir el servicio

- GET **/api/players/old**

retorna el jugador mas viejo registrado
agregar en el header `x-access-token` el token para consumir el servicio

- GET **/api/players/young**

retorna el jugador mas joven registrado
agregar en el header `x-access-token` el token para consumir el servicio

- GET **api/players/alternate**

retorna los jugadores que no son titulares
agregar en el header `x-access-token` el token para consumir el servicio

- GET **/api/players/avgalter**

retorna el promedio de jugadores por equipo
agregar en el header `x-access-token` el token para consumir el servicio

- POST **/api/players**

salva los datos de los jugadores del campeonato
agregar en el header `x-access-token` el token para consumir el servicio
el form con los datos de los jugadores
NombreEquipo
Nombre
Apellido
Fecha de nacimiento
Posición en la que juega
Número de camiseta
titular (True,False)

- POST **/api/coachs**

salva los datos del cuerpo tecnico
agregar en el header `x-access-token` el token para consumir el servicio
NombreEquipo
Nombre
Apellido
Fecha de nacimiento
Nacionalidad
Rol (técnico|asistente|médico|preparador)

- POST **/api/teams**

salvar los datos del equipo
agregar en el header `x-access-token` el token para consumir el servicio
Nombre del Equipo
Imagen de Bandera
Escudo del Equipo
pais

- GET **/api/temas**

retorna los equipos registrados
agregar en el header `x-access-token` el token para consumir el servicio

- GET **/api/country**

retorna nombre de los paises
agregar en el header `x-access-token` el token para consumir el servicio
