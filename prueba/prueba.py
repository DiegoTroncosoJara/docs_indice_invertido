import requests

# URL del servidor Flask
url = "http://127.0.0.1:4001/leer"

# Realizar la solicitud GET al servidor
response = requests.post(url, json={
    "file_path" : "/Users/basti/Desktop/sis_dis/docs_indice_invertido/Maquina_Virtual_5.0/Descarga_Tramo_0/data/www.pcfactory.cl_25.txt"
})

# Verificar si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    result = response.json()
    result = result["content"]
    
    
    print(result)

    # Guardar el contenido de la respuesta en un archivo local
    pass

else:
    print("Error al obtener el archivo TXT:", response.status_code)
