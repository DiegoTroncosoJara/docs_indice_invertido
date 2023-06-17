## FastAPI
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

## Elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
## Otros
import requests
import os
import uvicorn
import zipfile


#Logs
import logging
from logging import handlers
import time


import random 
from apscheduler.schedulers.background import BackgroundScheduler
## conexión DB (mariadb-mysql)
import mysql.connector
from urllib.parse import urlparse

## para variable de enterno
from dotenv import load_dotenv

## funciones 
from helpers.helper import obtener_dominio_raiz , obtainDomainPath, SeparaLink
#
# ----- Cargar .env ----- #
load_dotenv()

# ----- Variables: Puerto y Origins (cors) ----- #

port = int(os.getenv("PORT"))
origins = [
    os.getenv("URL_FRONT_END"),
    "localhost"
]


# ----- Variables: Globales ----- #
data = []
list_names = []
list_path = []
list_id = []
SLAVES = {}

# ----- Conexión: DB MariaDB/Mysql ----- #
conexion = mysql.connector.connect(
    host=os.getenv("HOST_DB"),
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATA_BASE")
)
cursor = conexion.cursor()

# ----- Inicializar FastAPI junto a CORS ----- #

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Conexión: ELasticsearch ----- #
es = Elasticsearch(os.getenv("URL_ELASTICSEARCH"))
DB_NAME = 'db_scrapper'


# ----- Path del log ----- #
log_path = os.getenv("LOG_PATH")


# =================================================================================================================== #
# ========================================== LOGICA PARA EL PATH ==================================================== #
# =================================================================================================================== #

# Crear un objeto de log
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Crear un manejador para escribir en el archivo de log
log_file = log_path
file_handler = handlers.RotatingFileHandler(log_file, maxBytes=1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)

# Formateador para el log
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)

# Agregar el manejador al objeto de log
logger.addHandler(file_handler)

# ----- Funcion para crear logs ----- #

def log(text):
    current_time = int(time.time())
    """ 
    Registrar un mensaje con el tiempo UNIX
    El formato es: TiempoEnUnix;Referencia_log
    EJ: 1686363931;ObtainDomainPath
    """
    logger.debug(f'{current_time};{text}')


####  ------------------------------------------------------------------------------------


##inicializa un diccionario  con los esclavos disponibles. 
def GetUrlSlaves(): 
    global SLAVES
    slaves_quantity = int((os.getenv("ESCLAVOS_quantity")))
    for i in range(slaves_quantity):
        aux = os.getenv("URL_ESCLAVO_{}".format(str(i)))
        SLAVES[str(i)] = aux
            


## retorna alatoriamente un esclavo para ir a buscar un link para hacer un scraping
def RandomSlave():
    num = random.randint(0,len(SLAVES)-1)
    #return "http://127.0.0.1:4001/getlink"
    return SLAVES[str(num)] + "getlink" 



# verifica si el link ya esta en la base de datos 
def CheckLinkDb(link): 
    query_select = f"SELECT * FROM documentos WHERE link = '{link}'"
    cursor.execute(query_select)
    resultado = cursor.fetchone()
    
    if resultado is not None:
        return True, resultado[0]
    else:
        return False, None


##agrega un link a la base de datos con su hora para realizar scraping. 
def enterDbLink(link, id_link_parent):
    hora_desc = datetime.now().strftime("%H:%M:%S")
    query_db = "INSERT INTO documentos (link, hoara_desc, id_url_dependient) VALUES (%s, %s, %s)"
    values_db = (link, hora_desc, id_link_parent)
    cursor.execute(query_db, values_db)
    conexion.commit()


def  verifylinkparentDb(url):
    check, id = CheckLinkDb(url)
    ##ver su url raiz 
    if(check): 
        return id 
    else: 
        return None 


### trae un link de los distintos scrapeer 
def goFindLink():
    url = RandomSlave()
    response = requests.get(url);
    if response.status_code == 200:
        result = response.json()
        if (result["status"] == "ok"): 
            result = result["link"]
            result = SeparaLink(result)

            return result , True
        else: 
            return [], False 
    else: 
        print("error de conexion... ")
        

