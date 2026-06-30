# Python-Ofensivo

Mis herramientas desarrolladas en Python para pruebas de seguridad ofensiva.

> **Aviso:** Todas las herramientas están destinadas exclusivamente a fines educativos y a su utilización en entornos propios o con autorización explícita.

---

## Herramientas incluidas

### Requirements

Cada carpeta contiene su respectivos "requirements.txt". Para instalarlos ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

---

### MAC Changers

Permiten modificar la dirección MAC de una interfaz de red.

#### MacChanger_spec.py

Cambia la dirección MAC por una especificada manualmente por el usuario.

Ejemplo:

```bash
python3 MacChanger_spec.py -i eth0 -m 00:11:22:33:44:55
```

#### MacChanger_random.py

Genera y asigna automáticamente una dirección MAC aleatoria. Solo es necesario indicar la interfaz de red.

Ejemplo:

```bash
python3 MacChanger_random.py -i eth0
```

---

### ARP Spoofing y Sniffers

Estas herramientas están diseñadas para utilizarse en conjunto.

#### ARP_spoofer.py

Realiza un ataque de ARP Spoofing (Man-in-the-Middle), redirigiendo el tráfico entre los dispositivos de la red.

Mientras esta herramienta se encuentra en ejecución, es posible utilizar los sniffers para inspeccionar la información que circula por la red.

Ejemplo:

```bash
python3 ARP_spoofer.py -t 192.168.100.1
```

#### DNS_sniffer.py

Captura y muestra las consultas DNS realizadas por los equipos de la red. Simplemente ejecutalo y el script hara todo.

#### HTTPS_sniffer.py

Se requiere control previo del dispositivo a analizar para asi descargar certificaciones de MITMProxy. (Para la ejecucion de este script es necesario tener instalado MITMProxy por fuera de python)

```bash
mitmproxy/mitmdump -s HTTPS_sniffer.py --quiet
```

---

### Escáneres de red y puertos

#### Red_scanner.py

Escanea un rango de direcciones IP para identificar los hosts activos dentro de una red.

Ejemplo:

```bash
python3 Red_scanner.py -t 192.168.100.1-255
```

Resultado:

* Escaneará las direcciones desde `192.168.100.1` hasta `192.168.100.255` e identificará los dispositivos activos.

---

#### Port_scan.py

Escanea los puertos abiertos de un host.

Escanear todos los puertos:

```bash
python3 Port_scan.py -t 192.168.100.10 -p 1-65535
```

Escanear puertos específicos:

```bash
python3 Port_scan.py -t 192.168.100.10 -p 22,80
```

Resultado:

* Verifica si los puertos indicados se encuentran abiertos en el host objetivo.

---

## Requisitos

* Python 3.x
* Privilegios de administrador/root para aquellas herramientas que interactúan directamente con interfaces de red.

