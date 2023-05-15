from flask import Flask , jsonify, request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
import re
##----------------------------------------------------------------#

port = 5001

## define que es una aplicacion flask 
app = Flask(__name__)

## guarda los datos scrapiados en un archivo txt -> el nombre del archivo es el dominio con un identificador
def escribir_archivo(url,data):
    with open('./data/{}.txt'.format(url), 'w') as archivo:
        archivo.write(data)

## obtener un diferenciador para la  paginas con el mismo dominio
def obtener_dominio(url): 
    cant= len(url)
    cant= "" + str(cant)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    return domain+"_"+cant 


## definicion  de un latido para saber que el servidor esta disponible
@app.route('/latido',  methods=['GET'])
def latido():
    return  ({'status': "ok" })


###definicon /scrapi -> en esta parte  realiza el scrapeo de la pagina enviada.
@app.route('/scrapi',  methods=['POST'])
def scraping_data():
    
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
        
        domain = obtener_dominio(url)
        escribir_archivo(domain,data)
        return ({'status': "ok" })
    except:
        print("error...")
        return   ({'status': "Algun error..." })



if __name__ == '__main__':

    ##arranca el servidor
    app.run(debug=True, port=port)
