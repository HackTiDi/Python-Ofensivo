import argparse
import random
import subprocess
from time import sleep

def get_arguments():

    parser = argparse.ArgumentParser(description="Herramienta para cambiar la MAC de tu interfaz de red")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Nombre de la Interfaz de red")
    return parser.parse_args()

def change_mac(interface):

    verificacion = subprocess.run(["ifconfig", interface ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if verificacion.returncode == 0: 
        print("\n[+] Interfaz Valida y existente. Se empezara el cambio de direccion MAC")
        sleep(1)
        p1 = f"{random.choice('0123456789abcdef')}{random.choice('02468ace')}"
        mac = ":".join([p1] + ["".join(random.choices("0123456789abcdef", k=2)) for _ in range(5)])
        try:
            subprocess.run(["ifconfig", interface, "down"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\n[+] La nueva direccion mac sera: {mac}")
            sleep (0.5)
            print(f"\n[+] Iniciando cambio de MAC")
            sleep (0.5)
            subprocess.run(["ifconfig", interface, "hw", "ether", mac], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            subprocess.run(["ifconfig", interface, "up"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            print(f"\n[+] Tu direccion MAC ha sido cambiada exitosamente. Tu nueva direccion mas es: {mac}")
            sleep(0.5)
        except:
            subprocess.run(["ifconfig", interface, "up"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"\n[!] Ha surgido un error, verifique los permisos de ejecucion (sudo).")
    else:
        print("\n[!] La interfaz ingresada es invalida")


def main():
    args = get_arguments()
    change_mac(args.interface)

if __name__ == '__main__':
    main()