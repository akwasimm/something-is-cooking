import psycopg2
try:
    conn = psycopg2.connect('postgresql://jobfor:jobfor_secret@localhost:5432/jobsearch')
    cur = conn.cursor()
    cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    print('Localhost tables:', [r[0] for r in cur.fetchall()])
    conn.close()
except Exception as e:
    print('Localhost connect failed:', e)
