import argparse
import signal
import subprocess
import os
from concurrent.futures import ThreadPoolExecutor

def def_handler(sig, frame):
    print("\n[!] Saliendo del programa...\n")
    os.exit(1)

signal.signal(signal.SIGINT, def_handler)

def get_arguments():

    parser = argparse.ArgumentParser(description="Herramienta para escanear host de red")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host o rango de red a escanear")

    args = parser.parse_args()
    
    return args.target

def parse_target(target_str):

    target_str_splitted = target_str.split('.') 
    first_three_oct = '.'.join(target_str_splitted[:3])

    if len(target_str_splitted) == 4:
        if '-' in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [ f"{first_three_oct}.{i}" for i in range(int(start), int(end)+1) ]
        else:
            return [target_str]
    else:
        return "\n[!] El formato de ip o rango de ip es invalido"

def host_discovery(target):
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(f"\t[+] Host encontrado: {target}\n")
    except (subprocess.TimeoutExpired, SystemExit):
        pass

def main():
    target_str = get_arguments()
    targets = parse_target(target_str)
    print(f"\n[+] Iniciando busqueda de Hosts activos: ")

    max_theaders = 100
    with ThreadPoolExecutor(max_workers = max_theaders) as executor:
        executor.map(host_discovery, targets)



if __name__ == '__main__':
    main()