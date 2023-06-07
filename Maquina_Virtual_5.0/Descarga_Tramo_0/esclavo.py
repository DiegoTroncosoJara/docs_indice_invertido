from flask import Flask , jsonify, request
from urllib.parse import urlparse, urljoin
import requests
import random 
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
    file_name = './data/{}.txt'.format(url)
    file_path =  os.path.abspath(file_name)
    with open(file_name, 'w') as txt:
        txt.write(data)
    return file_path

def writeLinkScarping(data):
    with open("./data/link_for_scraping.txt", 'a') as txt:
        txt.write(data)
        ##txt.write("\n")

## obtener un diferenciador para la  paginas con el mismo dominio
def obtainDomain(url): 
    quantity = len(url)
    quantity = "" + str(quantity) 
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    return domain+"_"+quantity  

def scrapingLinks(url, links):
    data = ""
    urls = []
    for link in links:
            href = link.get('href')  # Obtener el atributo 'href'
            if href:
                absolute_url = urljoin(url, href)
                urls.append(absolute_url)
    
    num_rand = random.randint(1,4)
    print(num_rand)
    print(len(urls))
    for i in range(num_rand):
        rand_link_cant = random.randint(0,len(urls))
        
        data +=  urls[rand_link_cant] +  "\n"

    writeLinkScarping(data)
    urls = []

@app.route('/getlink',  methods=['GET'])
def getlink():

    with open("./data/link_for_scraping.txt", "r") as archivo:
        lineas = archivo.readlines()

    if(len(lineas)!=0):

        indice_aleatorio = random.randint(0, len(lineas) - 1)
        linea_aleatoria = lineas[indice_aleatorio]
        linea_aleatoria = linea_aleatoria.rstrip()
        del lineas[indice_aleatorio]

        with open("./data/link_for_scraping.txt", "w") as archivo:
            archivo.writelines(lineas)
        return  jsonify ({'link': linea_aleatoria, "status" : "ok"  })
    else: 
       return  jsonify({ "status" : "ningunLink" }) 


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
        return jsonify({'content': 'error en leer el archivo.....'})


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

        # Buscar todos los elementos 'a' en el HTML
        links = soup.find_all('a')    
        scrapingLinks(url, links)


        for word in words:
            data += word + "\n"
        
        domain = obtainDomain(url)
        file_path = writeTxt(domain,data)
        
        
        

        return ({'status': "ok" , 'file_path': file_path })
    except: 
        print("error...")
        return   ({'status': "Algun error..." })



if __name__ == '__main__':

    ##arranca el servidor
    app.run(host=HOST, debug=True, port=PORT)
