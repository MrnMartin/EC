import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

# Nom de la vidéo à traiter
video = "video10"
print("Pour :", video)

# Créer le dossier de sortie s’il n’existe pas
output_dir = f"graphs_{video}"
os.makedirs(output_dir, exist_ok=True)

# Charger le fichier Excel
df = pd.read_excel(f"{video}.xlsx")

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

# 3. Conversion binaire uniquement sur les colonnes émotions
def convertir_binaire_emotions(df, colonnes_emotions):
    for col in colonnes_emotions:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.lower()
                .map({'oui': 1, 'non': 0})
            )
    return df

emotion_columns = [col for col in df.columns if col.startswith("émotion_")]
df = convertir_binaire_emotions(df, emotion_columns)

# Sauvegarder fichier nettoyé (optionnel)
df.to_excel(f"{video}_processed.xlsx", index=False)
print("✅ Renommage et conversion binaire terminés !")

#############################################################################################
# 4. Extraction des sous-dataframes
excess_columns = [col for col in df.columns if col.startswith("excessif_")]
df_excess = df[excess_columns].apply(pd.to_numeric, errors='coerce')

df_emotions = df[emotion_columns]  # déjà converti en binaire, donc numérique

#############################################################################################
# Fonctions de visualisation

def graphe_moyennes(df_subset, label):
    mean_scores = df_subset.mean().sort_values(ascending=False) * 100

    if label == "excessif":
        mean_scores = mean_scores / 2
        title = "Excessivité perçue"
        xlabel = "Note moyenne (0 à 2, affichée sur 100%)"
    else:
        title = f"{label.capitalize()} perçues"
        xlabel = "Note moyenne (0 à 1, affichée sur 100%)"

    plt.figure(figsize=(20, 12))
    sns.barplot(x=mean_scores.values, y=mean_scores.index, palette="Reds_r")
    plt.xlabel(xlabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{label}_graph_moyenne_{video}.png"))
    plt.close()


def comparaison_par_profil(df, df_subset, profil, label):
    if profil in df.columns:
        merged_df = df[[profil]].join(df_subset)
        group_means = merged_df.groupby(profil).mean().T * 100

        if group_means.shape[1] == 0:
            print(f"❌ Aucun groupe valide pour {profil}")
            return

        if label == "excessif":
            group_means = group_means / 2
            title = f"Comparaison de l'excessivité par {profil.lower()}"
        else:
            title = f"Comparaison des {label}s par {profil.lower()}"

        group_means.plot(kind="barh", figsize=(12, 8), colormap="coolwarm")
        plt.title(title)
        plt.xlabel("Note moyenne (en %)")
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{label}_comparaison_{profil.replace(' ', '_').lower()}_{video}.png"))
        plt.close()


def heatmap_correlation(df_subset, label):
    corr = df_subset.corr() * 100
    if label == "excessif":
        corr = corr / 2
        title = "Corrélation entre les réponses (excessivité)"
    else:
        title = f"Corrélation entre les réponses ({label})"

    plt.figure(figsize=(20, 16))
    sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f")
    plt.title(title)
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

    print(f"✅ Tous les graphiques ont été générés dans le dossier {output_dir}/")

    # Affichage des moyennes (valeurs relatives en % pour émotions)
    # Affichage des moyennes sous forme de tableau


    print("\nMoyennes des réponses (valeurs relatives) :\n")

    # Pour émotions
    moyennes_emotions = df_emotions.mean().sort_values(ascending=False)
    table_emotions = pd.DataFrame({
        "Composantes": moyennes_emotions.index,
        "Moyennes sur 2 ": moyennes_emotions,
        "Moyennes (%)": (moyennes_emotions.values * 100).round(2)
    })
    print("Émotions :")
    print(table_emotions.to_string(index=False))

    print("\n---======----\n")

    # Pour excessivité
    moyennes_excess = df_excess.mean().sort_values(ascending=False)
    table_excess = pd.DataFrame({
        "Composantes": moyennes_excess.index,
        "Moyenne sur 2": moyennes_excess,
        "Moyenne (%)": ((moyennes_excess.values/2)* 100).round(2)
    })
    print("Excessivité :")
    print(table_excess.to_string(index=False))

    # Sauvegarde des moyennes dans un fichier texte
    with open(f"{output_dir}/moyennes_reponses_{video}.txt", "w", encoding="utf-8") as f:
        f.write("=== Moyennes Excessivité ===\n")
        table_excess.to_csv(f, sep='\t', index=False)
        f.write("\n\n=== Moyennes Émotions ===\n")
        table_emotions.to_csv(f, sep='\t', index=False)

