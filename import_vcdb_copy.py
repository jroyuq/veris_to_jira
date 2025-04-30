import psycopg2
import pandas as pd
import os

# Charger le fichier CSV (chemin local)
csv_path = r'C:\Users\MSIù\Downloads\vcdb_supabase_final_datetime_clean_with_asset.csv'
df = pd.read_csv(csv_path)

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname='vcdb_full',
    user='postgres',
    password='chris',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Nom de la table PostgreSQL
table_name = 'vcdb_incidents'

# Vérifier que les colonnes correspondent (CSV vs table)
cur.execute(f"""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_name = '{table_name}'
    ORDER BY ordinal_position;
""")
pg_columns = [col[0] for col in cur.fetchall()]

# Vérification
if sorted(df.columns) != sorted(pg_columns):
    with open('log.txt', 'w', encoding='utf-8') as log:
        log.write("❌ Erreur : les colonnes du CSV ne correspondent pas aux colonnes attendues.\n")
        log.write(f"\nColonnes manquantes ou incorrectes :\n")
        for col in df.columns:
            if col not in pg_columns:
                log.write(f"- {col}\n")
    print("❌ Erreur : les colonnes du CSV ne correspondent pas aux attendues. Voir log.txt.")
    conn.close()
    exit()

# Sauvegarder un nouveau CSV temporaire au bon format (UTF-8 sans index ni header)
temp_csv_path = 'temp_vcdb.csv'
df.to_csv(temp_csv_path, index=False, header=False)

# COPY FROM pour insertion rapide
try:
    with open(temp_csv_path, 'r', encoding='utf-8') as f:
        cur.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV", f)
    conn.commit()
    print("✅ Données insérées avec succès via COPY !")

except Exception as e:
    with open("log.txt", "w", encoding="utf-8") as log_file:
        log_file.write("❌ Erreur COPY : " + str(e))
    print("⚠️ Échec lors du chargement avec COPY. Voir log.txt.")

finally:
    # Nettoyage
    if os.path.exists(temp_csv_path):
        os.remove(temp_csv_path)
    cur.close()
    conn.close()
