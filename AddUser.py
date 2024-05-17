import ManageDB as db
import InteractPassword as ipwd
import getpass

def write_user_in_json(username, password, list_password):
    # Fonction ajoutant l'utilisateur et son coffre sécurisé dans la base de donnée
    user_object = {
            "login" : f"{ipwd.to_base_64(username, password)}",
            "listpassword" : 
                list_password
        }
    file_memory = db.open_json_file()
    file_memory[username] = user_object
    db.write_in_dB(file_memory)

def new_password_check():
    # Fonction contrôle de saisie du mot de passe maitre lors de la création du compte
    first_password_input = getpass.getpass("Enter your new password (Above 12 character): ")
    while len(first_password_input) < 11:
        first_password_input = getpass.getpass("Please enter password Above 12 character: ")
    second_password_input = getpass.getpass("Re-enter your new password : ")
    if first_password_input != second_password_input:
        print("Passwords don't match")
        new_password_check()
    else :
        return second_password_input

def user_already_exist_check(username):
    # Fonction vérifiant si l'utilisateur saisie un nom d'utilisateur disponible (pas existant dans la base de donnée)
    try:
        file_memory = db.open_json_file()
        if db.get_login_user(username,file_memory):
            print('User already exist, choose another username : ')
            add_user()
    except KeyError:
        return username

def add_user(username_input="",list_password=[]):
    # Fonction rassemblant la vérification du mot de passe maitre et de la disponibilité du nom d'utilisateur
    if not username_input :
        username_input = input("Enter your username : ")
    password_input = str(new_password_check())
    ipwd.check_password_pwned(password_input)
    if user_already_exist_check(username_input):
        write_user_in_json(username_input, ipwd.hash_master_password(password_input),list_password)