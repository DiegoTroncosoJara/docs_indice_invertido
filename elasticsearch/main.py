# FastAPI
from fastapi import FastAPI, Query
# Elasticsearch
from elasticsearch import Elasticsearch
from datetime import datetime
# Others
import os
import glob

##db conexion
import mysql.connector


conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="dbsd"
)
cursor = conexion.cursor()

#
app = FastAPI()

es = Elasticsearch("http://localhost:9200")
DB_NAME = 'db_scrapper'

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
        return { 'success': False, 'message': f'Index DB: {DB_NAME} already exists' }

def refresh_indexes():
    # Here we need to read /data/ folder, find .html files and create the indexes
    directory = "data"
    html_files = glob.glob(os.path.join(directory, "*.txt")) # ···> Lista de archivos html [ 'falabella.html', 'ripley.html']
    print(html_files)
    # If file (from html_files) is not in the index, then create it

    # We need to create a response to know if all files were created or are already in the index
    response = {
        'already_exists': [],
        'successfully_indexed': []
    }

    try:
        # For each file in html_files [ 'falabella.html', 'ripley.html']
        for file in html_files:
            
            print("sexooo",file)
            file_name = file.split('\\')[1].split('.txt')[0] # ···> falabella | ripley
            print("sexooo2",file)
            try:

                es.get(index=DB_NAME, id=file_name)
                response['already_exists'].append({'file_name':file_name})
                
            except:
                with open(file, 'r', encoding='utf-8')  as f:
                    file_content = f.read()
                    es.index(index='db_scrapper', id=file_name, document={
                        'title': file_name,
                        'content': file_content,
                        'timestamp': datetime.now()
                    })
                    response['successfully_indexed'].append({'file_name':file_name})

        return response

    except Exception as e:
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
    es = Elasticsearch()

    # Envía una solicitud DELETE para eliminar todos los índices
    es.indices.delete(index="db_scrapper")
    return { 'success': True, 'message': 'Se han eliminado los indices' }


# /api/elasticsearch/search: Search in the elasticsearch indexes
@app.get("/api/elasticsearch/search")
def search_root(q: str = Query(None, min_length=3, max_length=50)):
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
        finalResp = []
        for hit in resp['hits']['hits']:
            title = hit['_source']['title']
            content = hit['_source']['content']
            maintitle = title.split(".")[1]
            temp = { 'maintitle': maintitle, 'link': title, 'content': content}
            finalResp.append(temp)
        # Return full response
        return { 'success': True, 'data': finalResp }

    except Exception as e:
        print('Error: ', e)
        return { 'success': False, 'message': 'Something went wrong. Try adding a query ex: <search?q=audifonos>' }


@app.post("/api/link/")
async def get_link(link: str):
    hora_desc = "17:00:00"
    path = "/../data"
    query_db = "INSERT INTO documentos (link, hora_desc, path) VALUES (%s, %s, %s)"
    values_db = (link, hora_desc, path)
    cursor.execute(query_db, values_db)
    conexion.commit()
    return {"link_received": link}