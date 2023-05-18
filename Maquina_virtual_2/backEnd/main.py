## FastAPI
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

## Elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
## Otros

import os
import uvicorn

## conexión DB (mariadb-mysql)
import mysql.connector
from urllib.parse import urlparse

## para variable de enterno
from dotenv import load_dotenv



# ----- Cargar .env ----- #

load_dotenv()

# ----- Variables: Puerto y Origins (cors) ----- #

port = int(os.getenv("PORT"))
origins = [
    os.getenv("URL_FRONT_END")
]


# ----- Variables: Globales ----- #
data = []
list_names = []
list_path = []

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

# =================================================================================================================== #
# ===================================== FUNCIONES PARA RUTAS: FastAPI =============================================== #
# =================================================================================================================== #

# /api/elasticsearch/refresh
def obtainDomainPath(path):
    """
    Obtiene el dominio de un path
    """
    # print("path = ",path)
    parsed_url = urlparse(path)
    domain_name = parsed_url.netloc
    
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    if "." in domain_name:
        domain_name = domain_name[:domain_name.index(".")]
    ##print(domain_name)
    #return domain_name
    return path

# /api/elasticsearch/refresh
def dbCall():
    """
    Carga datos con link y path
    """
    global data
    cursor = conexion.cursor()
    query = "SELECT  link, path FROM  documentos"
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
    global data
    list_names = []
    list_path = []
    data = []
    dbCall()
    
    # data contiene link, path por cada documento
    for i in data:
        nombre_link = obtainDomainPath(i[0])
        list_names.append(nombre_link)
        list_path.append(i[1])


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
                es.get(index=DB_NAME, id=file_name)
                response['already_exists'].append({'file_name':file_name})


            except:
                with open(list_path[i], 'r', encoding='ISO-8859-1')  as f:
                    file_content = f.read()
                    es.index(index=DB_NAME, id=file_name, document={
                        'title': file_name,
                        'content': file_content,
                        'url' : url,
                        'timestamp': datetime.now()
                    })
                    response['successfully_indexed'].append({'file_name':file_name})

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
    return createIndex()

# /api/elasticsearch/refresh:
@app.get("/api/elasticsearch/refresh")
def refreshRoot():
    """
    Refresca los documentos, revisando si hay más elementos por agregar al Elasticsearch
    """
    return refreshIndexes()

# /api/delete:
# @app.get("/api/delete")
# def delete():
#     """
#     Función de testeo para eliminar completamente DB_NAME
#     Está comentado, y que se utilizó para pruebas, pero dejar una ruta así podría ser peligroso. Ya que cualquier persona podría eliminar todo el índice
#     """

#     # Crea una instancia de Elasticsearch
#     es = Elasticsearch(os.getenv("URL_ELASTICSEARCH"))

#     try:
#          es.indices.delete(index=DB_NAME)
#     except:
#         return{"success": False, "message" : "Something went wrong"}

#     return { "success": True, "message": f"DB: {DB_NAME} Successfully deleted"}
    

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

    # --- Si no hay Query ---
    # /api/elasticsearch/search
    # Entonces retorna todos los documentos
    if q is None:
        q = {
            "match_all": {},
        }
       # --- Buscando en el índice DB_NAME ---
        resp = es.search(index=DB_NAME, query=q)
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
        resp = es.search(index=DB_NAME, query=query, highlight=highlight)
        final_resp = []

        # hits.hits <··· Respuestas encontradas en Elasticsearch
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            url = hit['_source']['url']
            content = hit['highlight']['content']
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

    if not link_path_scrapper:
        return  { 'success': False, 'message': 'Something went wrong.'}

    # Si las llaves no corresponden retornamos error
    for clave in link_path_scrapper.keys():
        if (clave != "link_path_scrapper"):
            return  { 'success': False, 'message': 'Something went wrong.'}


    # LINK PATH : /home/alex/Desktop/info288/proyecto/docs_indice_invertido/scraping/esclavo2/data/www.youtube.com_24.txt
    try:
        # Nos conectamos a Mariadb/Mysql 
        link_content = link_path_scrapper['link_path_scrapper']
        cursor_1 = conexion.cursor()
        cursor_1.execute(f"SELECT link FROM documentos WHERE path = '{link_content}'")
        url = cursor_1.fetchone()

        # Se verifica si el url es None o no
        print("url: ", url)
        if url is None:
            print("El elemento no existe en la base de datos")
            return {"success": False, "message": "El elemento no existe en la base de datos"}
        cursor_1.close()

        # Leemos el archivo
        file_name = link_content.split("/")[-1].split(".")[1]

    except Exception as e:
        print("Error: ", e)
        return  { "success": False, "message": "Something went wrong."}

    # Add : maintitle, url, content
    try:
        with open(link_content, 'r', encoding='ISO-8859-1')  as f:
            file_content = f.read()
            es.index(index=DB_NAME, id=file_name, document={
                'title': file_name,
                'content': file_content,
                'url' : url,
            })
            return { "success": True, "message": "Se ha indexado el archivo"}

    except Exception as e:
        print("Error: ", e)
        return { "success": False, "message": "Something went wrong" }

# /api/links
@app.post("/api/links")
async def getLink(link: dict):
    
    if not link:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos")

    

    #####
    hoara_desc = "17:00:00"
    link_final = link["link"]
    print("link: ",link_final)
    query_db = "INSERT INTO documentos (link, hoara_desc) VALUES (%s, %s)"
    values_db = (link_final, hoara_desc)
    cursor.execute(query_db, values_db)
    conexion.commit()

    return JSONResponse(content={"message": link})



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

if __name__ == "__main__":
   
    uvicorn.run(app, host="0.0.0.0", port=port)