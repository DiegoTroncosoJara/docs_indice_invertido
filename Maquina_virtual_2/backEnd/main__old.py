# FastAPI
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import JSONResponse


from fastapi.encoders import jsonable_encoder

from fastapi.middleware.cors import CORSMiddleware

# Elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
# Others
import os
import glob
import uvicorn
##db conexion
import mysql.connector
from urllib.parse import urlparse

## para variable de enterno
from dotenv import load_dotenv



##----------------------------------------------------------------#
##funcion que permite leer el archivo .env 
load_dotenv()

port = int(os.getenv("PORT"))
origins = [
    os.getenv("URL_FRONT_END")
]


datos = []
lista_nombres = []
lista_path = []
conexion = mysql.connector.connect(
    host=os.getenv("HOST_DB"),
    user=os.getenv("USER_DB"),
    password=os.getenv("PASSWORD_DB"),
    database=os.getenv("DATA_BASE")
)
cursor = conexion.cursor()

#
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

es = Elasticsearch(os.getenv("URL_ELASTICSEARCH"))
DB_NAME = 'db_scrapper'




def obtener_dominio(path):
    print("path = ",path)
    parsed_url = urlparse(path)
    domain_name = parsed_url.netloc
    
    if domain_name.startswith("www."):
        domain_name = domain_name[4:]

    if "." in domain_name:
        domain_name = domain_name[:domain_name.index(".")]
    ##print(domain_name)
    #return domain_name
    return path

def llamada_base_datos():
    global datos
    cursor = conexion.cursor()

    consulta = "SELECT  link, path FROM  documentos"
    cursor.execute(consulta)

    datos = cursor.fetchall()
    ##datos = [elemento for dupla in datos for elemento in dupla]

def iniciar_las_listas_con_data():
    global lista_nombres
    global lista_path
    global datos
    lista_nombres = []
    lista_path = []
    datos = []
    llamada_base_datos()
    for i in datos:
        
        
        nombre_link = obtener_dominio(i[0])
        lista_nombres.append(nombre_link)
        lista_path.append(i[1])
        
      



