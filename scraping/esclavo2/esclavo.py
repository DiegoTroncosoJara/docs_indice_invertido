from flask import Flask , jsonify, request
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import json
import re
port = 5003
app = Flask(__name__)


def escribir_archivo(url,data):
    with open('{}.txt'.format(url), 'w') as archivo:
        archivo.write(data)


def obtener_dominio(url):
    ## obtener un diferenciador para la  paginas con el mismo dominio 
    cant= len(url)
    cant= "" + str(cant)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    return domain+"_"+cant 

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


# @app.route('/scrapi/<url>')
# def scraping_data(url):
    
    
#     index = {}
#     data=""
#     try:
#         response = requests.get("https://"+url+"/") # Hacer una solicitud GET al sitio web
    
#         soup = BeautifulSoup(response.text, 'html.parser') # Analizar el contenido HTML de la página
#         # Extraer todas las palabras clave de la página web
#         words = re.findall('\w+', soup.text)
#         for word in words:
#                 data += word + "\n"
        
#         escribir_archivo(url,data)
#         return jsonify({'status': "ok" })
#     except:
#         print("error...")
#         return   jsonify({'status': "Algun error..." })


if __name__ == '__main__':
    app.run(debug=True, port=port)
