import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Nom de la vidéo à traiter
video = "video5"
print("Pour :", video)

# Créer le dossier de sortie s’il n’existe pas
output_dir = f"graphs_{video}"
os.makedirs(output_dir, exist_ok=True)

# Charger le fichier Excel
df = pd.read_excel(f"{video5}.xlsx")

#############################################################################################
# 1. Détection dynamique des colonnes émotions et excessivité
colonnes_emotions = [col for col in df.columns if re.search(r"Quelle émotion ressentez-vous.*\[(.*?)\]", col)]
colonnes_excessivite = [col for col in df.columns if re.search(r"Trouvez-vous cette vidéo excessive.*\[(.*?)\]", col)]

# 2. Renommage dynamique des colonnes
def simplifier_colonnes(colonnes):
    colonnes_nettoyees = []
    for col in colonnes:
        if "Quelle émotion ressentez-vous" in col:
            match = re.search(r"\[(.*?)\]", col)
            label = match.group(1) if match else "émotion"
            colonnes_nettoyees.append(f"émotion_{label.strip().lower()}")
        elif "Trouvez-vous cette vidéo excessive" in col:
            match = re.search(r"\[(.*?)\]", col)
            label = match.group(1) if match else "excessif"
            label_clean = re.sub(r"\s+", "_", label.strip().lower())
            colonnes_nettoyees.append(f"excessif_{label_clean}")
        else:
            colonnes_nettoyees.append(col.lower().replace(" ", "_"))
    return colonnes_nettoyees

colonnes = colonnes_emotions + colonnes_excessivite
nv_noms = simplifier_colonnes(colonnes)
df.rename(columns=dict(zip(colonnes, nv_noms)), inplace=True)

# 3. Conversion binaire sur les colonnes renommées d’émotions
def convertir_binaire(df, colonnes=None):
    if colonnes is None:
        colonnes = df.select_dtypes(include='object').columns
    for col in colonnes:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace(r"[\r\n\t\u00A0]", "", regex=True)  # Nettoyage
                .str.strip()
                .str.lower()
                .map({'oui': 1, 'non': 0})
            )
    return df

# Appliquer conversion binaire sur les colonnes renommées d’émotions
emotion_columns = [col for col in df.columns if col.startswith("émotion_")]
df = convertir_binaire(df, emotion_columns)

df.to_excel(f"{video}.xlsx", index=False)
print("✅ Pré-traitement terminé !")

#############################################################################################
# 4. Extraction des sous-dataframes
excess_columns = [col for col in df.columns if col.startswith("excessif_")]
df_excess = df[excess_columns].apply(pd.to_numeric, errors='coerce')

df_emotions = df[emotion_columns].apply(pd.to_numeric, errors='coerce')

#############################################################################################
# Fonctions de visualisation
def graphe_moyennes(df_subset, label):
    mean_scores = df_subset.mean().sort_values(ascending=False)
    plt.figure(figsize=(20, 12))
    sns.barplot(x=mean_scores.values, y=mean_scores.index, palette="Reds_r")
    plt.xlabel("Note moyenne")
    plt.title(f"{label.capitalize()} perçus")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{label}_graph_moyenne_{video}.png"))
    plt.close()

def comparaison_par_profil(df, df_subset, profil, label):
    if profil in df.columns:
        merged_df = df[[profil]].join(df_subset)
        group_means = merged_df.groupby(profil).mean().T
        if group_means.shape[1] == 0:
            print(f"❌ Aucun groupe valide pour {profil}")
            return
        group_means.plot(kind="barh", figsize=(12, 8), colormap="coolwarm")
        plt.title(f"Comparaison des {label}s par {profil.lower()}")
        plt.xlabel("Note moyenne")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{label}_comparaison_{profil.replace(' ', '_').lower()}_{video}.png"))
        plt.close()

def heatmap_correlation(df_subset, label):
    corr = df_subset.corr()
    plt.figure(figsize=(20, 16))
    sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f")
    plt.title(f"Corrélation entre les réponses ({label})")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{label}_correlation_heatmap_{video}.png"))
    plt.close()

#############################################################################################
# 5. Génération des graphiques
if __name__ == "__main__":
    graphe_moyennes(df_excess, label="excessif")
    comparaison_par_profil(df, df_excess, "Votre genre?", "excessif")
    comparaison_par_profil(df, df_excess, "Votre âge?", "excessif")
    comparaison_par_profil(df, df_excess, "Votre niveau d'études?", "excessif")
    heatmap_correlation(df_excess, "excessif")

    graphe_moyennes(df_emotions, label="emotion")
    comparaison_par_profil(df, df_emotions, "Votre genre?", "emotion")
    comparaison_par_profil(df, df_emotions, "Votre âge?", "emotion")
    comparaison_par_profil(df, df_emotions, "Votre niveau d'études?", "emotion")
    heatmap_correlation(df_emotions, "emotion")

    print(f"✅ Tous les graphes ont été sauvegardé dans le dossier {output_dir}/")

