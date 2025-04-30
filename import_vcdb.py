import pandas as pd
import psycopg2

# 1. Charger le CSV
df = pd.read_csv(r'C:\Users\MSIù\Downloads\vcdb_supabase_final_datetime_clean_with_asset.csv', low_memory=False)

# 2. Connexion PostgreSQL
conn = psycopg2.connect(
    dbname='vcdb_full',
    user='postgres',
    password='chris',
    host='localhost',
    port='5432'
)

# 3. Récupérer les colonnes de la base existantes
cur = conn.cursor()
cur.execute("""
    SELECT column_name FROM information_schema.columns
    WHERE table_name = 'vcdb_incidents'
""")
existing_columns = [row[0] for row in cur.fetchall()]

# 4. Filtrer le DataFrame selon les colonnes de la base
filtered_columns = [col for col in df.columns if col in existing_columns]
df = df[filtered_columns]

# 5. Insertion
for index, row in df.iterrows():
    columns = ', '.join([f'"{col}"' for col in df.columns])
    placeholders = ', '.join(['%s'] * len(df.columns))
    sql = f'INSERT INTO vcdb_incidents ({columns}) VALUES ({placeholders})'
    try:
        cur.execute(sql, tuple(row))
    except Exception as e:
        print(f"❌ Erreur ligne {index + 1} : {e}")
        conn.rollback()
        continue

# 6. Terminer
conn.commit()
cur.close()
conn.close()

print("✅ Données insérées avec succès !")
