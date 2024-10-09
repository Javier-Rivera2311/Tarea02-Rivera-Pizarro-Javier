# Javier Rivera Pizarro, javier.riverapi@alumnos.uv.cl 
# Juan Pablo Páez Salas, juan.paez@alumnos.uv.cl 
# Fabian Cornejo Silva, fabian.cornejo@alumnos.uv.cl

import getopt
import os
import re
import time
import http.client
import json
import sys
import ssl

# URL de la API para consultar MAC
API_HOST = "api.maclookup.app"
API_PATH = "/v2/macs/"

def lookup_mac(mac_address):                                                   # Funcion buscar direccion mac especificada y mostrar su fabricante
    """Consulta la API para obtener el fabricante a partir de una MAC."""
    try:
        start_time = time.time()                                      # Variable que empieza a contar el tiempo de ejecucion
        
        # Crear un contexto SSL que no verifica certificados
        context = ssl._create_unverified_context()

        # Configuración de la conexión HTTP con la API 
        conn = http.client.HTTPSConnection(API_HOST,context=context)                            
        conn.request("GET", f"{API_PATH}{mac_address}")      # Donde se realiza la solicitud de tipo get solicitando al informacion de la direccion mac
        response = conn.getresponse()                        # Respuesta del servidor
        data = response.read()                               # Lectura de la respuesta
        conn.close()                                         # Fin de la conexion 
        
        response_time = int((time.time() - start_time) * 1000)  # Tiempo en ms 
        result = json.loads(data)                               # Conversion de la respuesta de JSON a un diccionario python

        if isinstance(result, dict) and result.get('company'):                        # Muestra en pantalla la direccion mac, el tiempo y si se encontro el fabricante
            return f"MAC address : {mac_address}\nFabricante : {result['company']}\nTiempo de respuesta: {response_time}ms"
        else:                                                                         # Muestra en pantalla la direccion mac, el tiempo y si no se encontro el fabricante
            return f"MAC address : {mac_address}\nFabricante : Not found\nTiempo de respuesta: {response_time}ms"   
         
    except Exception as e:
        return f"Error consultando la MAC: {e}"
    


def lookup_arpmac(mac_address):                                                   # Funcion buscar direcciones mac dentro de la tabla arp y mostrar su fabricante con su direccion mac
    """Consulta la API para obtener el fabricante a partir de una MAC."""
    try:  
        # Configuración de la conexión HTTP con la API 
        conn = http.client.HTTPSConnection(API_HOST)                            
        conn.request("GET", f"{API_PATH}{mac_address}")      # Donde se realiza la solicitud de tipo get solicitando al informacion de la direccion mac
        response = conn.getresponse()                        # Respuesta del servidor
        data = response.read()                               # Lectura de la respuesta
        conn.close()                                         # Fin de la conexion 
        result = json.loads(data)                            # Conversion de la respuesta de JSON a un diccionario python

        if isinstance(result, dict) and result.get('company'):               # Muestra en pantalla la direccion mac y el fabricante
            return f"{mac_address} / {result['company']}"
        else:
            return 0
           
    except Exception as e:
        return f"Error consultando la MAC: {e}"


def lookup_arp():
    """Obtiene la tabla ARP en Windows y consulta los fabricantes."""
    try:
        arp_output = os.popen('arp -a').read()
        arp_lines = arp_output.splitlines()
        results = []
        result = "IP/MAC/Vendor:"                            # Agrega formato a el arreglo
        results.append(result)          

        for line in arp_lines:                               # Busca las direcciones mac y las compara dentro de otra funcion lookup_arpmac()
            # Regex para capturar direcciones MAC
            match = re.search(r'([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]{2})', line)
            if match:
                mac_address = match.group(0)
                result = lookup_arpmac(mac_address)
                if result != 0:                              # Se agrega a el arreglo si este tiene fabricante
                    results.append(result)
                

        return "\n".join(results) if results else "No se encontraron direcciones MAC en la tabla ARP."     
    except Exception as e:
        return f"Error obteniendo la tabla ARP: {e}"

def main(argv): 
    mac_address = '' # Instancia de la direccion mac como vacia
    arp_flag = False # Instancia de la variable arp_flag como falsa para variable de control

    try:
        opts, args = getopt.getopt(argv, "", ["mac=", "arp", "help"])  # Aqui se obtienen los argumentos ingresados por consola al ejecutar el codigo
    except getopt.GetoptError as err:
        print(err)                                                     # Si falla muestra en pantalla error y como usar el --help
        sys.exit(2)

    for opt, arg in opts:                                              # Comparacion del argumento ingresado donde se ingresa en las variables dependiendo del argumento ingresado
        if opt == '--mac':                                             # ingresa en mac_address si el argumento entregado es --mac
            mac_address = arg   
        elif opt == '--arp':                                           # ingresa en arp_flag si el argumento entregado es --arp
            arp_flag = True
        elif opt == '--help':                                                # Muestra en la consola como utilizar el programa y termina su ejecucion
            print('Uso: OUILookup.py --mac <mac_address> | --arp | --help')
            sys.exit()

    if mac_address:                         
        result = lookup_mac(mac_address)                 #si la variable mac_address tiene algun contenido ejecuta lookup_mac para buscar la direccion mac proporcionada y la muestra en pantalla
        print(result)
    elif arp_flag:                                       #si la variable arp_flag tiene algun contenido ejecuta lookup_arp para buscar las direcciones mac del sistema y la muestra en pantalla
        result = lookup_arp()
        print(result)
    else:                                                                               
        print('No se proporcionó ninguna opción válida. Usa --help para más información.')  

if __name__ == "__main__":
    main(sys.argv[1:])
