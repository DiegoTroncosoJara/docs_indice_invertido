# Todas las config de puertos

## Máquina virtual 1 (Frontend)

```env
VITE_PORT= 3000
```
- VITE_PORT: Puerto en el que se alojará el servidor de Frontend

## Máquina virtual 2 (Backend)

```env
## Información
PORT = 8000

## Información de los esclavos 
ESCLAVOS_quantity=3
URL_ESCLAVO_0 = "http://localhost:4001/"
URL_ESCLAVO_1 = "http://localhost:4002/"
URL_ESCLAVO_2 = "http://localhost:4003/"

## Información sobre el FrontEnd
URL_FRONT_END = "http://localhost:3000"

## Información del Elasticsearch
URL_ELASTICSEARCH = "http://localhost:9200"

## Información de la base de datos 
USER_DB = 'root'
PASSWORD_DB = ''
HOST_DB = "localhost"
PORT_DB = 3306
DATA_BASE = "documentos"

#Log de los endpoints
LOG_PATH="log/ServerLog.log"
```

### Puertos internos

- PORT: Puerto en donde está el servicio de Backend 

### Variables que interactúan con esclavos

- ESCLAVOS_quantity: Cantidad esperada de esclavos
- URL_ESCLAVO_0: Url del esclavo 0
- URL_ESCLAVO_1: Url del esclavo 1
- URL_ESCLAVO_2: Url del esclavo 2

### Variables que interactúan con Frontend

- URL_FRONT_END: Url en donde está ubicado el Frontend, se utiliza para conflictos de cors.


### Variables que interactúan con Elasticsearch

- URL_ELASTICSEARCH: Url en donde está ubicado el proceso de Elasticsearch, se utiliza para la conexión y creación del índice invertido.

### Variables que interactúan con Base de Datos

- USER_DB: Usuario mysql, ej: `root`
- PASSWORD_DB: Contraseña del usuario mysql, ej : `123456`
- HOST_DB: Dirección de donde está la base de datos, ej: `localhost`
- PORT_DB: Puerto en donde está la base de datos, ej: `3306`
- DATA_BASE: Nombre de la base de datos utilizada, ej: `documentos`

### Variables que interactúan con Logs

- LOG_PATH: Path en donde están los Logs, se utiliza para visualizar registros en caso de peticiones o falla.

## Máquina virtual 3 (Base de datos)

## Máquina virtual 4 (Master Scrapper)

```env
## información de los esclavos 
URL = "0.0.0.0"
ESCLAVOS_quantity  =3
URL_ESCLAVO_0 = "http://localhost:4001/"
URL_ESCLAVO_1 = "http://localhost:4002/"
URL_ESCLAVO_2 = "http://localhost:4003/"


## Información de la base de datos 
USER_DB = 'root'
PASSWORD_DB = ''
HOST_DB = "localhost"
PORT_DB = 3306
DATA_BASE = "documentos"

## Información del back-end

URL_BACK_END = "http://0.0.0.0:8000"
```
### URL interna

- URL: Url base en donde está el Master.

### Variables que interactúan con esclavos

- ESCLAVOS_quantity: Cantidad esperada de esclavos
- URL_ESCLAVO_0: Url del esclavo 0
- URL_ESCLAVO_1: Url del esclavo 1
- URL_ESCLAVO_2: Url del esclavo 2

### Variables que interactúan con Base de Datos
- USER_DB: Usuario mysql, ej: `root`
- PASSWORD_DB: Contraseña del usuario mysql, ej : `123456`
- HOST_DB: Dirección de donde está la base de datos, ej: `localhost`
- PORT_DB: Puerto en donde está la base de datos, ej: `3306`
- DATA_BASE: Nombre de la base de datos utilizada, ej: `documentos`

### Variables que interactúan con Backend
- URL_BACK_END: Url en donde está ubicado el Backend.

## Máquina virtual 5.0 (Slave Scrapper)

**Configuración por cada esclavo**

```env
HOST = '0.0.0.0'
PORT_SLAVE = 4002
```

- HOST: Host en donde está el esclavo.
- PORT_SLAVE: Puerto en el que está el esclavo.
