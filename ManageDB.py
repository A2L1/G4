import json

def open_json_file():
    # Fonction permettant de retourner le contenu du fichier base de donnée
    with open('data.json', 'r') as file:
        data = json.load(file)
        file.close()
    return data

def get_user_dB(user,db):
    # Fonction retournant les données d'un utilisateur 
    return db[user]

def get_login_user(user,db):
    # Fonction récupérant les données d'authentifications d'un utilisateur donné
    db_user = get_user_dB(user,db)
    return db_user["login"]

def get_all_password(db_user):
    # Fonction récupérant l'ensembles du coffre d'un utilisateur
    return db_user["listpassword"]

def write_in_dB(db):
    # Fonction permettant de réécrire les nouvelles données dans le fichier base de données
    with open('data.json','w') as f:
        json_object = json.dumps(db, indent=4)
        f.write(json_object)
        f.close()

