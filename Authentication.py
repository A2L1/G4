import ManageDB as db
import InteractPassword as ipwd
import getpass

from colorama import init, Fore, Style
init(autoreset=True)

def authentication_input():
    # Fonction permettant le contrôle du nombre de tentatives effectuées ainsi que la validité des informations fournies 
    isAuth = False
    attempt = 0
    while not isAuth :
        if attempt == 3:
            print(Fore.RED + 'to many attempt.')
            exit()
        input_username = input("Enter your Username : ")
        input_master_password = getpass.getpass("Enter your Master password : ")
        hashed_user_input_master_password = ipwd.hash_master_password(input_master_password)
        isAuth = verify_credential(input_username, hashed_user_input_master_password)
        attempt += 1
    return input_username

def verify_credential(username, hashed_password):
    # Fonction pour vérifier la validité des identifiants avec les identifiants en base de données
    try :
        data = db.open_json_file()
        credential_db = db.get_login_user(username,data)
    except :
        print(Fore.RED + "\nCredential don't match\n")
        return False
    
    if credential_db == ipwd.to_base_64(username, hashed_password):
        print(Fore.GREEN + "\nlogin success\n")
        return True
    
    print(Fore.RED + "\nCredential don't match\n")
    return False