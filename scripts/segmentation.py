import csv
filename = "results-survey293392-4.4.csv"

def get_video_annotations(row, video_num, annotateurs=10, block_size=20):
    """
    Extrait les données des annotateurs et les annotations d'une vidéo donnée.
    """
    annotations_start = annotateurs + (video_num - 1) * block_size + 1
    annotations = row[annotations_start:annotations_start + block_size - 1]
    return row[:annotateurs] + annotations

# Lecture du fichier CSV
with open(filename, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = [[None if cell == "" else cell for cell in row] for row in reader]

# Sauvegarde des données pour chaque vidéo
for video_number in range(1, 11): #exclu n°11
    output_filename = f"videos/video{video_number}.txt"
    with open(output_filename, 'w', encoding='utf-8') as out_file:
        for row in data:
            combined = get_video_annotations(row, video_number)
            out_file.write(f"{combined}\n")  # Format Python list

print("Fichiers .txt avec listes Python générés pour chaque vidéo.")
