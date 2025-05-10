import pandas as pd
import re

file_path = 'Resultats_homogenises.xlsx'
df= pd.read_excel(file_path)
print (df.columns)

col_nationalite = 'Votre nationalité?'

européens = [
    "Français","Française","Italienne","Italien","Portugais","Portugaise","Espagnol","Espagnole","Belge","Allemand","Allemande","Suisse","Néerlandais","Néerlandaise","Suédois","Suédoise", "Danois","Danoise","Finlandais", "Finlandaise", "Irlandais","Irlandaise", "Norvégien",'Norvégienne',"Polonais", "Polonaise", "Grec", "Grecque", "Roumain","Roumaine","Tchèque", "Slovaque","Hongrois","Hongroise","Croate","Serbe","Letton","Lituanien","Estonien","Slovène","Chypriote","Maltais", "Autrichien", "Autrichienne"
    ]

def europ(nationalite):
    if pd.isna(nationalite):
        return "Non-européen"
    nationalite = nationalite.lower()
    for europe in européens:
        if europe.lower() in nationalite:
            return "Européen"
        return "Non-européen"

df[col_nationalite] = df[col_nationalite].apply(europ)

df.to_excel('Resultats_homogenises.xlsx', index=False)

print(df[[col_nationalite]].head())
