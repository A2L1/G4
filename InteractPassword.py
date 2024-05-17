from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import base64
import hashlib
import requests
import time

import string
import secrets

from tkinter import Tk

from colorama import init, Fore, Style
init(autoreset=True)

load_dotenv(dotenv_path=".env")

ALPHABET = string.ascii_letters + string.digits
SPECIAL_ALPHABET = ALPHABET + '-_=+#$@*'

def hash_master_password(password):
    # Fonction retournant le hash (SHA256) d'un mot de passe donné 
    hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return hashed_password

def to_base_64(username, password):
    # Fonction retournant un string en base64 de la paire username:hashPassword
    clear_credential = f"{username}:{password}"
    base64_credential = base64.b64encode(clear_credential.encode('utf-8')).decode('utf-8')
    return base64_credential

def initialise_key():
    # Fonction permettant de récupérer ou de créer la clé de chiffrement pour les mots de passe dans le .env
    try :
        FERNET_KEY = bytes(os.getenv("FERNET_KEY"), 'utf-8')
        FERNET_KEY = base64.b64decode(FERNET_KEY)
    except TypeError:
        FERNET_KEY = Fernet.generate_key()
        FERNET_KEY = base64.b64encode(FERNET_KEY)
        with open('.env','a') as f:
            f.write('FERNET_KEY=')
            f.close()
        with open('.env','ab') as f:
            f.write(FERNET_KEY)
            f.close()
        with open('.env','a') as f:
            f.write('\n')
            f.close()
    return FERNET_KEY

def initialise_cipher():
    # Fonction initialisant le cipher pour le chiffrement des mots de passe
   
    key = initialise_key()
    FERNET_CIPHER = Fernet(key)
    return FERNET_CIPHER 

def encrypt_password(cipher, password):
   # Fonction retournant le mot de passe chiffré donné 
   return cipher.encrypt(password.encode()).decode()

def decrypt_password(cipher, encrypted_password):
   # Fonction retournant le mot de passe déchiffré donné 
   return cipher.decrypt(encrypted_password.encode()).decode()

def generate_user_password(len_password, list):
    # Fonction permettant la génération aléatoire d'un mot de passe en fonction de la longueur
    password_list = []
    for i in range(0, int(len_password) + 1,):
        password_list.append(secrets.choice(list))
    password = "".join(password_list)
    return password

def generate_password(len_password):
    # Fonction prenant en charge la validation pour les choix de génération des mots de passes
    print('Do you want a password with special character ? :')
    user_choice = input('Y/N : ')
    while user_choice != 'Y' and user_choice != 'N':
        user_choice = input('choice between Y/N : ')
    if user_choice == 'Y':
        user_choice = SPECIAL_ALPHABET
    elif user_choice == 'N':
        user_choice = ALPHABET
    password = generate_user_password(len_password, user_choice)
    copy_password_clipboard(password)
    return password

def copy_password_clipboard(password):
    # Fonction permettant la copie dans le presse papier d'un mot de passe généré
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(password)
    r.update()
    print(Fore.GREEN + Style.BRIGHT + '\npassword copied to clipboard\n')

def hash_password_hibp(password):
    #Fonction retournant les 5 premiers et dernier caractères du hash d'un mot de passe
    sha1_password = hashlib.sha1(password.encode()).hexdigest().upper()
    return sha1_password[:5], sha1_password[5:]

def check_password_pwned(password):
    # Fonction vérifiant via l'API HaveIBeenPwned si le mot de passe est compromis
    prefix, suffix = hash_password_hibp(password)

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    if response.status_code == 200:
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                print(Fore.YELLOW +"AVERTISSEMENT")
                print('Attention votre mot de passe est connu sur internet :' + Fore.RED +" ( "+ str(count) + " ) fois\n"+Fore.WHITE +"Nous vous conseillons de le modifier rapidement")
                print("Ajout de l'élément ...")
                time.sleep(4)
    return 0


def check_vault_pwned(password):
    # Fonction vérifiant la sécurité de l'ensemble des mots de passe contenu dans un vault
    prefix, suffix = hash_password_hibp(password)

    response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")

    if response.status_code == 200:
        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                print('Ce mot de passe est connu sur internet : ' + Fore.RED + password +" ( "+ str(count) + " ) fois\n")
                return 1
    return 0