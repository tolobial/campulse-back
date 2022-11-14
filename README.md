# PlanA

## Health

### Master

[![pipeline status](https://git.unistra.fr/di/plan_a/plana/badges/master/pipeline.svg)](https://git.unistra.fr/di/plan_a/plana/-/commits/master)
[![coverage report](https://git.unistra.fr/di/plan_a/plana/badges/master/coverage.svg)](https://git.unistra.fr/di/plan_a/plana/-/commits/master)

### Develop

[![pipeline status](https://git.unistra.fr/di/plan_a/plana/badges/develop/pipeline.svg)](https://git.unistra.fr/di/plan_a/plana/-/commits/develop)
[![coverage report](https://git.unistra.fr/di/plan_a/plana/badges/develop/coverage.svg)](https://git.unistra.fr/di/plan_a/plana/-/commits/develop)

## Description

Création d'une application web pour la gestion des associations étudiantes et de leurs projets.

## Prérequis

python (>=3.9), pip, virtualenv, virtualenvwrapper

## Installation

### Lancer la base de données PostgreSQL et le service de mail en local avec Docker

À la racine du projet :

```sh
$ sudo docker-compose up -d
```

Ou
```sh
$ sudo docker compose up -d
```

Pour stopper le service :
```sh
$ sudo docker-compose down
```

### Créer l'environnement virtuel

```sh
$ mkvirtualenv plana
```

### Configurer les variables d'environnement nécessaires (fichier postactivate du venv)

```sh
export DJANGO_SETTINGS_MODULE=plana.settings.dev
```

Les actions suivantes se font avec le virtualenv activé :

### Installer les dépendances de dev dans le virtualenv

```sh
$ pip install -r requirements/dev.txt
```

### Migrer les modèles de données dans la base de données

```sh
$ python manage.py makemigrations
$ python manage.py migrate
```

### Charger les fixtures dans la base de données

```sh
$ python manage.py loaddata plana/apps/*/fixtures/*.json
```

## Développement

### Lancer du serveur en local

```sh
$ python manage.py runserver
```

### Détecter de nouvelles chaînes de caractères à traduire

```sh
$ python manage.py makemessages -l fr --extension html,txt,py

```

### Linter les fichiers

```sh
$ black plana
```
