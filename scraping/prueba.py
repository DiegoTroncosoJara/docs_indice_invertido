import requests

url = 'http://localhost:5001/scrapi'
url_scraping = "https://www.pcfactory.cl/producto/43968-gear-desktop-intel-pentium-gold-g6405-4gb-1tb"
data = {'url_scraping': url_scraping }

response = requests.post(url, json=data)

if response.status_code == 200:
    print('La solicitud fue exitosa.')
else:
    print('La solicitud falló con el código de estado:', response.status_code)

