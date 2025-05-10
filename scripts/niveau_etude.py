import pandas as pd
import re
from collections import Counter
from collections import defaultdict

# Chargement du fichier Excel
file_path = 'Resultats_homogenises.xlsx'
df = pd.read_excel(file_path, engine="openpyxl")

# Nettoyage des noms de colonnes
df.columns = df.columns.str.strip().str.replace('\xa0', '', regex=False)

# Nom de la colonne nettoyée
col_etude = "Votre niveau d'études?"

# Extraction, suppression des NaN et espaces
col_data = df[col_etude].dropna().astype(str).str.strip()

# Normalisation
def normaliser(val):
    val = val.lower()
    val = val.replace("é", "e").replace("è", "e").replace("ê", "e")
    val = val.replace("+", " + ")
    val = re.sub(r"\s+", " ", val)  # Nettoyage des espaces multiples
    return val.strip()

# Application de la normalisation
col_data_norm = col_data.apply(normaliser)

# Création du dictionnaire fréquence
frequences = dict(Counter(col_data_norm))
#print(frequences)


###################################################"

groupes = {
    "inférieur à Bac": [
        'sans diplôme', '3eme', 'lycee', 'je passe le bac cette annee.', '1ere annee lycee professionnel', 'terminale', 'cap', 'cap patissier, cap chocolatier, btm chocolatier', 'bep', 'bac pro', 'bac pro secretariat'
        ],
    "Bac 1 à 2": [
        'bac', 'baccalaureat', 'niveau bac', 'bac + 1', 'bac + 2', 'b + 2', 'bientôt bac + 2', 'niveau bts' ,'bts', '2eme annee etude sup','bac + bts'
        ],
    "Licence": [
        'licence 2', 'licence', 'licence pro', 'licence professionnelle','l1', 'licence 1', 'bac + 3 en cours', 'bac +3', 'en cours de troisieme annee d’une licence',
        '3e annee de licence', 'l3', '3eme annee licence histoire', 'bac + 3/ de', 'bac + 3'
        ],
    "Master ou plus": [
        'master', 'master 1', 'bac + 5', 'bac + 5 master', 'bac + 5 grade master', 'doctorat', 'hdr'
    ]
}
#Source : Onisep

# Calcul du total par groupe
resultats = defaultdict(int)

# Mapping inverse pour rechercher dans data
flat_mapping = {}
for groupe, labels in groupes.items():
    for label in labels:
        flat_mapping[label] = groupe

# Calcul des fréquences par groupe
for k, v in frequences.items():
    groupe = flat_mapping.get(k, "Autres")
    #Autres =
    resultats[groupe] += v

# Affichage du résultat final
#print(frequences)
#print("---====---")
#print(dict(resultats))

# Affichage des valeurs spécifiques d'une classe
"""
autres_vals = {k: v for k, v in frequences.items() if flat_mapping.get(k, "Autres") == "Autres"}

print("\n--- Valeurs dans 'Autres' ---")
for val, freq in autres_vals.items():
    print(f"{val}: {freq}")
"""

#########################"

# Création du mapping inversé
flat_mapping = {}
for groupe, labels in groupes.items():
    for label in labels:
        flat_mapping[label] = groupe

# Fonction de classification qui applique le groupe correct à chaque niveau d'étude
def niveau_etude(niv):
    if pd.isna(niv) or niv.strip() == "":  # Vérification pour un texte vide ou NaN
        return "Non spécifié"

    # Normaliser le texte
    niv = normaliser(niv)

    # Vérifier chaque groupe et ses labels
    for label, groupe in flat_mapping.items():
        if niv == label:
            return groupe

    # Retourner "Non spécifié" si aucun groupe ne correspond
    return "Non spécifié"


df[col_etude] = df[col_etude].apply(niveau_etude)
#print(df['groupe_etude'].value_counts()) pour les occurences

df.to_excel('Resultats_homogenises.xlsx', index=False)

# Aperçu des résultats
#print(df[[col_etude]].head())
