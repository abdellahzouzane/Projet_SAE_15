import csv

# Nom du fichier CSV à ouvrir
fichier_csv = "experimentations_5G.csv"

# Colonnes à récupérer
colonnes_cible = [
    "Operateur",
    "Bande de fréquences",
    "Fréquences attribuées (limite haute)",
    "Fréquences attribuées (limite basse)",
    "Région",
    "Début",
    "Fin"
]

# Liste pour stocker les données extraites
donnees = []

# Lecture du fichier CSV
with open(fichier_csv, mode="r", encoding="windows-1252") as fichier:
    lecteur = csv.DictReader(fichier, delimiter=';')
    
    for ligne in lecteur:
        # On récupère uniquement les colonnes qui nous intéressent
        entree = {col: ligne[col] for col in colonnes_cible if col in ligne}
        donnees.append(entree)

# Affichage des données extraites
for d in donnees:
    print(d)




