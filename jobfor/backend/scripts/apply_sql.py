import psycopg2
from app.core.config import settings

print(f"Connecting to {settings.DATABASE_URL}")
conn = psycopg2.connect(settings.DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

with open('migrate.sql', 'r', encoding='utf-16') as f:
    sql = f.read()

try:
    print("Executing SQL migrations directly...")
    cur.execute(sql)
    print("Success!")
except Exception as e:
    print(f"Error during migration execution: {e}")

cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [row[0] for row in cur.fetchall()]
print(f"Tables in DB: {tables}")
conn.close()
