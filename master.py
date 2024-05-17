from cryptography.fernet import Fernet
import Authentication as auth
import AddUser as adduser
import Command as command

from colorama import init, Style
init(autoreset=True)

def login():

    # Première interface qui propose un choix entre l'authentification et la création d'un nouveau coffre sécurisé 
    print('''
        
    _   _            _                  ______             
    | \ | |          | |                 | ___ \            
    |  \| | ___ _   _| |_ _ __ ___  _ __ | |_/ /_ _ ___ ___ 
    | . ` |/ _ \ | | | __| '__/ _ \| '_ \|  __/ _` / __/ __|
    | |\  |  __/ |_| | |_| | | (_) | | | | | | (_| \__ \__ |
    \_| \_/\___|\__,_|\__|_|  \___/|_| |_\_|  \__,_|___/___/
                                                            
    ''')
    print('''
        1. Log in
        2. Create account
    ''')
    user_choice_var = "Type " + Style.BRIGHT + "1" + Style.NORMAL + " or " + Style.BRIGHT + "2" + Style.NORMAL + ": "
    user_choice = input(f"{user_choice_var}")
    if user_choice == '2':
        # Permet la création d'un utilisateur et de son coffre sécurisé 
        adduser.add_user()

    # Boucle permettant l'intéraction avec le coffre via les commandes
    username = auth.authentication_input()
    run = 1
    loaded_list_password = []
    while run:
        run,loaded_list_password= command.display_menu(username,loaded_list_password)
    return 0

login()