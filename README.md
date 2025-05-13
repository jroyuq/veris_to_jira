# Veris to jira
Ce projet a été effectué dans le cadre d'une tâche pratique ayant pour objectif de transférer des incidents depuis la base de données VERIS (VCDB) vers la plateforme JIRA.

# objectif

Le but premier est d'offrir une solution simple et efficace qui permet de : 

- Consulter un fichier CSV qui contient des incidents de sécurité structurés en suivant le modèle VERIS. 
- Générer de manière automatique une table PostgreSQL pour la conservation de ces incidents. 
- Introduire les informations dans la base de données locale. 
- Prévoir l'intégration future avec JIRA en utilisant l'API REST (ceci n'est pas présent dans ce dépôt). 

# contenu du projet

- `import_vcdb_assets_fixed.py` : Script de premier plan servant à l'importation des incidents VERIS dans PostgreSQL. 
- `vcdb_supabase_final_datetime_clean_with_asset.csv` : Fichier de données épuré au format VERIS. 
- Scripts additionnels utilisés lors des tests (`testconnection.py`, `log.txt`, etc.) 

# prérequis

- Python version 3.x 
- PostgreSQL configuré et installé en local 
- Bibliothèques Python : 
- `pandas` 
- `psycopg2`

Attention :  Assurez-vous de modifier les identifiants de connexion à la base PostgreSQL si vous testez ce script sur un autre poste.

## Comment exécuter le script

1. Cloner ce dépôt :
   ```bash
   git clone https://github.com/jroyuq/veris_to_jira.git
   cd veris_to_jira

Remarque : 
•	Ce script est destiné à une utilisation locale à des fins d’apprentissage.
•	Il pourrait être amélioré pour créer automatiquement des tickets dans JIRA grâce à l’API REST de JIRA.


