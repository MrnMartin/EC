import pandas as pd
import csv

filename = "Resultats_homogenises.xlsx"

def get_video_annotations(row, video_num, annotateurs=10, block_size=20):
    annotations_start = annotateurs + (video_num - 1) * block_size
    annotations = row[annotations_start:annotations_start + block_size]
    return row[:annotateurs] + annotations

# Lecture du fichier Excel
df = pd.read_excel(filename, header=None)
data = df.values.tolist()

# Sauvegarde des données pour chaque vidéo (CSV valide)
for video_number in range(1, 11):
    output_filename = f"../videos/video{video_number}.csv"
    with open(output_filename, 'w', encoding='utf-8', newline='') as out_file:
        writer = csv.writer(out_file)
        for row in data:
            combined = get_video_annotations(row, video_number)
            writer.writerow(combined)
