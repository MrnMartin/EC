import pandas as pd

filename = "../Resultats_homogenises.xlsx"

def get_video_annotations(row, video_num, annotateurs=10, block_size=20):
    annotations_start = annotateurs + (video_num - 1) * block_size
    annotations = row[annotations_start:annotations_start + block_size]
    return row[:annotateurs] + annotations

# Lecture du fichier Excel
df = pd.read_excel(filename, header=None)
data = df.values.tolist()

# Sauvegarde des données pour chaque vidéo en format Excel
for video_number in range(1, 11):
    output_filename = f"../videos/video{video_number}.xlsx"

    # Traitement des données pour chaque vidéo
    processed_data = [get_video_annotations(row, video_number) for row in data]

    # Création d'un DataFrame avec les données traitées
    processed_df = pd.DataFrame(processed_data)

    # Sauvegarde du DataFrame sous forme de fichier Excel
    processed_df.to_excel(output_filename, index=False, header=False, engine='openpyxl')

    print(f"Fichier sauvegardé sous : {output_filename}")
