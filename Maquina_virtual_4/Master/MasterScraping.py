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
  'user': os.getenv("USER_DB"),
  'password': os.getenv("PASSWORD_DB"),
  'host': os.getenv("PASSWORD_DB"),
  'port': os.getenv("PORT_DB"),
  'database': os.getenv("DATA_BASE")
}

## dupla que guarda los datos de la base de datos 
ROWS = ()
#lista donde se almancenan los esclavos que estan disponible 
SLAVES = []
#lista que tiene la url de todo los esclavos (esten o no disponible) -> todavia falta implementarlo 
SLAVES_TOTAL = []




##realiza una llamada para avisar al back-end que se insercto una nueva url para que pueda guardarla en el indixe invertido
def newIndexing(path): 
    try: 
        data = {'url_scraping': path  }
        response = requests.post('{}/api/elasticsearch/linkPath_scrapper'.format(os.getenv("URL_BACK_END")), json=data)
        result = response.json()
        if(result['success'] == True):
            print("se realizo la indexion correctamente....")
            return True
        elif(result['success'] == False):
            print("paso un error en el back.....")
            return False
        
    except:
        print("error.... ")

    pass


## llamada  para avisar al back-end que puede empezar indexear 
def callElasticSearch(): 
    try: 
        response = requests.get('{}/api/elasticsearch/refresh'.format(os.getenv("URL_BACK_END"))) 
        result = response.json()
        
        if((result['success'] == True)):
           print("todo ok en la indexion de los datos")
        
           return True 
        if(result['success'] == False):
            print("desde aca por que es falso.....")
            return False
            pass
    except:
        print("error.... ")

    pass 

##funcion que inicializa los esclavos disponibles 
def initSlaves(): 
    global SLAVES
    slaves_quantity = int((os.getenv("ESCLAVOS_quantity ")))
    for i in range(slaves_quantity):
        aux = os.getenv("URL_ESCLAVO_{}".format(str(i)))
        slave_status = checkSlaveStatus(aux)
        if(slave_status):
            SLAVES_TOTAL.append((aux,0))
    
    SLAVES = SLAVES_TOTAL

    
## funcion que verifica que los esclavos esten encendidos 
def checkSlaveStatus(url): 
    
    try: 
        response = requests.get('{}/latido'.format(url)) 
        result = response.json()
        if(result["status"]=="ok"):
            return True
        
    except:
        return False
## funcion que cada un tiempo determinado verifica que esten encendidos los esclavos.         
def timerSlaveStatus():
    for i in range(len(SLAVES)):
        
        slave_status = checkSlaveStatus(SLAVES[i][0])
        print(slave_status)
        if(slave_status != True):
            SLAVES.pop(i)

    print(SLAVES)  

## obtener un diferenciador para la  paginas con el mismo dominio  
def obtainDomain(url):
    quantity = len(url)
    quantity = "" + str(quantity )
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    return domain+"_"+quantity  

###----------------------------------------------------------------------------------#
###balanceador de carga
def sendRequest(url, url_data):
    data = {'url_scraping': url_data }
    response = requests.post('{}/scrapi'.format(url), json=data)
    if response.status_code == 200:
        print('La solicitud fue exitosa.')
    else:
        print('La solicitud falló con el código de estado:', response.status_code)
    result = response.json()
    # data = json.loads(response.text)
    print(result)

def getMinSlave():
    min_slave = SLAVES[0]
    for slave in SLAVES:
        if slave[1] < min_slave[1]:
            min_slave = slave
    return min_slave, SLAVES.index(min_slave)

def sendLoadBalancedRequest(url_data):
    min_slave , index_min_slave = getMinSlave()
    sendRequest(min_slave[0],url_data)
    SLAVES[SLAVES.index(min_slave)] = (min_slave[0], min_slave[1] + 1)
    return  index_min_slave 
###----------------------------------------------------------------------------------#