def create_index():

    try:
        es.indices.create( # ···> Solo debe ejecutarse una vez
            index=DB_NAME, # ···> db_scrapperDB_NAME
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

def refresh_indexes():
    # Here we need to read /data/ folder, find .html files and create the indexes
    #print('w')
    global lista_nombres
    global lista_path
    iniciar_las_listas_con_data()
    print("hola")
    print(lista_nombres)
    ##html_files = glob.glob(os.path.join(directory, "*.txt")) # ···> Lista de archivos html [ 'falabella.html', 'ripley.html']
    
    # If file (from html_files) is not in the index, then create it

    # We need to create a response to know if all files were created or are already in the index
    response = {
        'already_exists': [],
        'successfully_indexed': []
    }

    try:
        # For each file in html_files [ 'falabella.html', 'ripley.html']
        for i in range(len(lista_path)):

            file_name = lista_nombres[i] # ···> falabella | ripley
            url = datos[i][0]
            
            try:

                es.get(index=DB_NAME, id=file_name)
                
                response['already_exists'].append({'file_name':file_name})


            except:
                print('XS')
                with open(lista_path[i], 'r', encoding='ISO-8859-1')  as f:
                    file_content = f.read()
                    es.index(index='db_scrapper', id=file_name, document={
                        'title': file_name,
                        'content': file_content,
                        'url' : url,
                        'timestamp': datetime.now()

                    })

                    response['successfully_indexed'].append({'file_name':file_name})

        response['success'] = True
        return  response

    except Exception as e:
        print("desde error.. ")
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong' }



@app.get("/")
def read_root():
    return {"Hello": "World"}

# /api/elasticsearch/create: Create the elasticsearch: db_scrapper
@app.get("/api/elasticsearch/create")
def create_root():
    return create_index()

# /api/elasticsearch/refresh: Refresh the elasticsearch indexes
# For example, if we have a new file in the folder, we need to refresh the indexes
@app.get("/api/elasticsearch/refresh")
def refresh_root():
    return refresh_indexes()

@app.get("/api/delete")
def delete():
    # Crea una instancia de Elasticsearch
    es = Elasticsearch(os.getenv("URL_ELASTICSEARCH"))

    try:
        # Envía una solicitud DELETE para eliminar todos los índices
         es.indices.delete(index="db_scrapper")
        
    except:
        return{"status" : "error...."}

        
    
    return { 'success': True, 'message': 'Se han eliminado los indices' }
    


# /api/elasticsearch/search: Search in the elasticsearch indexes
@app.get("/api/elasticsearch/search")
def search_root(q: str = Query(None, min_length=3, max_length=50)):

    # Si no hay query, es decir se busca por /api/elasticsearch/search
    # entonces retorna todos los documentos
    if q is None:
        q = {
            "match_all": {},
        }
       # --- Searching in the index ---
        resp = es.search(index="db_scrapper", query=q)
        print(resp)
        print("cantidad de respuestas jiji", len(resp['hits']['hits']))
        finalResp = []
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            url = hit['_source']['url']
            content = hit['_source']['content']
            maintitle = title.split(".")[1]
            temp = { 'maintitle': maintitle, 'link': url, 'content': content}
            finalResp.append(temp)
            # print(finalResp)
        # Return full response
        encoded_item = jsonable_encoder({ 'success': True, 'data': finalResp })
        return encoded_item

    print("hola")
    print("aca la consulta ", Query )
    # q: str = Query(None, min_length=3, max_length=50)
    # ···> Query: None, min_length: 3, max_length: 50

    # We need to search in the index for the query
    # If we have a match, then return it
    # If we don't have a match, then return an error
    
    try:
        # NOTE: 'content' field is the field that we want to search (in the index)
        # query: It's the query that we want to search
        query = {
            "match": {
                "content": q,
            },
        }

        # highlight: It's the highlight (the text that we want to highlight)
        highlight = {
            "fields": {
                "content": {
                    "type": "unified",
                },
            },
        }

        # --- Searching in the index ---
        resp = es.search(index="db_scrapper", query=query, highlight=highlight)
        print(resp)
        print("cantidad de respuestas jiji", len(resp['hits']['hits']))
        finalResp = []
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            url = hit['_source']['url']
            print(hit.keys())
            print(hit['highlight'])
            content = hit['highlight']['content']


            maintitle = title.split(".")[1]
            temp = { 'maintitle': maintitle, 'link': url, 'content': content}
            finalResp.append(temp)
            # print(finalResp)
        # Return full response
        

        encoded_item = jsonable_encoder({ 'success': True, 'data': finalResp })
        return encoded_item

    except Exception as e:

        print('Error: ', e)
        encoded_item = jsonable_encoder({ 'success': False, 'message': 'Something went wrong. Try adding a query ex: <search?q=audifonos>' })
        return encoded_item


 
@app.post("/api/elasticsearch/linkPath_scrapper")
async def linkPath_scrapper(linkPath_scrapper: dict):
    if not linkPath_scrapper:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos")

    # LINK PATH : /home/alex/Desktop/info288/proyecto/docs_indice_invertido/scraping/esclavo2/data/www.youtube.com_24.txt
    # Add : maintitle, url, content
    link_content = linkPath_scrapper['linkPath_scrapper']
    
    # conexino mariadb
    cursor_1 = conexion.cursor()
    # Se ejecuta la consulta SQL
    cursor_1.execute(f"SELECT link FROM documentos WHERE path = '{link_content}'")
    url = cursor_1.fetchone()

    # Se verifica si el url es None o no
    print("url: ", url)
    if url is None:
        print("El elemento no existe en la base de datos")
        return {"status": "error", "message": "El elemento no existe en la base de datos"}
    cursor_1.close()

    # Read the file
    print("linkPath_scrapper: ", link_content)
    file_name = link_content.split("/")[-1].split(".")[1]

    print("file_name: ", file_name)
    print("url: ", url[0])
    try:
        with open(link_content, 'r', encoding='ISO-8859-1')  as f:
            file_content = f.read()
            es.index(index='db_scrapper', id=file_name, document={
                'title': file_name,
                'content': file_content,
                'url' : url,
            })
            return { 'success': True, 'message': 'Se ha indexado el archivo'}

    except Exception as e:
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong' }

@app.post("/api/links")
async def get_link(link: dict):
    
    if not link:
        raise HTTPException(status_code=400, detail="No se proporcionaron datos")

#TODO Ver si existe un link igual en la base de datos, si existe no agregarlo, si no, agregarlo

    #####
    hora_desc = "17:00:00"
    link_final = link["link"]
    print("link: ",link_final)
    query_db = "INSERT INTO documentos (link, hora_desc) VALUES (%s, %s)"
    values_db = (link_final, hora_desc)
    cursor.execute(query_db, values_db)
    conexion.commit()

    return JSONResponse(content={"message": link})

# ASI SE EJECUTA :  se envia como json en un body

# {
#     "link": "https://www.example.com"
# }

    

    

    
#     ##refresh_indexes()

#     uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
   
    uvicorn.run(app, host="0.0.0.0", port=port)