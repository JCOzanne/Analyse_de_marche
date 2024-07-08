


# Scraper des Livres depuis "Books to Scrape"

Ce script Python permet de récupérer les informations des livres depuis le site "Books to Scrape" :
-	 l’url de la page du livre (product_page_url),
-	Le code universel du livre (universal_product_code),
-	le titre (title),
-	le prix avec taxes (price_including_tax),
-	le prix sans taxes (price_excluding_tax),
-	le nombre de livres disponibles (number_available),
-	la description du livre (product_description),
-	la catégorie du livre (category),
-	l'évaluation du livre (review_rating),
-	l’url de l'image (image_url)

 Les données sont organisées dans des fichiers CSV classés par catégorie de livre, et les images de couverture sont téléchargées dans un répertoire local.



## Prérequis

- Python 3.12
- Bibliothèque Requests
- Bibliothèque BeautifulSoup4


## Installation

1. Clonez le dépôt :
git clone https://github.com/JCOzanne/Analyse_de_marche

2. Installez les dépendances :

Se référer au fichier requirements.txt :
pip install -r requirements.txt

## Utilisation

Exécutez le script main.py pour lancer le processus de scraping :
python main.py

Ce script effectuera les opérations suivantes :
•	Récupération des données des livres depuis le site "Books to Scrape".
•	Organisation des livres dans des fichiers CSV par catégories.
•	Téléchargement des images de couverture des livres dans le répertoire book_images.

## Créer l’environnement virtuel

cd Analyse_de_marche
python -m venv venv

# Activer l’environnement virtuel

source env/bin/activate (macOS et Linux) 
 env\Scripts\activate (Windows)

Structure du Répertoire
•	main.py : Script principal Python pour le scraping.
•	book_images/ : Répertoire pour stocker les images de couverture téléchargées.
•	nom_de_la_categorie.csv : Fichiers CSV contenant les détails des livres pour chaque catégorie.

Notes
•	Chaque livre est enregistré avec son titre comme nom de fichier d'image après nettoyage des caractères spéciaux.


### Explications du README :

- **Prérequis** : Liste des logiciels et bibliothèques nécessaires pour exécuter le script.
- **Installation** : Instructions pour cloner le dépôt et installer les dépendances.
- **Utilisation** : Comment démarrer le script de scraping.
- **Structure du Répertoire** : Description des fichiers et répertoires créés par le script.
- **Notes** : Informations supplémentaires sur le fonctionnement du script, comme le nettoyage des caractères spéciaux dans les noms de fichiers d'images.

