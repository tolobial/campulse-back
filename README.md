# PlanA

## Description

Création d'une application web pour la gestion des associations étudiantes et de leurs projets.

## Prérequis

python (>=3.9), pip, virtualenv, virtualenvwrapper

## Installation

### Lancer la base de données PostgreSQL et le service de mail en local avec Docker

A la racine du projet :

```
$ sudo docker-compose up -d
```

Et pour stopper le service :
```
$ sudo docker-compose down
```

### Création de l'environnement virtuel

```
$ mkvirtualenv plana
```

### Configuration des variables d'environnement nécessaires (fichier postactivate du venv)

```
export DJANGO_SETTINGS_MODULE=plana.settings.dev
```


Les actions suivantes se font avec le virtualenv activé :


### Installation des dépendances de dev dans le virtualenv

```
$ pip install -r requirements/dev.txt
```

### Migrer les modèles de données dans la base de données
```
$ python manage.py makemigrations
$ python manage.py migrate
```

### Chargement des fixtures dans la base de données
```
$ python manage.py loaddata associations_users auth_groups users user_groups account_email_addresses activity_fields associations institution_components institutions social_networks
```

## Lancement du serveur en local
```
$ python manage.py runserver
```

## Documentation des routes de l'application

### Commande pour mettre à jour automatiquement le fichier de documentation de l'API
```
$ python manage.py spectacular --file schema.yml
```

### URLs pour accéder à la documentation générée
- `/api/schema/` pour télécharger un fichier YAML contenant la documentation
- `/api/schema/swagger-ui/` pour consulter la documentation de l'API en mode Swagger
- `/api/schema/redoc/` pour consulter la documentation de l'API en mode Redoc
