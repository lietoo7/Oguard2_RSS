# Oguard2_RSS
Agrégateurs de flux RSS
Ce projet est une station de veille cyber (OSINT) utilisant PyQt6 pour visualiser des flux RSS sous forme de réseau de nodes dynamiques.

## Prérequis
- Python 3.9 ou une version supérieure.
- Accès Internet (pour la récupération des flux).
## Installation rapide
1. Cloner ou copier les fichiers
Assurez-vous d'avoir la structure de fichiers suivante dans votre dossier de projet :
```Plaintext

PROJET/
├── main.py
├── utils/
│   ├── cache_manager.py
│   ├── config_handler.py
│   └── logger_custom.py
└── data/ (sera créé automatiquement)
```

2. Créer l'environnement virtuel (venv)
Ouvrez un terminal dans le dossier du projet :

Sur Windows :

```Bash

python -m venv venv
venv\Scripts\activate
```
Sur macOS/Linux :
```Bash

python3 -m venv venv
source venv/bin/activate
```
3. Installer les dépendances
Une fois l'environnement activé, installez les bibliothèques nécessaires :

```Bash

pip install PyQt6 feedparser
```
## Utilisation
Lancer l'application
```Bash

python main.py
``` 
