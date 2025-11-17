import csv
import pandas as pd
import matplotlib.pyplot as plt

# === 1. Lecture du fichier CSV ===
fichier_csv = "experimentations_5G.csv"

colonnes_cible = [
    "Expérimentateur",
    "Bande de fréquences",
    "Fréquences attribuées (limite haute)",
    "Fréquences attribuées (limite basse)",
    "Région",
    "Début",
    "Fin"
]

# Lecture du fichier CSV dans une liste de dictionnaires
donnees = []
with open(fichier_csv, mode="r", encoding="windows-1252") as fichier:
    lecteur = csv.DictReader(fichier, delimiter=';')
    for ligne in lecteur:
        entree = {col: ligne.get(col, "") for col in colonnes_cible}
        donnees.append(entree)

print(f" {len(donnees)} lignes lues depuis {fichier_csv}")

# === 2. Conversion en DataFrame Pandas ===
df = pd.DataFrame(donnees)

# Vérification des colonnes présentes
print("\nColonnes disponibles :", list(df.columns))
print("\nAperçu des données :")
print(df.head())

# === 3. Nettoyage et transformation des dates ===
df["Début"] = pd.to_datetime(df["Début"], errors="coerce")
df["Fin"] = pd.to_datetime(df["Fin"], errors="coerce")

# Calcul de la durée (en jours)
df["Durée (jours)"] = (df["Fin"] - df["Début"]).dt.days

# Création d'une colonne 'Année' pour l'analyse temporelle
df["Année"] = df["Début"].dt.year

# === 4. Graphique 1 : Nombre d’expérimentations par opérateur ===
plt.figure(figsize=(10, 6))
df["Expérimentateur"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Nombre d'expérimentations 5G par opérateur")
plt.xlabel("Expérimentateur")
plt.ylabel("Nombre d'expérimentations")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# === 5. Graphique 2 : Répartition par région ===
plt.figure(figsize=(10, 6))
df["Région"].value_counts().plot(kind="barh", color="lightgreen")
plt.title("Expérimentations 5G par région")
plt.xlabel("Nombre d'expérimentations")
plt.ylabel("Région")
plt.tight_layout()
plt.show()

# === 6. Graphique 3 : Évolution dans le temps ===
plt.figure(figsize=(8, 5))
df["Année"].value_counts().sort_index().plot(kind="line", marker="o", color="coral")
plt.title("Nombre d'expérimentations 5G par année")
plt.xlabel("Année de début")
plt.ylabel("Nombre d'expérimentations")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

# === 7. Graphique 4 : Durée des expérimentations ===
plt.figure(figsize=(8, 5))
df["Durée (jours)"].dropna().plot(kind="hist", bins=30, color="purple", alpha=0.7)
plt.title("Durée des expérimentations 5G (en jours)")
plt.xlabel("Durée (jours)")
plt.ylabel("Nombre d'expérimentations")
plt.grid(axis='y', linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

