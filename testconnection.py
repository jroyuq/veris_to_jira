import psycopg2

conn = psycopg2.connect(
    dbname="vcdb_full",
    user="postgres",
    password="chris",
    host="localhost",
    port="5432"
)

cursor = conn.cursor()
cursor.execute("SELECT incident_id, summary FROM vcdb_incidents LIMIT 1;")
print(cursor.fetchone())
