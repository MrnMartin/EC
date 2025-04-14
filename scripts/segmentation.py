import pandas as pd

filename = "Resultats_homogenises.xlsx"

def get_video_annotations(row, video_num, annotateurs=10, block_size=20):
    annotations_start = annotateurs + (video_num - 1) * block_size
    annotations = row[annotations_start:annotations_start + block_size]
    return row[:annotateurs] + annotations

# Lecture du fichier Excel
df = pd.read_excel(filename, header=None)
data = df.values.tolist()

# Sauvegarde des données pour chaque vidéo (avec format liste)
for video_number in range(1, 11):
    output_filename = f"../videos/video{video_number}.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for row in data:
            combined = get_video_annotations(row, video_number)
            out_file.write(f"{combined}\n")  # Format liste conservé
