import sqlite3

conn = sqlite3.connect('data/cf_problems.db')
cur = conn.cursor()
cur.execute("SELECT id, problem_url, description FROM problems WHERE statement_status = 'error'")
rows = cur.fetchall()
print("Error rows count:", len(rows))
for r in rows:
    print(r)
