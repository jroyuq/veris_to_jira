import pandas as pd
import psycopg2

# Connexion à PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="vcdb_full",
    user="postgres",
    password="chris"  # remplace par ton mot de passe PostgreSQL
)
cur = conn.cursor()

# Lire le fichier CSV
df = pd.read_csv("vcdb_supabase_final_datetime_clean_with_asset.csv")

# Remplace les NaN par None pour les valeurs SQL NULL
df = df.where(pd.notnull(df), None)

# Création de la nouvelle table
cur.execute("""
DROP TABLE IF EXISTS vcdb_incidents_assets;
CREATE TABLE vcdb_incidents_assets (
    incident_id TEXT PRIMARY KEY,
    summary TEXT,
    plus_created TEXT,
    plus_modified TEXT,
    impact_notes TEXT,
    victim_victim_id TEXT,
    victim_industry TEXT,
    plus_timeline_notification_year DOUBLE PRECISION,
    plus_timeline_notification_month DOUBLE PRECISION,
    timeline_discovery_value TEXT,
    action_malware BOOLEAN,
    action_hacking BOOLEAN,
    action_social BOOLEAN,
    action_physical BOOLEAN,
    action_misuse BOOLEAN,
    action_error BOOLEAN,
    action_environmental BOOLEAN,
    action_unknown BOOLEAN,
    actor_external BOOLEAN,
    actor_internal BOOLEAN,
    actor_partner BOOLEAN,
    actor_unknown BOOLEAN,
    attribute_confidentiality BOOLEAN,
    attribute_integrity BOOLEAN,
    attribute_availability BOOLEAN,
    asset_assets_variety TEXT,
    asset_assets_amount INTEGER,
    asset_assets_value TEXT,
    asset_cloud TEXT
);
""")

# Insertion des données
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO vcdb_incidents_assets (
            incident_id, summary, plus_created, plus_modified, impact_notes,
            victim_victim_id, victim_industry, plus_timeline_notification_year,
            plus_timeline_notification_month, timeline_discovery_value,
            action_malware, action_hacking, action_social, action_physical,
            action_misuse, action_error, action_environmental, action_unknown,
            actor_external, actor_internal, actor_partner, actor_unknown,
            attribute_confidentiality, attribute_integrity, attribute_availability,
            asset_assets_variety, asset_assets_amount, asset_assets_value, asset_cloud
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, tuple(row[col] for col in [
        'incident_id', 'summary', 'plus_created', 'plus_modified', 'impact_notes',
        'victim_victim_id', 'victim_industry', 'plus_timeline_notification_year',
        'plus_timeline_notification_month', 'timeline_discovery_value',
        'action_malware', 'action_hacking', 'action_social', 'action_physical',
        'action_misuse', 'action_error', 'action_environmental', 'action_unknown',
        'actor_external', 'actor_internal', 'actor_partner', 'actor_unknown',
        'attribute_confidentiality', 'attribute_integrity', 'attribute_availability',
        'asset_assets_variety', 'asset_assets_amount', 'asset_assets_value', 'asset_cloud'
    ]))

conn.commit()
cur.close()
conn.close()
print("✅ Données insérées avec succès dans vcdb_incidents_assets.")
