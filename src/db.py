"""Database interface for Codeforces problem storage and management."""

import sqlite3
import json
import os
from typing import Dict, Any, List, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cf_problems.db')


def get_db_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH):
    """Initialize database tables and indexes."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS problems (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,              -- 'problemset' or 'gym'
        contest_id INTEGER NOT NULL,
        problem_index TEXT NOT NULL,
        name TEXT NOT NULL,
        rating INTEGER,                    -- e.g. 1400..3000 (NULL for unrated gym)
        tags TEXT,                         -- JSON array string
        solved_count INTEGER DEFAULT 0,
        problem_url TEXT NOT NULL,
        editorial_url TEXT,
        time_limit TEXT,
        memory_limit TEXT,
        description TEXT,
        input_specification TEXT,
        output_specification TEXT,
        sample_testcases TEXT,             -- JSON array string of {"input": "...", "output": "..."}
        statement_status TEXT DEFAULT 'pending', -- 'completed', 'pending', 'error', 'pdf_attachment'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS contests (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        phase TEXT,
        is_gym INTEGER DEFAULT 0,
        difficulty INTEGER
    );

    CREATE TABLE IF NOT EXISTS problem_tags (
        problem_id TEXT,
        tag TEXT,
        PRIMARY KEY(problem_id, tag),
        FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS user_progress (
        problem_id TEXT PRIMARY KEY,
        is_solved INTEGER DEFAULT 0,
        is_bookmarked INTEGER DEFAULT 0,
        notes TEXT DEFAULT '',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_problems_rating ON problems(rating);
    CREATE INDEX IF NOT EXISTS idx_problems_source ON problems(source);
    CREATE INDEX IF NOT EXISTS idx_problems_status ON problems(statement_status);
    CREATE INDEX IF NOT EXISTS idx_problem_tags_tag ON problem_tags(tag);
    CREATE INDEX IF NOT EXISTS idx_user_progress_solved ON user_progress(is_solved);
    CREATE INDEX IF NOT EXISTS idx_user_progress_bookmarked ON user_progress(is_bookmarked);
    """)

    conn.commit()
    conn.close()


def bulk_upsert_problems(problems: List[Dict[str, Any]], db_path: str = DB_PATH):
    """Insert or update a batch of problem metadata."""
    if not problems:
        return

    conn = get_db_connection(db_path)
    cur = conn.cursor()

    problem_rows = []
    tag_rows = []

    for p in problems:
        tags_json = json.dumps(p.get('tags', []))
        samples_json = json.dumps(p.get('sample_testcases', [])) if isinstance(p.get('sample_testcases'), list) else (p.get('sample_testcases') or '[]')

        problem_rows.append((
            p['id'],
            p['source'],
            p['contest_id'],
            p['problem_index'],
            p['name'],
            p.get('rating'),
            tags_json,
            p.get('solved_count', 0),
            p['problem_url'],
            p.get('editorial_url'),
            p.get('time_limit'),
            p.get('memory_limit'),
            p.get('description'),
            p.get('input_specification'),
            p.get('output_specification'),
            samples_json,
            p.get('statement_status', 'pending')
        ))

        for t in p.get('tags', []):
            tag_rows.append((p['id'], t))

    cur.executemany("""
    INSERT INTO problems (
        id, source, contest_id, problem_index, name, rating, tags,
        solved_count, problem_url, editorial_url, time_limit, memory_limit,
        description, input_specification, output_specification,
        sample_testcases, statement_status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        rating = COALESCE(excluded.rating, problems.rating),
        tags = excluded.tags,
        solved_count = excluded.solved_count,
        problem_url = excluded.problem_url,
        updated_at = CURRENT_TIMESTAMP
    """, problem_rows)

    if tag_rows:
        cur.executemany("""
        INSERT OR IGNORE INTO problem_tags (problem_id, tag) VALUES (?, ?)
        """, tag_rows)

    conn.commit()
    conn.close()


