import pandas as pd

# Chargement du fichier Excel
file_path = '../corpus/results-survey293392-4.4.xlsx'
df = pd.read_excel(file_path)

# Nettoyage des noms de colonnes : supprime les espaces et caractères spéciaux invisibles
df.columns = df.columns.str.strip().str.replace('\xa0', '', regex=False)

# Affichage des colonnes pour vérification
#print("Colonnes disponibles :", df.columns.tolist())

# Nom de la colonne après nettoyage
col_pays = 'Votre pays de naissance?'

# Listes de pays
france = ["France", "france", "fr", "FR", "FRANCE", "Je suis née en France", "France 🇫🇷"]
burundi = ["burundi", "Burundi"]
italie = ["italie", "Italie"]
algerie = ["Algérie"]
rwanda = ["Rwanda"]

# Fonction de classification
def pays_naissance(pays):
    if pd.isna(pays):
        return "Autres"
    pays = str(pays).strip().lower()
    if pays in [x.lower() for x in france]:
        return "France"
    else:
        return "Autres"

# Application de la fonction à la colonne
df[col_pays] = df[col_pays].apply(pays_naissance)

# Sauvegarde du fichier
df.to_excel('Resultats.xlsx', index=False)

# Aperçu des résultats
print(df[[col_pays]].head())
