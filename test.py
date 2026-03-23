"""
Génère un CSV filtré des communes > 1500 habitants
en croisant ton fichier codes_villes.csv avec les données population de data.gouv.fr

Prérequis : pip install pandas requests
"""
import pandas as pd
import requests
import io

print("Téléchargement des données population (data.gouv.fr)...")
url = "https://www.data.gouv.fr/api/1/datasets/r/f5df602b-3800-44d7-b2df-fa40a0350325"
response = requests.get(url, timeout=30)
response.raise_for_status()

pop_df = pd.read_csv(
    io.StringIO(response.text),
    usecols=["code_insee", "population"],
    dtype={"code_insee": str}
)
pop_df["code_insee"] = pop_df["code_insee"].str.zfill(5)
print(f"  -> {len(pop_df)} communes chargées depuis data.gouv.fr")

# Charger ton fichier
print("\nChargement de codes_villes.csv...")
codes_df = pd.read_csv(
    "codes_villes.csv",
    encoding="latin-1",
    sep=None,
    engine="python"
)
codes_df.columns = codes_df.columns.str.strip()
codes_df.rename(columns={"#Code_commune_INSEE": "Code_commune_INSEE"}, inplace=True)
codes_df["Code_commune_INSEE"] = codes_df["Code_commune_INSEE"].astype(str).str.zfill(5)
print(f"  -> {len(codes_df)} lignes chargées")

# Fusionner avec les populations
merged = codes_df.merge(
    pop_df,
    left_on="Code_commune_INSEE",
    right_on="code_insee",
    how="left"
)

# Filtrer les communes > 1500 habitants
seuil = 1500
filtered = merged[merged["population"] >= seuil].copy()
filtered = filtered.drop(columns=["code_insee", "population"])

print(f"\nCommunes >= {seuil} hab : {len(filtered)} lignes")
print(f"  (sur {codes_df['Code_commune_INSEE'].nunique()} communes uniques dans le fichier source)")

# Sauvegarder
output_file = "codes_villes_1500hab.csv"
filtered.to_csv(output_file, index=False, encoding="utf-8-sig")
print(f"\nFichier genere : {output_file}")
print(filtered.head())