# funcion que inicia  el proceso de traer un link 
def algorithmInsertLinkScraping():
    os.system("clear")
    print("desde aca")
    link , conditional = goFindLink()
    print(conditional)
    print(link)
    try:
        if(len(link)!=0):
            check, id= CheckLinkDb(link[0])
            print(check)
            print(conditional)
            if(check!= True and conditional): 
                print("pasa por aca para agregar...  ")
                id_link_parent = verifylinkparentDb(link[1])
                enterDbLink(link[0],id_link_parent)
            elif((check== False )and (conditional != False)):
                print("hola")
                ##algorithmInsertLinkScraping()
                pass 
            else:
                print("hola viendo que cae en el else... .")
            ## algorithmInsertLinkScraping()
        else:
            print("no quedan mas link.....")
    except Exception as e  :
        print("Error:", str(e))
####--------------------------------------------------------------------------------####


# =================================================================================================================== #
# ===================================== FUNCIONES PARA RUTAS: FastAPI =============================================== #
# =================================================================================================================== #



# /api/elasticsearch/refresh
def dbCall():
    """
    Carga datos con link y path
    """

    global data
    cursor = conexion.cursor()
    query = "SELECT  link, path , id_esclavo FROM  documentos"
    cursor.execute(query)
    data = cursor.fetchall()
    ##data = [elemento for dupla in datos for elemento in dupla]

# /api/elasticsearch/refresh
def initializeGlobalData():
    """
    Carga los datos para list_names, list_path y datos
    Información para verificar que está todo cargado y listo
    """
    global list_names
    global list_path
    global list_id
    global data
    list_names = []
    list_path = []
    list_id = []
    data = []
    dbCall()
    
    # data contiene link, path por cada documento
    for i in data:
        nombre_link = obtainDomainPath(i[0])
        list_names.append(nombre_link)
        list_path.append(i[1])
        list_id.append(i[2])

## obtienen el contenido del url, mediante una petición al  esclavo designado. 
def bringDataFile(file_path, id_slave):
    
        url = "{}leer".format(SLAVES[str(id_slave)])
        response = requests.post(url, json={
            "file_path" : file_path
        })

        if response.status_code == 200:
            result = response.json()
            result = result["content"]
            return result
            

def DbCallByPath(path):
    cursor_2 = conexion.cursor()
    url = ""
    try:
        cursor_2.execute(f"SELECT link, id_esclavo FROM documentos WHERE path = '{path}'")
        url = cursor_2.fetchone()
        cursor_2.close()  # Cerrar el cursor después de leer el resultado
    except Exception as e:
        print("Error:", str(e))
        cursor_2.close()
    return url

    

# =================================================================================================================== #
# ============================================== Funciones para elasticsearch =======================================#
# =================================================================================================================== #

# /api/elasticsearch/create
def createIndex():
    """
    Crea el índice "DB_NAME"
    Si ya está creado, devuelve los documentos que hay
    """

    try:
        es.indices.create( # ···> Solo debe ejecutarse una vez
            index=DB_NAME, # ···> DB_NAME
            settings={
                "index": {
                    "highlight": {
                        "max_analyzed_offset": 2_000_000 # <--- Esto es para limitar el tamaño del highlight
                    }
                }
            }
        )
        print('Index created')
        return { 'success': True, 'message': 'Index DB created' }

    except Exception as e:
        print('Index already exists')
        try: 
            q = {"match_all": {}} # ···> Query to get all documents
            result = es.search(index=DB_NAME, query=q)
            current_documents = []
            for hit in result['hits']['hits']:
                doc_info = {
                    'id': hit['_id'],
                    'title': hit['_source']['title'],
                }
                current_documents.append(doc_info)

            print('Current documents: ', current_documents)

            return { 'success': False, 'message': f'Index DB: {DB_NAME} already exists', 'current_documents': current_documents}
        except Exception as e:
            print('Error: ', e)
            return { 'success': False, 'message': 'Something went wrong' }

