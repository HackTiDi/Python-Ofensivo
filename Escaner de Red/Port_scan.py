#!/usr/bin/env python3

import socket
import argparse
import signal
import sys
from termcolor import colored
from concurrent.futures import ThreadPoolExecutor

open_sockets = []

def def_handler(sig,frame):
    print(colored(f"\n[!] Saliendo del programa\n", "red" ))
    
    for socket in open_sockets:
        socket.close()

    sys.exit(0)

signal.signal(signal.SIGINT, def_handler) # Ctrl + C
    

def get_argument():

    parser = argparse.ArgumentParser(description="Fast TCP Scan")
    parser.add_argument("-t", "--target", dest="target", required=True, help="Victim target to Scan. Ex: (-t 192.0.0.1)")
    parser.add_argument("-p", "--port", dest="port", required=True, help= "Port Range to Scan. Ex: (-p 1-1000). Max ports to scan: 65535 (If you want scan some exact ports use ',' Ex: (-p 1,2,3,4)")
    options = parser.parse_args()

    return options.target, options.port

def create_socket():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    open_sockets.append(s)
    return s


def port_scanner(port, host):
    
    s = create_socket()

    try:
        s.connect((host, port))
        s.sendall(b"GET / HTTP/1.0\r\n\r\n")
        response = s.recv(1024)
        response = response.decode(errors = 'ignore').split('\n')
        if response:
            print(colored(f"\n[+] El puerto {port} esta abierto", "green"))

            for line in response:
                print(colored(f"{line}", "gray"))
        else:    
            print(colored(f"\n[+] El puerto {port} esta abierto", "green"))

    except (socket.timeout, ConnectionRefusedError):
        pass
    
    finally:
        s.close()
        

def scan_ports(ports, target):

    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda port:port_scanner(port, target), ports)
        

def parse_port(ports_str):
    
    if '-' in ports_str:
        start, end = map(int, ports_str.split(('-')))
        return range(start, end+1)
    elif ',' in ports_str:
        return map(int, ports_str.split(','))
    else:
        return (int(ports_str),)


def main():

    target, ports_str = get_argument()
    ports = parse_port(ports_str) 
    scan_ports(ports, target)
   
if __name__ == '__main__':
    print(colored("\n[+] Iniciando Escaneo de Puertos...", "gray"))
    main()