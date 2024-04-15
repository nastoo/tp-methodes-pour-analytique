# Analyse des Jeux Olympiques d'été 2024 : Modélisation de la Prédiction des Médailles

## Introduction
Bienvenue dans le cadre de ce travail pratique où nous explorerons et développerons un modèle de prédiction du nombre total de médailles que chaque pays inscrit pourrait remporter aux Jeux Olympiques d'été 2024 à Paris. Notre point de départ pour cette tâche sera le jeu de données "120 years of Olympic history: athletes and results". 

## Récupération de ce dépôt Git:
### Clonage du repository Git
```bash
git clone https://github.com/nastoo/tp-methodes-pour-analytique
```
### Installation des dépendances
```bash
pip install -r requirements.txt
```
### Exécution du Notebook Projet.ipynb
Au moyen de Jupyter Notebook, nous conseillons de passer par Anaconda. Plus de détails ici : https://www.anaconda.com/download

## Dataframes fournis
Les fichiers "athlete_events.csv" et "noc_regions.csv" sont extraits du jeu de données intitulé "120 years of Olympic history: athletes and results", partagé par rgriffin sur Kaggle à l'adresse suivante : [120 years of Olympic history: athletes and results.](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results "120 years of Olympic history: athletes and results.")
Le fichier "dictionary.csv" provient du jeu de données "Olympic Sports and Medals, 1896-2014", publié par The Guardian sur Kaggle, accessible via le lien suivant : [Olympic Sports and Medals, 1896-2014.](https://www.kaggle.com/datasets/the-guardian/olympic-games "Olympic Sports and Medals, 1896-2014.")

## Utilisation de données supplémentaires
Nous avons également à notre disposition le fichier "dictionary.csv" issu du jeu de données "Olympic Sports and Medals, 1896-2014" posté par The Guardian sur Kaggle. 
En plus de cela, nous avons inclus des données des JO de Tokyo, absents de ce dataframe, à l'adresse suivante https://www.kaggle.com/datasets/piterfm/tokyo-2020-olympics, ainsi que des données provenant de Wikipédia et de la Banque Mondiale (https://data.worldbank.org/).

## Résultats
Les résultats des prédictions ont été exportés dans `/data/2024_predictions.csv`. Les détails sont dans le notebook, mais nous avons choisi d'utiliser un algorithme RandomForestRegressor, qui est ressorti comme étant l'un des plus performants dans nos tests. 
