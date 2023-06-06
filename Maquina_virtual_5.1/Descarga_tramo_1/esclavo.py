from flask import Flask , jsonify, request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
import re
import os
from dotenv import load_dotenv

##----------------------------------------------------------------#
##funcion que permite leer el archivo .env 
load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT_SLAVE")

## define que es una aplicacion flask 
app = Flask(__name__)

## guarda los datos scrapiados en un archivo txt -> el nombre del archivo es el dominio con un identificador
def writeTxt(url,data):
    with open('./data/{}.txt'.format(url), 'w') as txt:
        txt.write(data)

## obtener un diferenciador para la  paginas con el mismo dominio
def obtainDomain(url): 
    quantity = len(url)
    quantity = "" + str(quantity)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    return domain+"_"+quantity  


## definicion  de un beat para saber que el servidor esta disponible
@app.route('/latido',  methods=['GET'])
def beat():
    return  ({'status': "ok" })

#permite devolver el contenido de los archivos
@app.route('/leer', methods=['POST'])
def readFile():
    file_path = request.get_json('file_path')
    file_path =  file_path['file_path']
    
    # Ruta al archivo TXT en el servidor
    # Leer el contenido del archivo
    try: 
        with open(file_path, 'r') as file:
            content = file.read()

        # Devolver 
        return jsonify({'content': content})
    except:
        return jsonify({'error': 'error en leer el archivo.....'})
    

###definicon /scrapi -> en esta parte  realiza el scrapeo de la pagina enviada.
@app.route('/scrapi',  methods=['POST'])
def scrapingData():
    
    data = ""
    url = request.get_json('url_scraping')
    url = url['url_scraping']

    try:
        ##response = requests.get("https://"+url+"/") # Hacer una solicitud GET al sitio web
        response = requests.get(url)
       
        soup = BeautifulSoup(response.text, 'html.parser') # Analizar el contenido HTML de la página
        # # Extraer todas las palabras clave de la página web
        words = re.findall('\w+', soup.text)
        
        for word in words:
            data += word + "\n"
        
        domain = obtainDomain(url)
        writeTxt(domain,data)
        return ({'status': "ok" })
    except:
        print("error...")
        return   ({'status': "Algun error..." })



if __name__ == '__main__':

    ##arranca el servidor
    app.run(host=HOST, debug=True, port=PORT)
