import ManageDB as db
import InteractPassword as ipwd
import uuid
import getpass

from colorama import init, Fore, Style
init(autoreset=True)

def input_url():
    # Fonction pour la saisie de l'URL
    return input("Enter URL : ")

def input_username():
    # Fonction pour la saisie du nom d'utilisateur
    return input("Enter Username : ")

def input_password():
    # Fonction pour la saisie d'un mot de passe

    ## Vérification de la bonne écriture du mot de passe avec une double saisie
    first_password = getpass.getpass("Enter a password : ")
    second_password = getpass.getpass("Enter same password : ")
    while first_password != second_password:
        print("Passwords don't match.")
        first_password = getpass.getpass("Enter a password : ")
        second_password = getpass.getpass("Enter same password : ")
    ## Vérification via API que le mot de passe n'est pas compromis 
    ipwd.check_password_pwned(first_password)
    ## Encryption pour stocker dans la base de données
    encrypted_password = ipwd.encrypt_password(ipwd.initialise_cipher(),second_password)
    return encrypted_password

def choice_create_password():
    # Fonctions permettant de choisir entre la saisie manuelle d'un mot de passe et une génération automatique

    print('Do you want to generate your password or write it manualy ? : ')
    print(f"1. generate it")
    print(f"2. write it manualy")

    ## Contrôle de saisie
    choice = input("1/2 : ")
    while choice not in ['1', '2']:
        print("Invalid choice")
        choice = input("1/2 : ")

    ## Définition du mot de passe généré aléatoirement
    if choice == '1':
        choice_len = input("Choose length of the password : ")
        while not choice_len.isnumeric():
            print("This is not a number.")
            choice_len = input("Choose length of the password")
    ## Vérification via API que le mot de passe n'est pas compromis 
        password = ipwd.generate_password(choice_len)
        print('your new password : \n\n   ' + Fore.CYAN + password + "\n")
    ## Encryption pour stocker dans la base de données
        encrypted_password = ipwd.encrypt_password(ipwd.initialise_cipher(),password)
        return encrypted_password
    ## Appel de la fonction de saisie manuelle du mot de passe 
    elif choice == '2':
        return input_password()

def create_item(user):
    # Fonction regroupants toutes les saisies concernant la création d'un item
    item = {}
    printListe = []
    file_memory = db.open_json_file()
    user_memory = db.get_user_dB(user,file_memory)
    list_passwords = db.get_all_password(user_memory)

    item['id'] = str(uuid.uuid4())
    item["url"] = input_url()
    item["username"] = input_username()
    item["password"] = choice_create_password()
    printListe.append(item)
    print_liste_passwords(printListe)
    list_passwords.append(item)

    user_memory["listpassword"] = list_passwords
    file_memory[user] = user_memory
    db.write_in_dB(file_memory)

def print_liste_passwords(liste_password):
    # Fonction d'affichage pour une liste de mot de passe donnée
    for element in liste_password:
        print('='*50)
        print(str(liste_password.index(element))+" : id : "+element["id"])
        print("    url : "+element["url"])
        print(Style.BRIGHT + "    username : "+element["username"])
        decrypted_password = ipwd.decrypt_password(ipwd.initialise_cipher(),element["password"])
        print(Style.BRIGHT + "    password : "+decrypted_password)
        print('='*50)

def modify_item(user, item_id):
    # Fonction prenant en charge la modification d'un item dans la base de données 
    file_memory = db.open_json_file()
    user_memory = db.get_user_dB(user,file_memory)
    list_passwords = db.get_all_password(user_memory)
    for item in list_passwords:
        if item['id'] == item_id:
            choice_modify_item(item)
    user_memory["listpassword"] = list_passwords
    file_memory[user] = user_memory
    db.write_in_dB(file_memory)

    return 0

def choice_modify_item(item):
    # Fonction controlant la saisie pour effectuer les choix de modifications sur un item de la base de données 
    print('What do you want to change ? : ')
    print(f"1. url: {item['url']}")
    print(f"2. username: {item['username']}")
    print(f'3. password : {ipwd.decrypt_password(ipwd.initialise_cipher(),item["password"])}')
    choice = input("1/2/3 : ")
    while choice not in ['1', '2', '3']:
        print(Fore.RED + "Invalid choice")
        choice = input("1/2/3 : ")
    if choice == '1':
        url = input_url()
        item['url'] = url
    elif choice == '2':
        username = input_username()
        item["username"] = username
    elif choice == '3':
        password = choice_create_password()
        item["password"] = password

    return item

def delete_item(user, item_id):
    # Fonction gérant la suppression d'un item dans la base de données
    file_memory = db.open_json_file()
    user_memory = db.get_user_dB(user,file_memory)
    list_passwords = db.get_all_password(user_memory)
    for item in list_passwords:
        if item['id'] == item_id:
            list_passwords.remove(item)
    user_memory["listpassword"] = list_passwords
    file_memory[user] = user_memory
    db.write_in_dB(file_memory)
    return 0