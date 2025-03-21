import pandas as pd

f = 'sondage_énoncé_par_énoncé.xlsx'
df = pd.read_excel(f)

print(df.columns)
df.columns= df.columns.str.strip()

if 'niveau d\'études' in df.columns:

    df ['niveau d\'études'] = df['niveau d\'études'].replace({
        r'\b(?:bac\s?\+3|Bac\s?\+3|Bac\s?\+3|bac \+3|Bac \+3|Bac \+ 3|BAC \+3|BAC \+ 3|bac \+ 3)\b': 'Bac+3',
        r'\b(?:bac\s?\+4|Bac\s?\+4|Bac\s?\+4|bac \+4|Bac \+4|Bac \+ 4)\b': 'Bac+4',
    }, regex=True)

    df.to_excel('Modifié.xlsx', index=False)
    print ("Les notations sont good")
