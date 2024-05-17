import ManageDB as db
import CrudItem as ci
import AddUser as adduser
import InteractPassword as ipwd
import time

from colorama import init, Fore, Style
init(autoreset=True)

COMMAND_LIST = ['search', 'modify', 'create', 'delete', '@exit']
LIST_ARGUMENT_OF = {
    'search' : ['-h', '-url', '-username'],
    'modify' : ['-h', '-item','-account'],
    'create' : [],
    'delete' : ['-h', '-n'],
    'check-security' : []
}

def search_command(command, user):
    # Fonction définissant le comportement de la commande en fonction des arguments

    ## Affichage du menu help de la commande
    if command[1] == '-h':
        print("="*50)
        print('''
        choice between :
            -username [text] : to search password by the username
            -url [text] : to search password by the URL
        ''')
        return 1
   
    ## Affichage de la liste de mots de passe en fonction de l'argument de recherche
    user_memory = db.get_user_dB(user,db.open_json_file())
    list_passwords = db.get_all_password(user_memory)

    loaded_list = []

    for item in list_passwords:
        if command[1] == '-url' and command[2] in item['url']:
            loaded_list.append(item)
        elif command[1] == '-username' and command [2] in item["username"]:
            loaded_list.append(item)

    ci.print_liste_passwords(loaded_list)
    return loaded_list

def modify_command(command, user, loaded_password_list):
    # Fonction définissant le comportement de la commande en fonction des arguments

    ## Affichage du menu help de la commande
    if command[1] == '-h':
        print("="*50)
        print('''
        you must load password with search command
            -item [index] : to modify the index item
            -account : to modify the master password
        ''')
        return 1
    ## Modification du mot de passe maitre 
    elif command[1] == '-account':
        modify_account_command(user)
        return 1
    
    ## Modifie l'élement, de la liste chargée (si une liste est chargée), définit en paramètre
    if not loaded_password_list:
        print(Fore.RED + 'No item lists have been loaded, please load an item list via the command search. ')
        return 0
    number_item = int(command[2])
    temp_load=[]
    temp_load.append(loaded_password_list[number_item])
    ci.print_liste_passwords(temp_load)
    print(Style.BRIGHT + 'Are you sure you want edit this item ?')
    choice = input("Y/N : ")
    while choice != 'Y' and choice != 'N':
        print(Fore.RED + "\nNot a valid answer.\n")
        print(Style.BRIGHT + 'Are you sure you want edit this item ?')
        choice = input("Y/N : ")
    if choice == "Y":
        ci.modify_item(user, temp_load[0]["id"])
    return 0

def modify_account_command(user):
    # Fonction modifiant le mot de passe maitre et l'inscrit dans la base de données
    file_memory = db.open_json_file()
    user_db = db.get_user_dB(user, file_memory)
    list_password=db.get_all_password(user_db)
    del file_memory[user]
    db.write_in_dB(file_memory)
    adduser.add_user(user,list_password)
    return 1

def delete_command(command, user, loaded_password_list):
    # Fonction définissant le comportement de la commande en fonction des arguments

    ## Affichage du menu help de la commande
    if command[1] == '-h':
        print("="*50)
        print('''
        you must load password with search command
            -n [index] : to delete the index item
        ''')
        return 1

    ## Supprime l'élement, de la liste chargée (si une liste est chargée), définit en paramètre
    if not loaded_password_list:
        print(Fore.RED + 'No item lists have been loaded, please load an item list via the command search. ')
        return 0
    number_item = int(command[2])
    temp_load=[]
    temp_load.append(loaded_password_list[number_item])
    ci.print_liste_passwords(temp_load)
    print('Are you sure you want delete this item ?')
    choice = input("Y/N : ")
    while choice != 'Y' and choice != 'N':
        print(Fore.RED + "\nNot a valid answer.")
        print(Style.BRIGHT + 'Are you sure you want delete this item ?')
        choice = input("Y/N : ")
    if choice == "Y":
        ci.delete_item(user, temp_load[0]["id"])
        print(Fore.GREEN + '\nPassword successful deleted\n')
    return 0