##funcion que validad si se incerto una  nueva url 
def checkNewUrls(rows_aux):
    global ROWS
    if(len(ROWS) == len(rows_aux)):
        pass   
    else: 
        filtered = [tuple for tuple in rows_aux if any(x is None for x in tuple)]
        for row in filtered:
            min = sendLoadBalancedRequest(row[1])
            path = insertInDB(row[1],min)
            newIndexing(path)
        ROWS = queryDB(config)
        
## funcion que validad si alguna de las url de la base de datos le toca hacer scraping         
def checkEveryHour():
    global ROWS
    now = datetime.now()
    current_time = now.strftime("%H")
    for row in ROWS:
        data_time = str(row[2])
        if(str(current_time) !=  data_time[:2]):
            print("no son iguales ")
        else:
            min = sendLoadBalancedRequest(row[1])
            insertInDB(row[1],min)        
    
    ROWS = queryDB(config)



##funcion que consulta se agrego  una nueva url para realizar el scraping    
def daemonProcess():
        rows_aux = queryDB(config)
        print("realizando consulta demonio")
        ##verifica si hay url con cambos vacios
        checkNewUrls(rows_aux)
        
### crae los datos de la base de datos
def queryDB(config):
    conn = mysql.connector.connect(**config)

    # Crear un cursor para ejecutar consultas SQL
    cursor = conn.cursor()

    # Ejecutar una consulta SQL
    cursor.execute("SELECT * FROM documentos")


    # Obtener los results de la consulta
    ROWS = cursor.fetchall()

    cursor.close()
    conn.close()

    return ROWS 

## cuando ya se realizo el scraping se incerta en la base de datos la informacion correspondinete como, hora, path y la id del esclavo que realizo es scraping
def insertInDB(url,id_esclavo):
    conn = mysql.connector.connect(**config)

    cursor = conn.cursor()
    query_select = 'SELECT * FROM documentos WHERE link = %s'
    cursor.execute(query_select, (url,))
    object = cursor.fetchone()

    ## nos da la hora... 
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")

    id = object[0]
    url = obtainDomain(url)
    absolute_path = os.path.abspath("esclavo{}/data/{}.txt".format(id_esclavo,url))
    ###"/esclavo{}/data/{}.txt".format(str(id_esclavo), url)
    ###actualiza la base de datos 
    query_update = 'UPDATE documentos SET path = %s, ultima_desc = %s, id_esclavo = %s  WHERE id = %s'
    cursor.execute(query_update, (absolute_path, current_time, id_esclavo,id ))
    conn.commit()

    
    conn.close()
    return absolute_path

##porgrama que inicializa el programa cada vez que se ejecuta 
def startProgram():
    ##verifica que los esclavos esten disponibles y los agrega a una lista -> SLAVES
    initSlaves()
    #Agregue aquí el código para realizar la consulta
    for row in ROWS:
        print(row[1])
        min = sendLoadBalancedRequest(row[1])
        print(min)
        insertInDB(row[1],min)
        #peticion_esclavo(row[1])
    if(callElasticSearch()):
            print("se realizo llama al back-end")



if __name__ == '__main__':

    if(1):
        ## son los datos que estna en la base de datos 
        ROWS = queryDB(config)
        # inicia el programa
        startProgram()
        
        #verifica cada 1 minitos si los esclavos estan disponibles
        schedule.every(1).minutes.do(timerSlaveStatus)
        #verifica cada 30 min si se agrego una nueva url a la base de datos
        schedule.every(30).minutes.do(daemonProcess)
        ##verifica cada 1 hora si a alguna url se toca hacer scraping
        schedule.every().hour.at(":00").do(checkEveryHour)

        # schedule.every().day.at("15:56").do(startProgram)
        # schedule.every().day.at("15:56").do(startProgram)

        
        ## ol programa queda corriendo 
        while True:
            schedule.run_pending()
            time.sleep(1)

    


    ###########################################################################
    # for row in ROWS:
    #     print(row[1])
    #     minimo = sendLoadBalancedRequest(row[1])
    #     print(minimo)
    #     insertInDB(row[1],minimo)
        ##peticion_esclavo(row[1])

        # with multiprocessing.Pool(num_processes) as pool:
        #         results = pool.map(sendLoadBalancedRequest(row[1]), range(num_processes))



