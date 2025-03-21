import csv

filename="sondage_énoncé_par_énoncé.csv"

with open(filename,'r', encoding='utf-8') as data :
    read = csv.reader(data)
    data = [[None if cell == "" else cell for cell in row] for row in read]  # Transformation

#Affichage :
for row in data:
    print(row)

#command : python3 xlxs-to-csv.py > corpus.txt
