# Python-Ofensivo
Diferentes Herramientas, diferentes propositos.

----------------------------------------------------------------------------------------------------------------------

Mac Changers. 
El "MacChanger_spec" necesita que se le introduzca el numero de MAC por el que se lo quiere cambiar. Mientras que el "MacChanger_random", con solo especificar las interfaz de red, selecciona una direccion MAC random.

----------------------------------------------------------------------------------------------------------------------

Envenenador ARP y Sniffers.
Estas herramientas van en conjuntos ya que mientras se ejecuta el "ARP_spoofer". Los demas, como "DNS_sniffer", sirven para filtrar la informacion que se puede extraer de los paquetes de red.

----------------------------------------------------------------------------------------------------------------------

Scanners de red y puertos.
"Red_scanner" Sirve para scannear los host conectados a la red en la cual tiene conectividad. Ex: python3 Red_scanner.py -t 192.168.100.1-255 | Escaneara los host conectados a tu red de la 1 a la 255.
"Port_scan" Sirve para scanear los puertos abiertos de una red. Ex: python3 Port_scan.py -t 192.168.100.XX -p 1-65535 | Escaneara los puertos que esten abiertos entre 1 y 65535. | -p 22, 80 | Escaneara si el puerto 22 y/o el 80 estan abiertos.

----------------------------------------------------------------------------------------------------------------------
...

