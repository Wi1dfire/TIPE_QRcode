# TIPE QRcode

Projet de TIPE sur la génération et la lecture de QR codes.

## Description

Ce projet vise à explorer les méthodes de création, d'encodage et de décodage des QR codes à l'aide de Python.

## Fonctionnalités

- Génération de QR codes personnalisés
- Lecture et décodage de QR codes à partir d'images
- Interface utilisateur simple

## Utilisation
Pour utiliser ce projet, assurez-vous d'avoir Python installé ainsi que les dépendances requises. Installez-les avec :

```bash
pip install -r requirements.txt
```

Ensuite, vous pouvez générer ou lire des QR codes en utilisant les commandes ci-dessous.

## Description des fichiers

- **main.py** : Le point d’entrée du programme. Permet de générer ou lire des QR codes selon les arguments fournis en ligne de commande.
- **requirements.txt** : Liste des dépendances Python nécessaires pour exécuter le projet.
- **README.md** : Ce fichier de documentation, expliquant l’utilisation et la structure du projet.
- **Autres fichiers :**  
  - **fonctionsbase.py** : Répertoire des fonctions de base utile pour transformer les objets que l'on utilise.
  - **structure.py** : Construit les motifs immuable du QRcode et les outils necessaire à la constructuion du squelette du QRcode.  
  - **informationsvesion.py** : Encode les informations de version  
  - **loisempiriques.py** : Créé une base de donnée de QRcode dans image_test_QRcode\empirique\QRcode pour récupérer des informations sur la structure des QRcodes de manière empirique.   
  - **image_test_QRcode\empirique\loisempiriques.csv** : Contient les données empiriques récupérées par loisempiriques.py.  
  - **construction.py** : Utilise fonctionsbase.py, informationsvesion.py et loisempiriques.csv pour construire le squelette du QRcode.  
  - **evaluation.py** : Contient les critères de lisibilité et attribut un score de lisibilité à un QRcode  
  - **informationsformat.py** : Encode les informations de format
  - **mask.py** : Gère les masques. Contient chacun de leur motif, applique le masque permettant un lisibilité optimal du QRcode grâce à evaluation.py et inscrit les informations de format déterminées par informationsformat.py sur ce dernier. Peut également retrouver le masque utilisé dans un QRcode.  
  - **fonctionsutiles.py** : Répertoire des fonctions dont l'utilisation est restreinte à la création de QRcode

### Générer un QR code

```bash
python main.py QRcode "Votre message ici" <niveau_correction>
```

### Lire un QR code

```bash
python main.py read_QR chemin/vers/image.png
```

## Auteurs

- TRIOUX Marius

## Licence

Ce projet est sous licence **Creative Commons Attribution - Pas d’Utilisation Commerciale (CC BY-NC 4.0)**.

- Vous devez créditer l’auteur.
- L’utilisation commerciale est interdite.

Pour plus d’informations, consultez la [licence complète](https://creativecommons.org/licenses/by-nc/4.0/deed.fr).