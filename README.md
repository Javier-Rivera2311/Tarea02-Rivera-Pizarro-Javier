# Tarea02-Rivera-Pizarro-Javier

*Javier Rivera

*javier.riverapi@alumnos.uv.cl

*Este código representa una utilidad que permite averiguar quién fabricó una tarjeta de red en particular a partir de su dirección MAC o dirección IP.

*Para realizar esto, comienza descargando una base de datos de fabricantes de la IEEE desde una dirección URL llamada "oui_db_url". Luego, se establecen varias funciones para examinar y buscar tanto direcciones MAC como *direcciones IP en esta base de datos de fabricantes.

*La herramienta se puede utilizar con tres argumentos de línea de comandos:

*--ip: Se utiliza para especificar la dirección IP del dispositivo que se quiere investigar.

*--mac: Sirve para indicar la dirección MAC que se desea analizar.

*--arp: Cuando se utiliza esta opción, se obtienen los fabricantes de los dispositivos disponibles en la tabla ARP.

*El programa utiliza el módulo "argparse" para procesar y entender los argumentos proporcionados en la línea de comandos. Dependiendo de si se ingresa una dirección MAC o una dirección IP, la herramienta busca en la base de *datos de fabricantes y muestra en la pantalla el nombre del fabricante correspondiente. Si se utiliza el argumento --arp, la herramienta mostrará los fabricantes de los dispositivos que están disponibles en la tabla ARP.