def update_problem_statement(problem_id: str, data: Dict[str, Any], db_path: str = DB_PATH):
    """Update statement fields after scraping."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    samples_json = json.dumps(data.get('sample_testcases', [])) if isinstance(data.get('sample_testcases'), list) else '[]'

    cur.execute("""
    UPDATE problems SET
        description = ?,
        input_specification = ?,
        output_specification = ?,
        sample_testcases = ?,
        editorial_url = COALESCE(?, editorial_url),
        time_limit = COALESCE(?, time_limit),
        memory_limit = COALESCE(?, memory_limit),
        statement_status = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, (
        data.get('description'),
        data.get('input_specification'),
        data.get('output_specification'),
        samples_json,
        data.get('editorial_url'),
        data.get('time_limit'),
        data.get('memory_limit'),
        data.get('statement_status', 'completed'),
        problem_id
    ))

    conn.commit()
    conn.close()


def bulk_update_problem_statements(updates: List[Dict[str, Any]], db_path: str = DB_PATH):
    """Bulk update multiple problem statements."""
    if not updates:
        return
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    rows = []
    for u in updates:
        samples_json = json.dumps(u.get('sample_testcases', [])) if isinstance(u.get('sample_testcases'), list) else '[]'
        rows.append((
            u.get('description'),
            u.get('input_specification'),
            u.get('output_specification'),
            samples_json,
            u.get('editorial_url'),
            u.get('time_limit'),
            u.get('memory_limit'),
            u.get('statement_status', 'completed'),
            u['id']
        ))

    cur.executemany("""
    UPDATE problems SET
        description = ?,
        input_specification = ?,
        output_specification = ?,
        sample_testcases = ?,
        editorial_url = COALESCE(?, editorial_url),
        time_limit = COALESCE(?, time_limit),
        memory_limit = COALESCE(?, memory_limit),
        statement_status = ?,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = ?
    """, rows)

    conn.commit()
    conn.close()


def get_pending_statement_problems(source: Optional[str] = None, limit: Optional[int] = None, db_path: str = DB_PATH) -> List[Dict[str, Any]]:
    """Retrieve problems that still need statement scraping (including retrying errors)."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    query = "SELECT * FROM problems WHERE statement_status IN ('pending', 'error')"
    params = []
    if source:
        query += " AND source = ?"
        params.append(source)
    query += " ORDER BY contest_id DESC, problem_index ASC"
    if limit:
        query += " LIMIT ?"
        params.append(limit)

    cur.execute(query, params)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def get_db_stats(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Return database statistics."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    stats = {}
    cur.execute("SELECT COUNT(*) FROM problems")
    stats['total_problems'] = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM problems WHERE source = 'problemset'")
    stats['problemset_total'] = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM problems WHERE source = 'problemset' AND rating BETWEEN 1400 AND 3000")
    stats['problemset_1400_3000'] = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM problems WHERE source = 'gym'")
    stats['gym_total'] = cur.fetchone()[0]

    cur.execute("SELECT statement_status, COUNT(*) FROM problems GROUP BY statement_status")
    stats['status_breakdown'] = {row[0]: row[1] for row in cur.fetchall()}

    cur.execute("SELECT COUNT(DISTINCT tag) FROM problem_tags")
    stats['unique_tags_count'] = cur.fetchone()[0]

    conn.close()
    return stats


def export_problems_to_json(output_path: str, source: Optional[str] = None, min_rating: Optional[int] = None, max_rating: Optional[int] = None, db_path: str = DB_PATH) -> int:
    """Export problems to JSON format."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()

    query = "SELECT * FROM problems WHERE 1=1"
    params = []

    if source:
        query += " AND source = ?"
        params.append(source)
    if min_rating is not None:
        query += " AND rating >= ?"
        params.append(min_rating)
    if max_rating is not None:
        query += " AND rating <= ?"
        params.append(max_rating)

    query += " ORDER BY rating ASC, contest_id DESC"

    cur.execute(query, params)
    rows = cur.fetchall()

    results = []
    for r in rows:
        d = dict(r)
        # Parse JSON fields
        try:
            d['tags'] = json.loads(d['tags']) if d['tags'] else []
        except Exception:
            d['tags'] = []
        try:
            d['sample_testcases'] = json.loads(d['sample_testcases']) if d['sample_testcases'] else []
        except Exception:
            d['sample_testcases'] = []
        results.append(d)

    conn.close()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    return len(results)