# /api/elasticsearch/refresh
def refreshIndexes():
    """
        Refresca los índices, comparativa que hace utilizando la base de datos.    
    """ 
    
    global list_names
    global list_path
    global list_id
    initializeGlobalData()

    response = {
        'already_exists': [],
        'successfully_indexed': []
    }

    try:
        for i in range(len(list_path)):

            file_name = list_names[i]
            url = data[i][0]
            try:
                es.get(index=DB_NAME, id=url)
                # Si el indexamiento es exitoso Comprimir el contenido del archivo
                ##compressFile(list_path[i])

                response['already_exists'].append({'file_name':file_name})


            except:
                file_content = bringDataFile(list_path[i], list_id[i])
                es.index(index=DB_NAME, id=url, document={
                        'title': file_name,
                        'content': file_content,
                        'url' : url,
                        'timestamp': datetime.now()
                })
                response['successfully_indexed'].append({'file_name':file_name})
                # test compresion archivo


        response['success'] = True
        return  response

    except Exception as e:
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong' }


# =================================================================================================================== #
# ============================================== RUTAS: FastAPI ===================================================== #
# =================================================================================================================== #

# /api/elasticsearch/create:
@app.get("/api/elasticsearch/create")
def createRoot():
    """
    En Elasticsearch se crean los índices (DB_NAME = 'db_scrapper')
    Si ya existe el índice, entonces retorna los documentos actuales
    """

    #Agregar en el log la ruta
    log("crea_indices")  


    return createIndex()

# /api/elasticsearch/refresh:
@app.get("/api/elasticsearch/refresh")
def refreshRoot():
    """
    Refresca los documentos, revisando si hay más elementos por agregar al Elasticsearch
    """
    #Agregar en el log la ruta
    log("refresca_documentos") 

    return refreshIndexes()

# /api/delete:
@app.get("/api/delete")
def delete():
    """
    Función de testeo para eliminar completamente DB_NAME
    Está comentado, y que se utilizó para pruebas, pero dejar una ruta así podría ser peligroso. Ya que cualquier persona podría eliminar todo el índice
    """

     #Agregar en el log la ruta
    log("elimina_DB_NAME") 

    # Crea una instancia de Elasticsearch
    es = Elasticsearch(os.getenv("URL_ELASTICSEARCH"))

    try:
         es.indices.delete(index=DB_NAME)
    except:
        return{"success": False, "message" : "Something went wrong"}

    return { "success": True, "message": f"DB: {DB_NAME} Successfully deleted"}
    

# /api/elasticsearch/search
# /api/elasticsearch/search?q={query}
@app.get("/api/elasticsearch/search")
def searchRoot(q: str = Query(None, min_length=3, max_length=50)):
    """
    Buscar elementos en Elasticsearch (documentos obtenidos por scrapper)
    Params:
        Largo míninmo 3, Largo máximo 50
        q: str | None
        return: documentos
    """

    #Agregar en el log la ruta
    log("busqueda_en_documentos") 
    ssize = 30 
    # --- Si no hay Query ---
    # /api/elasticsearch/search
    # Entonces retorna todos los documentos
    if q is None:
        q = {
            "match_all": {},
        }
       # --- Buscando en el índice DB_NAME ---
        resp = es.search(index=DB_NAME, query=q, size= ssize)
        final_resp = []
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            url = hit['_source']['url']
            content = hit['_source']['content']

            # maintitle = title.split(".")[1]
            temp = { 'maintitle': title, 'link': url, 'content': content}
            final_resp.append(temp)
            # print(final_resp)
        # Return full response
        encoded_item = jsonable_encoder({ 'success': True, 'data': final_resp })
        return encoded_item

    # --- Si hay Query ---
    # /api/elasticsearch/search?q={query}
    # Entonces retorna los documentos coincidentes

    try:
        # NOTA: 'content' es el campo que queremos buscar en el índice de Elasticsearch (campo que nosotros creamos)
        # query: Es el query que queremos buscar
        query = {
            "match": {
                "content": q,
            },
        }

        # highlight: Es la parte que queremos 'destacar'
        highlight = {
            "fields": {
                "content": {
                    "type": "unified",
                },
            },
        }

        # --- Buscando en el índice DB_NAME ---
        resp = es.search(index=DB_NAME, query=query, highlight=highlight , size=ssize )
        final_resp = []

        # hits.hits <··· Respuestas encontradas en Elasticsearch
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            url = hit['_source']['url']
            content = hit['highlight']['content']
            content = content[:500]
            # maintitle = title.split(".")[1]
            temp = { 'maintitle': title, 'link': url, 'content': content}
            final_resp.append(temp)
        encoded_item = jsonable_encoder({ 'success': True, 'data': final_resp })
        return encoded_item

    except Exception as e:
        encoded_item = jsonable_encoder({ 'success': False, 'message': 'Something went wrong. Try adding a query ex: <search?q=audifonos>' })
        return encoded_item


