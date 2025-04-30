import pandas as pd
import psycopg2

# 1. Charger le CSV
df = pd.read_csv(r'C:\Users\MSIù\Downloads\vcdb_supabase_final_datetime_clean_with_asset.csv')

# 2. Nettoyer les noms de colonnes (remplacer les points par des underscores)
df.columns = [col.replace('.', '_') for col in df.columns]

# 3. Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname='vcdb_full',
    user='postgres',
    password='chris',
    host='localhost',
    port='5432'
)

# 4. Création du curseur
cur = conn.cursor()

# 5. Boucle d'insertion ligne par ligne
for index, row in df.iterrows():
    columns = ', '.join([f'"{col}"' for col in df.columns])
    values_placeholders = ', '.join(['%s'] * len(df.columns))
    sql = f"INSERT INTO vcdb_incidents ({columns}) VALUES ({values_placeholders})"
    cur.execute(sql, tuple(row))

# 6. Commit + fermeture
conn.commit()
cur.close()
conn.close()

print("✅ Données insérées avec succès !")
