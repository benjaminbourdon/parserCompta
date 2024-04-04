# ParserCompta

Il s'agit d'un algorythme écrit en Python dont la finalité est de générer automatiquement 
des messages de relance des debiteurs (comptes auxiliaires) à partir de l'outil
de comptabilité AssoConnect.

## Pré-requis

- Python 3.x

## Fonctionnement

### Préparation

Depuis AssoConnect, la liste des opérations comptables doit être exportée. 
Le fichier doit être placé au format .csv à la racine du projet. 
Le nom du fichier doit être export.csv.
Un example de fichier avec des fausses données est proposé.

Le message doit être rédigé dans le fichier modele-dette.html
Les variables disponibles sont les attributs publiques de la classe CompteAuxiliaire.

### Lancement et résultat

Le fichier main.py est le fichier a executer.
Il genère un fichier .html par personne débitrice dans un sous-dossier Sorties.
L'envoie doit se faire ensuite manuellement.