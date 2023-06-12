import requests

# URL del servidor Flask
url = "http://127.0.0.1:4001/scrapi"

# Realizar la solicitud GET al servidor
response = requests.post(url, json={
    'url_scraping':  "https://www.pcfactory.cl/ereaders?categoria=828&papa=967"
})

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    result = response.json()
    
    
    print(result)

    # Guardar el contenido de la respuesta en un archivo local
    pass

else:
    print("Error al obtener el archivo TXT:", response.status_code)