def save_individual_problem_file(problem_dict: Dict[str, Any], output_dir: Optional[str] = None):
    """Save a single problem as an individual JSON file."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'problems')
    os.makedirs(output_dir, exist_ok=True)

    prob_id = problem_dict['id']
    file_path = os.path.join(output_dir, f"{prob_id}.json")

    # Clean JSON fields if needed
    cleaned = dict(problem_dict)
    if isinstance(cleaned.get('tags'), str):
        try:
            cleaned['tags'] = json.loads(cleaned['tags'])
        except Exception:
            cleaned['tags'] = []
    if isinstance(cleaned.get('sample_testcases'), str):
        try:
            cleaned['sample_testcases'] = json.loads(cleaned['sample_testcases'])
        except Exception:
            cleaned['sample_testcases'] = []

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)


def export_all_individual_problems(output_dir: Optional[str] = None, source: Optional[str] = None, db_path: str = DB_PATH) -> int:
    """Export every problem in the database as an individual JSON file in data/problems."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'problems')
    os.makedirs(output_dir, exist_ok=True)

    conn = get_db_connection(db_path)
    cur = conn.cursor()

    query = "SELECT * FROM problems WHERE 1=1"
    params = []
    if source:
        query += " AND source = ?"
        params.append(source)
    query += " ORDER BY contest_id DESC, problem_index ASC"

    cur.execute(query, params)
    rows = cur.fetchall()

    for r in rows:
        d = dict(r)
        save_individual_problem_file(d, output_dir=output_dir)

    conn.close()
    return len(rows)


def get_user_progress(db_path: str = DB_PATH) -> Dict[str, Any]:
    """Retrieve all user solved, bookmarked problems and personal notes."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT problem_id, is_solved, is_bookmarked, notes FROM user_progress")
    rows = cur.fetchall()
    conn.close()

    solved = set()
    bookmarked = set()
    notes = {}

    for r in rows:
        pid = r['problem_id']
        if r['is_solved']:
            solved.add(pid)
        if r['is_bookmarked']:
            bookmarked.add(pid)
        if r['notes']:
            notes[pid] = r['notes']

    return {
        'solved': list(solved),
        'bookmarked': list(bookmarked),
        'notes': notes
    }


def toggle_problem_solved(problem_id: str, db_path: str = DB_PATH) -> bool:
    """Toggle solved state for a problem. Returns new state."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT is_solved FROM user_progress WHERE problem_id = ?", (problem_id,))
    row = cur.fetchone()
    new_state = 1
    if row:
        new_state = 0 if row['is_solved'] else 1
        cur.execute("UPDATE user_progress SET is_solved = ?, updated_at = CURRENT_TIMESTAMP WHERE problem_id = ?", (new_state, problem_id))
    else:
        cur.execute("INSERT INTO user_progress (problem_id, is_solved) VALUES (?, 1)", (problem_id,))
    conn.commit()
    conn.close()
    return bool(new_state)


def toggle_problem_bookmarked(problem_id: str, db_path: str = DB_PATH) -> bool:
    """Toggle bookmark state for a problem. Returns new state."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT is_bookmarked FROM user_progress WHERE problem_id = ?", (problem_id,))
    row = cur.fetchone()
    new_state = 1
    if row:
        new_state = 0 if row['is_bookmarked'] else 1
        cur.execute("UPDATE user_progress SET is_bookmarked = ?, updated_at = CURRENT_TIMESTAMP WHERE problem_id = ?", (new_state, problem_id))
    else:
        cur.execute("INSERT INTO user_progress (problem_id, is_bookmarked) VALUES (?, 1)", (problem_id,))
    conn.commit()
    conn.close()
    return bool(new_state)


def save_problem_note(problem_id: str, notes: str, db_path: str = DB_PATH) -> str:
    """Save user note for a problem."""
    conn = get_db_connection(db_path)
    cur = conn.cursor()
    cur.execute("SELECT problem_id FROM user_progress WHERE problem_id = ?", (problem_id,))
    if cur.fetchone():
        cur.execute("UPDATE user_progress SET notes = ?, updated_at = CURRENT_TIMESTAMP WHERE problem_id = ?", (notes, problem_id))
    else:
        cur.execute("INSERT INTO user_progress (problem_id, notes) VALUES (?, ?)", (problem_id, notes))
    conn.commit()
    conn.close()
    return notes


