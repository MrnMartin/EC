"""Script principal pour lancer tous les scripts un par un.
(Il attend que le script précédent soit terminé pour lancer le prochain)"""
import subprocess

# Liste des scripts à lancer :
scripts = ['Genre.py', 'Nationalite.py', 'pays_naissance.py', 'segmentation.py']

for script in scripts:
    print(f"Exécution de {script}...")
    subprocess.run(['python', script])
