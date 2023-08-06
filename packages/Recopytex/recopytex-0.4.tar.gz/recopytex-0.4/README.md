# Recopytex

Editeur de note et de devoir pour mes classes

## Utilisation 

    recopytex start

Cela va créer la base de donnée recopytex.db. Toutes les données seront stockés à l'intérieur.

## Installation pour le développent  (non téstée...!)

### Python

    python -m venv venv
    source venv/bin/activate
    pip install .

### Vuejs et node

En supposant que *yarn* est déjà installé

    cd front_src/
    yarn install


### Mise en route

#### Lancer l'app flask

    python run.py

#### Server dev vuejs

    cd front_src/
    yarn run dev

Il faut penser à lancer l'app flask sinon les appels à l'api ne marcheront pas!

### Exporter l'app vue dans Recopytex

    cd front_src/
    yarn run build

Après ça, plus besoin de yarn. Il suffit de lancer l'app flask


## Création d'un paquet

- Exporter l'app vue dans Recopytex

    cd front_src/
    yarn run build

- Mettre à jour le setup.py (numéro de la version)
- Créer le package

    python setup.py sdist

- Upload vers Pypi

    twine upload dist/{nom}

- On crée le tag de version à partir de la branch master!