def create_command(user):
    # Fonction redirigeant vers la fonction de création d'un item
    ci.create_item(user)

def is_valid_command_and_arg(command):
    # Fonction permettant de controler la validité d'une commande  
    bool_valid_command = is_valid_command(command)
    bool_valid_arg = False
    if bool_valid_command:
        if command[0] != '@exit' and command[0] != 'create' and command[0] != 'check-security':
            bool_valid_arg = is_valid_args(command)
        else:
            bool_valid_arg = True

    ## Boucle pour le contrôle de la saisie de la commande
    while not (bool_valid_command and bool_valid_arg):
        print(" ".join(command))
        user_command = input(Fore.RED + '    is not a valid command : \n' + Fore.WHITE)
        command = user_command.split(" ")
        bool_valid_command = is_valid_command(command)
        if bool_valid_command:
            if command[0] != '@exit' and command[0] != 'create':
                bool_valid_arg = is_valid_args(command)
            else:
                bool_valid_arg = True
    return command

def is_valid_command(user_command_list):
    # Fonction renvoyant un booléen en fonction des différents critères de validité pour la commande

    is_command_in_list = user_command_list[0] in COMMAND_LIST
    is_len_3 = len(user_command_list) == 3
    is_len_2 = len(user_command_list) == 2 and user_command_list[1] == '-h'
    is_modify_master_password = len(user_command_list) == 2 and user_command_list[1] == '-account'
    is_command_exit = user_command_list[0] == '@exit'
    is_command_create = user_command_list[0] == 'create'
    is_command_check_security = user_command_list[0] == 'check-security'

    return (is_command_in_list and (is_len_3 or is_len_2 or is_modify_master_password)) or is_command_exit or is_command_create or is_command_check_security

def is_valid_args(command):
    # Fonction renvoyant un booléen en fonction de l'existence de l'argument pour la commande voulue

    argument_in_list = command[1] in LIST_ARGUMENT_OF[command[0]]
    return argument_in_list

def check_command(user):
    # Fonction permettant l'évaluation de l'ensemble des mots de passe sur l'API HaveIBeenPwned

    user_db = db.get_user_dB(user,db.open_json_file())
    user_vault = db.get_all_password(user_db)
    leaked_passwords =[]
    for item in user_vault:
        password = ipwd.decrypt_password(ipwd.initialise_cipher(),item['password'])
        if ipwd.check_password_pwned(password):
            tmp_list = [item]
            ci.print_liste_passwords(tmp_list)
            leaked_passwords.append(item)

    percentage = (len(leaked_passwords) / len(user_vault)) * 100

    ## Affiche le pourcentage de mots de passe existant dans des leaks disponibles sur Internet
    if 0 <= percentage < 31:
        print("Votre vault est sécurisé à : "+Fore.GREEN +f"{percentage:.2f}%")
    elif 31 <= percentage < 81:
        print("Votre vault est sécurisé à : "+Fore.YELLOW +f"{percentage:.2f}%")
    elif 81 <= percentage < 101:
        print("Votre vault est sécurisé à : "+Fore.RED +f"{percentage:.2f}%")


def display_menu(user, loaded_password_list):
    # Fonction affichant le menu des commandes disponibles et gère la commande saisie

    time.sleep(2)
    print("="*50)
    print("\n")
    print("Commands available :")
    print(Style.BRIGHT + '''
        - search
        - modify
        - create
        - delete
        - check-security
          
    (-h for help)
    ''')

    ## Controle la validité de la commande
    user_command = input(': ')
    user_command_list = user_command.split(" ")
    command = is_valid_command_and_arg(user_command_list)

    ## Appelle la fonction correspondante à la commande
    if command[0] == 'search':
        loaded_password_list = search_command(command, user)
        return 1,loaded_password_list
    elif command[0] == 'modify':
        modify_command(command, user, loaded_password_list)
        return 1, []
    elif command[0] == 'create':
        create_command(user)
        return 1,[]
    elif command[0] == 'delete':
        delete_command(command, user, loaded_password_list)
        return 1,[]
    elif command[0] == 'check-security':
        check_command(user)
        return 1,[]
    elif command[0] == '@exit':
        return 0,[]
    return 0