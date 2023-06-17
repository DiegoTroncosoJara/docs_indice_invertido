from flask import Flask , jsonify, request
from urllib.parse import urlparse, urljoin
import requests
import random 
from bs4 import BeautifulSoup
import json
import re
import os
from dotenv import load_dotenv
import zipfile
##----------------------------------------------------------------#
##funcion que permite leer el archivo .env 
load_dotenv()

HOST = os.getenv("HOST")
PORT = os.getenv("PORT_SLAVE")

## define que es una aplicacion flask 
app = Flask(__name__)

## algoritmo ue comprime el archivo txt despues de utilizarlo... 
def compressFile(file_path):
    """
    Comprime un archivo según su path
    """
    # ej: /some/path/to/www.file.txt
    nombre_archivo = file_path.split("/")[-1] # www.file.txt
    nombre_archivo = nombre_archivo.split(".")[:-1]
    nombre_archivo = ".".join(nombre_archivo) # www.file
    nombre_archivo_comprimido = "{}.zip".format(nombre_archivo) # file.zip
    print(nombre_archivo_comprimido)

    print('file_path = ', file_path)

    # Comprimimos el archivo en zip y lo guardamos en el path del archivo

    try:
        # tomamos el file_path menos el archivo.txt
        path = file_path.split("/")[:-1] # /some/path/to/www.file
        path = "/".join(path) # /some/path/to
        # agregamos el nombre del archivo comprimido
        path = "{}/{}".format(path, nombre_archivo_comprimido) # /some/path/to/file.zip
        print('path = ', path)
        # Comprimimos el archivo
        with zipfile.ZipFile(path, 'w') as zip:
            zip.write(file_path, nombre_archivo_comprimido)
        print("Archivo comprimido")
    except:
        print("Error al comprimir archivo")
        pass


    # Eliminar archivo original
    try:
        os.remove(file_path)
        print('removiendo archivo original')   
    except:
        print("Error al eliminar archivo original")
        pass


##----------------------------------------------------------------#

## guarda los datos scrapiados en un archivo txt -> el nombre del archivo es el dominio con un identificador
def writeTxt(url,data):
    file_name = './data/{}.txt'.format(url)
    file_path =  os.path.abspath(file_name)
    with open(file_name, 'w') as txt:
        txt.write(data)
    return file_path


### funcion que escribe los url  en  "link_for_scraping.txt"
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



## algoritmo que dado el scraping de las url, eligue alatoriamente entre (1,4) cuantos link va a dejar en  "link_for_scraping.txt"
def scrapingLinks(url, links):
    print(url)
    data = ""
    urls = []
    for link in links:
            href = link.get('href')  # Obtener el atributo 'href'
            if href:
                absolute_url = urljoin(url, href)
                urls.append(absolute_url)
    
    
    
    num_rand = random.randint(1,int(os.getenv("RANDOM_LINK")))

    for i in range(num_rand):
        rand_link_cant = random.randint(0,len(urls))
        
        data +=  urls[rand_link_cant] + "," + url +  "\n"

    writeLinkScarping(data)
    urls = []


##################################################################################################################################################
##################################################################################################################################################

#permite devolver el contenido de los archivos txt
@app.route('/leer', methods=['POST'])
def readFile():
    file_path = request.get_json('file_path')
    file_path =  file_path['file_path']
    ##print(file_path)
    # Ruta al archivo TXT en el servidor
    # Leer el contenido del archivo
    try: 
        with open(file_path, 'r') as file:
            content = file.read()

        # Devolver 
        ### aca
        compressFile(file_path)
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

##entrega un link al backend para que este lo pueda almacenar en db. Además, elimina del txt el link.
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




if __name__ == '__main__':

    ##arranca el servidor
    app.run(host=HOST, debug=True, port=PORT)
