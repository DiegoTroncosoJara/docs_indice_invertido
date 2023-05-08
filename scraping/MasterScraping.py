import schedule
import time
from datetime import datetime
import daemon
import mysql.connector
import requests
import os 
import multiprocessing
import json
import re
from dotenv import load_dotenv

from urllib.parse import urlparse
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'port': '3306',
  'database': 'documentos'
}
slaves = [('http://localhost:5001/', 0), ('http://localhost:5002/', 0), ('http://localhost:5003/', 0)]

## para los datos de la base de datos 
rows = ()


def init_esclavos(): 
    cantidad_esclavos = (os.getenv("ESCLAVOS_CANT"))
    print(cantidad_esclavos)
    


def obtener_dominio(url):
    ## obtener un diferenciador para la  paginas con el mismo dominio 
    cant= len(url)
    cant= "" + str(cant)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    return domain+"_"+cant 

###balanceador de carga
def send_request(url, url_data):
    data = {'url_scraping': url_data }
    response = requests.post('{}/scrapi'.format(url), json=data)
    if response.status_code == 200:
        print('La solicitud fue exitosa.')
    else:
        print('La solicitud falló con el código de estado:', response.status_code)
    resultado = response.json()
    # data = json.loads(response.text)
    print(resultado)

def get_min_slave():
    min_slave = slaves[0]
    for slave in slaves:
        if slave[1] < min_slave[1]:
            min_slave = slave
    return min_slave, slaves.index(min_slave)

def send_load_balanced_request(url_data):
    min_slave , index_min_slave = get_min_slave()
    send_request(min_slave[0],url_data)
    slaves[slaves.index(min_slave)] = (min_slave[0], min_slave[1] + 1)
    return  index_min_slave 


####-----------------------------------------------------------------------------------------------

def para_nuevas_url(rows_aux):
    global rows
    if(len(rows) == len(rows_aux)):
        pass   
    else: 
        tuplas_filtradas = [tupla for tupla in rows_aux if any(x is None for x in tupla)]
        for row in tuplas_filtradas:
            minimo = send_load_balanced_request(row[1])
            insertar_en_base_datos(row[1],minimo)
        rows = consultar_base_dato(config)
        
        
def consultar_por_hora():
    global rows
    now = datetime.now()
    hora_actual = now.strftime("%H")
    for row in rows:
        hora_data = str(row[2])
        if(str(hora_actual) !=  hora_data[:2]):
            print("no son iguales ")
        else:
            minimo = send_load_balanced_request(row[1])
            insertar_en_base_datos(row[1],minimo)        
    
    rows = consultar_base_dato(config)



    
def demonio_consulta_datos():
        rows_aux = consultar_base_dato(config)
        print("realizando consulta demonio")
        para_nuevas_url(rows_aux)
        

def consultar_base_dato(config):
    conn = mysql.connector.connect(**config)

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Ejecutar una consulta SQL
    cursor.execute("SELECT * FROM documentos")


    # Obtener los resultados de la consulta
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows 

def insertar_en_base_datos(url,id_esclavo):
    conn = mysql.connector.connect(**config)

    cursor = conn.cursor()
    consulta_select = 'SELECT * FROM documentos WHERE link = %s'
    cursor.execute(consulta_select, (url,))
    objeto = cursor.fetchone()

    ## nos da la hora... 
    now = datetime.now()
    hora_actual = now.strftime("%H:%M:%S")

    id = objeto[0]
    url = obtener_dominio(url)
    ruta_absoluta = os.path.abspath("{}.txt".format(url))
    
    ###actualiza la base de datos 
    consulta_update = 'UPDATE documentos SET path = %s, ultima_desc = %s, id_esclavo = %s  WHERE id = %s'
    cursor.execute(consulta_update, (ruta_absoluta, hora_actual, id_esclavo,id ))
    conn.commit()

    
    conn.close()


def iniciar_programa():
    #Agregue aquí el código para realizar la consulta
    for row in rows:
        print(row[1])
        minimo = send_load_balanced_request(row[1])
        print(minimo)
        insertar_en_base_datos(row[1],minimo)
        #peticion_esclavo(row[1])


if __name__ == '__main__':
    ##with daemon.DaemonContext():
    ##main()

    rows = consultar_base_dato(config)
    iniciar_programa()


    schedule.every(30).minutes.do(demonio_consulta_datos)
    schedule.every().hour.at(":00").do(consultar_por_hora)
    # schedule.every().day.at("15:56").do(iniciar_programa)
    # schedule.every().day.at("15:56").do(iniciar_programa)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

    


    #############################################################################
    # for row in rows:
    #     print(row[1])
    #     minimo = send_load_balanced_request(row[1])
    #     print(minimo)
    #     insertar_en_base_datos(row[1],minimo)
        ##peticion_esclavo(row[1])

        # with multiprocessing.Pool(num_processes) as pool:
        #         results = pool.map(send_load_balanced_request(row[1]), range(num_processes))



