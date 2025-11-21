import csv
import pandas as pd
import os
import matplotlib.pyplot as plt
import folium
import os
from folium.plugins import MarkerCluster

# === 1. Lecture du fichier CSV ===
fichier_csv = "experimentations_5G.csv"

colonnes_cible = [
    "Expérimentateur",
    "Bande de fréquences",
    "Fréquences attribuées (limite haute)",
    "Fréquences attribuées (limite basse)",
    "Région",
    "Commune",
    "Latitude",
    "Longitude",
    "Début",
    "Fin"
]

donnees = []
with open(fichier_csv, mode="r", encoding="windows-1252") as fichier:
    lecteur = csv.DictReader(fichier, delimiter=';')
    for ligne in lecteur:
        entree = {col: ligne.get(col, "") for col in colonnes_cible}
        donnees.append(entree)

print(f"{len(donnees)} lignes lues depuis {fichier_csv}")

# === 2. Conversion ===
df = pd.DataFrame(donnees)

# Les coordonnées dans le CSV utilisent la virgule comme séparateur décimal (ex: 47,291944...)
# On remplace la virgule par un point avant la conversion en numérique.
df["Latitude"] = df["Latitude"].astype(str).str.replace(',', '.').str.strip()
df["Longitude"] = df["Longitude"].astype(str).str.replace(',', '.').str.strip()

df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")
df["Début"] = pd.to_datetime(df["Début"], errors="coerce")
df["Fin"] = pd.to_datetime(df["Fin"], errors="coerce")

df["Durée (jours)"] = (df["Fin"] - df["Début"]).dt.days
df["Année"] = df["Début"].dt.year

# === 3. GÉNÉRATION DES GRAPHIQUES ===
plt.figure(figsize=(10, 6))
df["Expérimentateur"].value_counts().plot(kind="bar", color="skyblue")
plt.title("Nombre d'expérimentations 5G par opérateur")
plt.tight_layout()
plt.savefig("graph_operateurs.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 6))
df["Région"].value_counts().plot(kind="barh", color="lightgreen")
plt.title("Expérimentations 5G par région")
plt.tight_layout()
plt.savefig("graph_regions.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
df["Année"].value_counts().sort_index().plot(kind="line", marker="o", color="coral")
plt.title("Nombre d'expérimentations 5G par année")
plt.grid(True, linestyle="--")
plt.tight_layout()
plt.savefig("graph_annees.png", dpi=150)
plt.close()

plt.figure(figsize=(8, 5))
df["Durée (jours)"].dropna().plot(kind="hist", bins=30, color="purple", alpha=0.7)
plt.title("Durée des expérimentations (jours)")
plt.grid(axis='y')
plt.tight_layout()
plt.savefig("graph_durees.png", dpi=150)
plt.close()

print("Graphiques exportés.")

# === 4. CARTE FOLIUM AMÉLIORÉE ===

# === 4. CARTE FOLIUM AMÉLIORÉE ===

# Vérifier qu'il existe au moins une coordonnée valide
valid_lat = df["Latitude"].dropna()
valid_lon = df["Longitude"].dropna()

if valid_lat.empty or valid_lon.empty:
    print("Avertissement : aucune coordonnée valide trouvée -> la carte ne sera pas générée.")
    # Écrire un fichier HTML minimal pour conserver la chaîne de traitement
    with open("map_5g.html", "w", encoding="utf-8") as f:
        f.write("<html><body><p>Aucune coordonnée valide pour générer la carte.</p></body></html>")
else:
    centre_lat = valid_lat.mean()
    centre_lon = valid_lon.mean()

    carte = folium.Map(location=[centre_lat, centre_lon], zoom_start=6, tiles="OpenStreetMap")

    cluster = MarkerCluster().add_to(carte)

    couleurs = {
        "Orange": "orange",
        "SFR": "red",
        "Bouygues": "blue",
        "Free": "green"
    }

    for _, row in df.iterrows():
        if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
            couleur = couleurs.get(row["Expérimentateur"], "gray")

            popup = folium.Popup(
                f"""
                <b>{row['Expérimentateur']}</b><br>
                Commune : {row['Commune']}<br>
                Région : {row['Région']}<br>
                Bande utilisée : {row['Bande de fréquences']}
                """,
                max_width=300
            )

            folium.Marker(
                location=[row["Latitude"], row["Longitude"]],
                popup=popup,
                icon=folium.Icon(color=couleur)
            ).add_to(cluster)

    carte.save("map_5g.html")

# === 5. INTÉGRATION DANS `new 1.html` ===

# Utiliser `new 1.html` comme template et faire une sauvegarde avant écriture
template_path = "new 1.html"
backup_path = template_path + ".bak"

if os.path.exists(template_path):
    # créer une sauvegarde si elle n'existe pas déjà
    if not os.path.exists(backup_path):
        with open(template_path, "r", encoding="utf-8") as f:
            original_html = f.read()
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(original_html)
        print(f"Sauvegarde créée : {backup_path}")
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()
else:
    # Si `new 1.html` n'existe pas, créer un template minimal
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head><meta charset='utf-8'><title>Rapport 5G</title></head>
    <body>
      <h1>Rapport 5G</h1>
      <div>[Zone d'affichage de la carte générée]</div>
      <div>[Tableau synthétique des expérimentations par région]</div>
      <div>[Liste ou graphique des principaux Expérimentateurs (SNCF, CEA, etc.)]</div>
      <div>[Graphique à barres ou circulaire montrant la fréquence d'utilisation de chaque technologie]</div>
      <div>[Graphique montrant quels usages sont les plus testés]</div>
    </body>
    </html>
    """
    print(f"Template minimal '{template_path}' utilisé (nouveau fichier sera créé).")

# insertion de la carte : on utilise un iframe pour embarquer `map_5g.html` de façon fiable
iframe = '<iframe src="map_5g.html" style="width:100%;height:600px;border:0;"></iframe>'
# Remplacer le placeholder attendu, ou remplacer un éventuel placeholder HTML déjà injecté précédemment
html = html.replace("[Zone d'affichage de la carte générée]", iframe)
html = html.replace('<html><body><p>Aucune coordonnée valide pour générer la carte.</p></body></html>', iframe)

# insertion des graphiques
html = html.replace("[Tableau synthétique des expérimentations par région]", '<img src="graph_regions.png" alt="graph_regions">')
html = html.replace("[Liste ou graphique des principaux Expérimentateurs (SNCF, CEA, etc.)]", '<img src="graph_operateurs.png" alt="graph_operateurs">')
html = html.replace("[Graphique à barres ou circulaire montrant la fréquence d'utilisation de chaque technologie]", '<img src="graph_annees.png" alt="graph_annees">')
html = html.replace("[Graphique montrant quels usages sont les plus testés]", '<img src="graph_durees.png" alt="graph_durees">')

# Écrire le résultat directement dans `new 1.html` (écrase le fichier après sauvegarde)
with open(template_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"Graphiques et carte intégrés dans : {template_path} (sauvegarde : {backup_path} si existant)")