import psycopg2
from app.core.config import settings

print(f"Connecting to {settings.DATABASE_URL}")
conn = psycopg2.connect(settings.DATABASE_URL)
conn.autocommit = True
cur = conn.cursor()

try:
    cur.execute("SELECT * FROM alembic_version")
    print("Alembic versions:", cur.fetchall())
except psycopg2.Error as e:
    print("Error selecting alembic_version:", e)

cur.execute("CREATE TABLE IF NOT EXISTS _test_table (id int)")
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [r[0] for r in cur.fetchall()]
print("All tables inside public schema:", tables)
conn.close()
