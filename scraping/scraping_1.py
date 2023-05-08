import requests
from bs4 import BeautifulSoup
import csv

# URL de la página web a extraer
url = "https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38"

# Hacer una solicitud GET al sitio web y analizar el contenido HTML de la página
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Encontrar todos los elementos HTML que contienen la información de los productos
items = soup.find_all("div", class_="item-cell")

# Crear un archivo CSV para almacenar la información de los productos
csv_file = open("newegg_products.csv", "w")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["Brand", "Product Name", "Price", "Shipping"])

# Iterar a través de los elementos encontrados y extraer información
for item in items:
    brand = item.find("div", class_="item-branding").img["title"]
    product_name = item.find("a", class_="item-title").text
    price = item.find("li", class_="price-current").strong.text + item.find("li", class_="price-current").sup.text
    shipping = item.find("li", class_="price-ship").text.strip()
    
    # Escribir la información del producto en el archivo CSV
    csv_writer.writerow([brand, product_name, price, shipping])

# Cerrar el archivo CSV
csv_file.close()
