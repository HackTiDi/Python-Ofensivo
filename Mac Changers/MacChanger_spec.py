import argparse
import re
import subprocess
from time import sleep

def get_arguments():

    parser = argparse.ArgumentParser(description="Herramienta para cambiar la MAC de tu interfaz de red")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la Interfaz de red")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="Direccion MAC que quiera tener." )
    return parser.parse_args()

def is_valid_input(interface, mac_address):

    patron_int = r"(eth|wlan|enp|wlp)\d+"
    patron_mac = r"^([0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}"

    is_valid_int = re.match( patron_int, interface)
    is_valid_mac = re.match( patron_mac, mac_address)

    return is_valid_int and is_valid_mac

def change_mac_address(interface, mac_address):

    if is_valid_input(interface, mac_address):

        verificacion = subprocess.run([ "ifconfig", interface ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if verificacion.returncode == 0: 
            print("\n[+] Interfaz Valida y existente. Se empezara el cambio de direccion MAC")
            sleep (0.5)
            print(f"\n[+] Iniciando cambio de MAC")
            sleep (0.5)
            try:
                subprocess.run(["ifconfig", interface, "down"], check=True)
                subprocess.run(["ifconfig", interface, "hw", "ether", mac_address], check=True)
                subprocess.run(["ifconfig", interface, "up"], check=True)
                
                print(f"\n[+] Tu direccion MAC ha sido cambiada exitosamente. Tu nueva direccion MAC es: {mac_address}")
            except:
                subprocess.run(["ifconfig", interface, "up"])
                print(f"\n[!] Ha surgido un error, verifique los permisos de ejecucion (sudo).")
        else:
            print("\n[!] La interfaz ingresada es invalida")

    else:
        print("\n[!] Los datos introduccidos son incorrectos")

def main():
    args = get_arguments()
    change_mac_address(args.interface, args.mac_address)

if __name__ == '__main__':
    main()