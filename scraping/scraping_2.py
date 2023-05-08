import requests
from bs4 import BeautifulSoup
import re
import json

# Lista de URLs a extraer
# urls = ['https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38', 'https://www.google.com', 'https://www.bbc.com']
urls = ["https://www.pcfactory.cl/producto/43968-gear-desktop-intel-pentium-gold-g6405-4gb-1tb"]
url1 = urls[0]
url1 = url1[8:]
print(url1)
# Diccionario para almacenar las palabras clave y las URL relacionadas
index = {}
data = ""
# Iterar a través de cada URL
for url in urls:
    response = requests.get(url) # Hacer una solicitud GET al sitio web
    soup = BeautifulSoup(response.text, 'html.parser') # Analizar el contenido HTML de la página
    
    # Extraer todas las palabras clave de la página web
    words = re.findall('\w+', soup.text)
    
    # Agregar cada palabra clave y la URL relacionada al índice
    for word in words:
        if word not in index:
            data += word + " url:" +  url + "\n"
            
            # index[word] = [url]
        # elif url not in index[word]:
        #     index[word].append(url)

# Convertir el índice en formato JSON y guardar en un archivo
with open('index.json', 'w') as outfile:
    json.dump(index, outfile)


with open('{}.txt'.format("prueba"), 'w') as archivo:
    archivo.write(data)
