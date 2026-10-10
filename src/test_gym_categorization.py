import sys
import sqlite3
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from src import categorizer

conn = sqlite3.connect('data/cf_problems.db')
cur = conn.cursor()
cur.execute('''
SELECT p.id, p.name, p.problem_index, c.name as contest_name, c.difficulty
FROM problems p
JOIN contests c ON p.contest_id = c.id
WHERE p.source = 'gym'
LIMIT 20
''')
rows = cur.fetchall()
conn.close()

for r in rows:
    pid, pname, pidx, cname, diff = r
    p = {
        'id': pid,
        'name': pname,
        'tags': [],
        'description': f"Problem {pname} from {cname}. Contest difficulty: {diff}. Problem index: {pidx}.",
        'rating': 1500 + (diff or 3) * 150
    }
    match = categorizer.match_topics(p)
    print(f"{pid} ({pname}) -> {match['main_topic']} > {match['subtopic']} > {match['subsubtopic']} [{match['importance']}]")
