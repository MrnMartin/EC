import pandas as pd

def compte_age(input_file):
    """Compte le nombre de personnes pour chaque tranche d'âge à partir d'un fichier CSV"""
    # On charge le fichier CSV
    df = pd.read_csv(input_file)
    
    # On vérifie si la colonne "âge" existe
    age_column = next((col for col in df.columns if "âge" in col.lower()), None)
    if not age_column:
        raise ValueError("Colonne contenant les âges introuvable dans le fichier.")

    # Initialisation des compteurs
    count_u21 = 0
    count_2125 = 0
    count_2644 = 0
    count_o44 = 0
    count_ns = 0

    # Comptage des tranches d'âge
    for age in df[age_column]:
        if isinstance(age, str):
            age = age.strip()
        if age == "20 ans et moins":
            count_u21 += 1
        elif age == "21 - 25":
            count_2125 += 1
        elif age == "26 - 44":
            count_2644 += 1
        elif age == "45 ans et plus":
            count_o44 += 1
        elif age == "Non spécifié":
            count_ns += 1

    # Affichage des résultats
    print("20 ans et moins :", count_u21)
    print("21 - 25 ans    :", count_2125)
    print("26 - 44 ans     :", count_2644)
    print("45 ans et plus     :", count_o44)
    print("Non spécifié    :", count_ns)

# Utilisation
input_file = "resultat-regroupement-ages.csv"
compte_age(input_file)
