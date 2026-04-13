import os
import sys

sys.path.insert(0, os.path.abspath('e:/Antigravity Projects/jobfor/backend'))

from app.core.config import settings
import psycopg2

print(f"Connecting to {settings.DATABASE_URL[:60]}...")
conn = psycopg2.connect(settings.DATABASE_URL)
cur = conn.cursor()
cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
tables = [row[0] for row in cur.fetchall()]
print(f"Found {len(tables)} tables: {tables}")
conn.close()
