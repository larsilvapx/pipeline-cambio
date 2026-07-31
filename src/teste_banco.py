import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="pipeline_dados",
    user="postgres",
    password="root"
)

print("Conectado!")
conn.close()