import pandas as pd
from collections import Counter

def compte_age(input_file):
    """Compte le nombre de personnes pour chaque tranche d'âge à partir d'un fichier CSV"""
    # On charge le fichier CSV
    df = pd.read_csv(input_file)
    
    # On vérifie si la colonne "âge" existe
    age_column = next((col for col in df.columns if "âge" in col.lower()), None)
    if not age_column:
        raise ValueError("Colonne contenant les âges introuvable dans le fichier.")

    # On ajoute les ages à une liste
    liste_ages = []
    for age in df[age_column]:
        liste_ages.append(age)
    liste_ages.sort()

    # Comptage des âges
    compteur = Counter(liste_ages)

    # Affichage des résultats
    for age, occurrence in compteur.items():
        print(f"L'âge {age} apparait {occurrence} fois.")

# Utilisation
input_file = "resultats-ages-individuels-video1.csv"
compte_age(input_file)