# /api/elasticsearch/link_path_scrapper
@app.post("/api/elasticsearch/link_path_scrapper")
async def addLinkPath(link_path_scrapper: dict):
    """
    Agregar links dado un path.
    Esta solicitud está pensada para los scrappers  
    Entrada esperada ej:
    {
        "link_path_scrapper":"/home/alex/Desktop/info288/proyecto/docs_indice_invertido/scraping/esclavo2/data/www.youtube.com_24.txt"
    }
    """

    #Agregar en el log la ruta
    log("agrega_links_por_path") 

    print(link_path_scrapper)
    if not link_path_scrapper:
        return  { 'success': False, 'message': 'Something went wrong.'}

    # Si las llaves no corresponden retornamos error
    for clave in link_path_scrapper.keys():
        if (clave != "link_path_scrapper"):
            return  { 'success': False, 'message': 'Something went wrong.'}
    

    path = link_path_scrapper['link_path_scrapper']
    
    url = DbCallByPath(path)   
    if(url!=""):
        try:
            # Nos conectamos a Mariadb/Mysql 
            
            print(path)
            # Se verifica si el url es None o no
            print("url: ", url)
            if url is None:
                print("El elemento no existe en la base de datos")
                return {"success": False, "message": "El elemento no existe en la base de datos"}
        
            
            file_name = obtainDomainPath(url[0])
            print(file_name)
            
            file_content = bringDataFile(path, url[1])
            print(file_content[:1])
        
        except Exception as e:
            
            print("Error: ", e)
            print("el error esta aca.. ")
            return  { "success": False, "message": "Something went wrong."}

        # Add : maintitle, url, content
        try:
            
                
                es.index(index=DB_NAME, id=url[0], document={
                    'title': file_name,
                    'content': file_content,
                    'url' : url[0],
                })
                return { "success": True, "message": "Se ha indexado el archivo"}

        except Exception as e:
            print("Error: ", e)
            return { "success": False, "message": "Something went wrong" }

###------------------------------------------------------------------------

# /api/links
@app.post("/api/links")
async def getLink(link: dict):
    
    #Agregar en el log la ruta
    log("consigue_links") 

    if not link:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos")

    link_final = link["link"]
    check, link = CheckLinkDb(link_final)
    if(check!=True):
        enterDbLink(link_final,None)
        return JSONResponse(content={"status": "success", "message": "El link se registró correctamente." })
    else:
        return JSONResponse(content={"status" : "error" ,"message": "El link ya está registrado."})



# =================================================================================================================== #
# ===================================================== MAIN ======================================================== #
# =================================================================================================================== #

# ASI SE EJECUTA :  se envia como json en un body

# {
#     "link": "https://www.example.com"
# }
    
#     ##refreshIndexes()

#     uvicorn.run(app, host="0.0.0.0", port=8000)
 
# ==


    ##print("hola probando el minuto")


if __name__ == "__main__":


    GetUrlSlaves()
    initializeGlobalData()


    if(1): 
        #Crear un objeto scheduler
        scheduler = BackgroundScheduler()

        # Agregar la tarea al scheduler
        scheduler.add_job(algorithmInsertLinkScraping, 'interval', minutes=1)

        # Iniciar el scheduler
        scheduler.start()

        try:
            # Mantener el backend en ejecución
            uvicorn.run(app, host=os.getenv("HOST") , port=port)
        except (KeyboardInterrupt, SystemExit):
            # Detener el scheduler cuando se recibe una señal de interrupción o salida del sistema
            scheduler.shutdown()
            scheduler.start()


        

