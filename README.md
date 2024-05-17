## Password Manager

### fonctionnalitées

- ajout de mot de passe 

- suppression de mot de passe

- modification de mot de passe

- recherche de mot de passe grace à des mots clés (url, username)

- generation de mot de passe aléatoire possible :

    - avec ou sans caractères spéciaux

    - choix de la taille du mot de passe (supérieur a 12 caractères)

- expérience multi utilisateur

- chiffrement des données & hash du mot de passe maitre dans le json

### Comment l'utiliser

```
    python3 master.py
```

1. Créer son utilisateur et/ou authentification

2. Ajouter un nouveau mot de passe avec la commande : create

    1. choisissez de générer ou écrire manuellement un mot de passe sécurisé

3. trier les differents mot de passe par username ou url grace à la commande : search

4. modifier ou supprimer des mots de passes grace aux commande : modify, delete

5. modifier le compte maitre avec la commande : modify -account