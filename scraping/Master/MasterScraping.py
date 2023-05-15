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
##----------------------------------------------------------------#
##funcion que permite leer el archivo .env 
load_dotenv()

#diccionario que guarda la informacion para la conexión de la base de datos 
config = {
  'user': 'root',
  'password': '',
  'host': 'localhost',
  'port': '3306',
  'database': 'documentos'
}

## dupla que guarda los datos de la base de datos 
rows = ()
#lista donde se almancenan los esclavos que estan disponible 
slaves = []
#lista que tiene la url de todo los esclavos (esten o no disponible) -> todavia falta implementarlo 
slaves_total = []




##realiza una llamada para avisar al back-end que se insercto una nueva url para que pueda guardarla en el indixe invertido
def llamada_para_nuevo_link(nuevo_url): 
    try: 
        response = requests.get('{}'.format("http://0.0.0.0:8000/api/............")) 
        resultado = response.json()
        if(resultado['success'] == True):
            print("se realizo la indexion correctamente....")
            return True
        elif(resultado['success'] == False):
            print("paso un error en el back.....")
            return False
        
    except:
        print("error.... ")

    pass

llamada_para_nuevo_link("hola")
## llamada  para avisar al back-end que puede empezar indexear 
def llamada_back_elastich(): 
    try: 
        response = requests.get('{}'.format("http://0.0.0.0:8000/api/elasticsearch/refresh")) 
        resultado = response.json()
        if((resultado['success'] == True)):
           print("todo ok en la indexion de los datos")

           return True 
        elif(resultado['success'] == False):
            print("desde aca por que es falso.....")
            return False
            pass
    except:
        print("error.... ")

    pass 

##funcion que inicializa los esclavos disponibles 
def init_esclavos(): 
    global slaves
    cantidad_esclavos = int((os.getenv("ESCLAVOS_CANT")))
    for i in range(cantidad_esclavos):
        aux = os.getenv("URL_ESCLAVO_{}".format(str(i)))
        condion_esclavo = latido_de_esclavos(aux)
        if(condion_esclavo):
            slaves_total.append((aux,0))
    
    slaves = slaves_total

    
## funcion que verifica que los esclavos esten encendidos 
def latido_de_esclavos(url): 
    
    try: 
        response = requests.get('{}/latido'.format(url)) 
        resultado = response.json()
        if(resultado["status"]=="ok"):
            return True
        
    except:
        return False
## funcion que cada un tiempo determinado verifica que esten encendidos los esclavos.         
def vallidacion_de_esclavo_determinado_tiempo():
    for i in range(len(slaves)):
        
        condicion_esclavo = latido_de_esclavos(slaves[i][0])
        print(condicion_esclavo)
        if(condicion_esclavo != True):
            slaves.pop(i)

    print(slaves)  

## obtener un diferenciador para la  paginas con el mismo dominio  
def obtener_dominio(url):
    cant= len(url)
    cant= "" + str(cant)
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return domain+"_"+cant 

###----------------------------------------------------------------------------------#
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
###----------------------------------------------------------------------------------#


##funcion que validad si se incerto una  nueva url 
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
        
## funcion que validad si alguna de las url de la base de datos le toca hacer scraping         
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



##funcion que consulta se agrego  una nueva url para realizar el scraping    
def demonio_consulta_datos():
        rows_aux = consultar_base_dato(config)
        print("realizando consulta demonio")
        ##verifica si hay url con cambos vacios
        para_nuevas_url(rows_aux)
        
### crae los datos de la base de datos
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

## cuando ya se realizo el scraping se incerta en la base de datos la informacion correspondinete como, hora, path y la id del esclavo que realizo es scraping
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
    ruta_absoluta = os.path.abspath("esclavo{}/data/{}.txt".format(id_esclavo,url))
    ###"/esclavo{}/data/{}.txt".format(str(id_esclavo), url)
    ###actualiza la base de datos 
    consulta_update = 'UPDATE documentos SET path = %s, ultima_desc = %s, id_esclavo = %s  WHERE id = %s'
    cursor.execute(consulta_update, (ruta_absoluta, hora_actual, id_esclavo,id ))
    conn.commit()

    
    conn.close()

##porgrama que inicializa el programa cada vez que se ejecuta 
def iniciar_programa():
    ##verifica que los esclavos esten disponibles y los agrega a una lista -> slaves
    init_esclavos()
    #Agregue aquí el código para realizar la consulta
    for row in rows:
        print(row[1])
        minimo = send_load_balanced_request(row[1])
        print(minimo)
        insertar_en_base_datos(row[1],minimo)
        #peticion_esclavo(row[1])


if __name__ == '__main__':

    #cosas de prueba 

    ##with daemon.DaemonContext():
    ##main()

    # init_esclavos()

    # print(slaves_total)
    # print(slaves)
    
    ##llamada_back_elastich()

    if(1):
        ## son los datos que estna en la base de datos 
        rows = consultar_base_dato(config)
        # inicia el programa
        iniciar_programa()
        
        #verifica cada 1 minitos si los esclavos estan disponibles
        schedule.every(1).minutes.do(vallidacion_de_esclavo_determinado_tiempo)
        #verifica cada 30 min si se agrego una nueva url a la base de datos
        schedule.every(30).minutes.do(demonio_consulta_datos)
        ##verifica cada 1 hora si a alguna url se toca hacer scraping
        schedule.every().hour.at(":00").do(consultar_por_hora)

        # schedule.every().day.at("15:56").do(iniciar_programa)
        # schedule.every().day.at("15:56").do(iniciar_programa)

        
        ## ol programa queda corriendo 
        while True:
            schedule.run_pending()
            time.sleep(1)

    


    ###########################################################################
    # for row in rows:
    #     print(row[1])
    #     minimo = send_load_balanced_request(row[1])
    #     print(minimo)
    #     insertar_en_base_datos(row[1],minimo)
        ##peticion_esclavo(row[1])

        # with multiprocessing.Pool(num_processes) as pool:
        #         results = pool.map(send_load_balanced_request(row[1]), range(num_processes))



