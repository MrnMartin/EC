import pandas as pd
import re

file_path = '../corpus/results-survey293392-4.4.xlsx'
df = pd.read_excel(file_path)
print (df.columns)

df['Votre genre?'] = df ['Votre genre?'].astype(str)

def homogenize_genre(gender):
    if isinstance(gender, str):
        gender_lower = gender.lower()
        if 'femme' in gender_lower or 'féminin' in gender_lower or 'sarah' in gender_lower or 'femele' in gender_lower or 'feminin' in gender_lower or 'fille'in gender_lower:
            return 'F'
        elif 'homme' in gender_lower or 'masculin' in gender_lower:
            return 'H'
        else:
            return ' '

    return gender

df['Votre genre?'] = df['Votre genre?'].apply(homogenize_genre)
df.to_excel('Genre_mod.xlsx', index=False)
print("Le fichier à été modifié")
