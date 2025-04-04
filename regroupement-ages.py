import pandas as pd
import re

def categorize_age(age):
    """Transforme un âge en catégorie d'âge."""
    if isinstance(age, str):  # On vérifie si l'âge est une chaîne de caractères
        match = re.search(r'\d+', age)  # Extraction du premier nombre trouvé
        if match:
            age = int(match.group())
        else:
            return "Non spécifié" # On indique si la case est vide
    elif pd.isna(age):  # Si les valeurs ne sont pas exploitables
        return "Non spécifié"
    
    # Catégorisation par tranche d'âge
    if age < 18:
        return "Moins de 18"
    elif 18 <= age <= 25:
        return "18 - 25"
    elif 26 <= age <= 35:
        return "26 - 35"
    elif 36 <= age <= 50:
        return "36 - 50"
    elif 51 <= age <= 70:
        return "51 - 70"
    elif age >= 71:
        return "71 et plus"
    return "Non spécifié"

def process_csv(input_file, output_file):
    """Charge le fichier CSV, applique la transformation et sauvegarde le fichier modifié."""
    # On charge le fichier CSV
    df = pd.read_csv(input_file)
    
    # On vérifie si la colonne "âge" existe
    age_column = next((col for col in df.columns if "âge" in col.lower()), None)
    if not age_column:
        raise ValueError("Colonne contenant les âges introuvable dans le fichier.")
    
    # On remplace la colonne des âges par la catégorie d'âge
    df[age_column] = df[age_column].apply(categorize_age)
    
    # Sauvegarde du fichier modifié
    df.to_csv(output_file, index=False)
    print(f"Fichier sauvegardé sous : {output_file}")

# Utilisation
input_file = "results-survey293392 -27.3.csv"
output_file = "results-survey-modified-ages.csv"
process_csv(input_file, output_file)