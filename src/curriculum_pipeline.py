"""Curriculum processing pipeline: Categorizes, filters, rates quality, and exports roadmap."""

import os
import json
import sqlite3
from typing import List, Dict, Any, Optional

from . import db
from . import categorizer

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'cf_problems.db')
ROADMAP_MD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'CURRICULUM_ROADMAP.md')
CURRICULUM_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'curriculum_quality_problems.json')


def init_categorized_table(db_path: str = DB_PATH):
    """Create categorized_problems table and indexes."""
    conn = db.get_db_connection(db_path)
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS categorized_problems (
        problem_id TEXT PRIMARY KEY,
        main_topic TEXT NOT NULL,
        subtopic TEXT NOT NULL,
        subsubtopic_id INTEGER NOT NULL,
        subsubtopic TEXT NOT NULL,
        importance TEXT NOT NULL,
        quality_score INTEGER NOT NULL,
        is_selected INTEGER NOT NULL,
        approach_summary TEXT,
        filter_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(problem_id) REFERENCES problems(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_cat_main_topic ON categorized_problems(main_topic);
    CREATE INDEX IF NOT EXISTS idx_cat_subtopic ON categorized_problems(subtopic);
    CREATE INDEX IF NOT EXISTS idx_cat_subsub_id ON categorized_problems(subsubtopic_id);
    CREATE INDEX IF NOT EXISTS idx_cat_importance ON categorized_problems(importance);
    CREATE INDEX IF NOT EXISTS idx_cat_selected ON categorized_problems(is_selected);
    """)
    conn.commit()
    conn.close()


def run_curriculum_categorization(batch_size: int = 500, limit: Optional[int] = None, force: bool = False) -> Dict[str, Any]:
    """
    Categorizes all problems in the database:
    1. Evaluates educational quality (filters out uninformative/boilerplate problems).
    2. Maps to Main Topic, Subtopic, Subsubtopic (1..576).
    3. Solves & explains core algorithmic trick.
    4. Assigns importance (*, **, ***).
    5. Updates individual problem JSON files and SQLite.
    """
    init_categorized_table()

    conn = db.get_db_connection()
    cur = conn.cursor()

    if force:
        print("[*] Force flag enabled: resetting existing categorized_problems table...")
        cur.execute("DELETE FROM categorized_problems")
        conn.commit()

    query = """
    SELECT p.* FROM problems p
    LEFT JOIN categorized_problems c ON p.id = c.problem_id
    WHERE c.problem_id IS NULL
    ORDER BY CASE WHEN p.source = 'problemset' THEN 0 ELSE 1 END, p.rating DESC
    """
    if limit:
        query += f" LIMIT {limit}"

    cur.execute(query)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()

    total_to_process = len(rows)
    print(f"[*] Processing {total_to_process} problems for curriculum categorization and quality selection...")

    categorized_rows = []
    selected_count = 0
    star_counts = {'*': 0, '**': 0, '***': 0}

    for i, p in enumerate(rows, 1):
        # Parse JSON tags if string
        if isinstance(p.get('tags'), str):
            try:
                p['tags'] = json.loads(p['tags'])
            except Exception:
                p['tags'] = []

        # 1. Quality Filter
        is_selected, q_score, reason = categorizer.evaluate_quality(p)
        if is_selected:
            selected_count += 1

        # 2. Topic Matching & Approach Derivation
        topic_info = categorizer.match_topics(p)
        importance = topic_info['importance']
        star_counts[importance] = star_counts.get(importance, 0) + 1

        categorized_rows.append((
            p['id'],
            topic_info['main_topic'],
            topic_info['subtopic'],
            topic_info['subsubtopic_id'],
            topic_info['subsubtopic'],
            importance,
            q_score,
            1 if is_selected else 0,
            topic_info['approach_summary'],
            reason
        ))

        # Update problem dictionary and individual JSON file
        p['main_topic'] = topic_info['main_topic']
        p['subtopic'] = topic_info['subtopic']
        p['subsubtopic'] = topic_info['subsubtopic']
        p['importance'] = importance
        p['is_selected_quality'] = is_selected
        p['approach_summary'] = topic_info['approach_summary']
        db.save_individual_problem_file(p)

        if len(categorized_rows) >= batch_size or i == total_to_process:
            conn = db.get_db_connection()
            conn.executemany("""
            INSERT OR REPLACE INTO categorized_problems (
                problem_id, main_topic, subtopic, subsubtopic_id, subsubtopic,
                importance, quality_score, is_selected, approach_summary, filter_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, categorized_rows)
            conn.commit()
            conn.close()
            categorized_rows.clear()
            print(f"[{i}/{total_to_process}] Categorized {p['id']} -> {topic_info['main_topic']} > {topic_info['subtopic']} [{importance}]")

    print("[*] Generating master curriculum exports and roadmap...")
    export_curriculum_data()
    generate_roadmap_markdown()

    return {
        'total_processed': total_to_process,
        'selected_quality_count': selected_count,
        'star_breakdown': star_counts
    }


def export_curriculum_data(output_path: str = CURRICULUM_JSON_PATH):
    """Export only high-quality selected problems structured by Main Topic and Subtopic."""
    conn = db.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        p.id, p.name, p.rating, p.solved_count, p.problem_url, p.editorial_url,
        p.time_limit, p.memory_limit, p.description, p.input_specification, p.output_specification,
        p.sample_testcases, p.tags,
        c.main_topic, c.subtopic, c.subsubtopic_id, c.subsubtopic, c.importance,
        c.quality_score, c.approach_summary
    FROM problems p
    JOIN categorized_problems c ON p.id = c.problem_id
    WHERE c.is_selected = 1
    ORDER BY c.subsubtopic_id ASC, CASE c.importance WHEN '***' THEN 1 WHEN '**' THEN 2 ELSE 3 END, p.solved_count DESC
    """)

    results = []
    for r in cur.fetchall():
        d = dict(r)
        if isinstance(d.get('tags'), str):
            try:
                d['tags'] = json.loads(d['tags'])
            except Exception:
                d['tags'] = []
        if isinstance(d.get('sample_testcases'), str):
            try:
                d['sample_testcases'] = json.loads(d['sample_testcases'])
            except Exception:
                d['sample_testcases'] = []
        results.append(d)

    conn.close()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"[+] Exported {len(results)} high-quality curriculum problems to {output_path}")
    return len(results)


def generate_roadmap_markdown(output_path: str = ROADMAP_MD_PATH):
    """Generate a clean, structured Markdown roadmap of all quality problems grouped by taxonomy."""
    conn = db.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        c.main_topic, c.subtopic, c.subsubtopic, c.subsubtopic_id,
        p.id, p.name, p.rating, p.solved_count, p.problem_url, p.editorial_url,
        c.importance, c.approach_summary
    FROM categorized_problems c
    JOIN problems p ON c.problem_id = p.id
    WHERE c.is_selected = 1
    ORDER BY c.subsubtopic_id ASC, 
             CASE c.importance WHEN '***' THEN 1 WHEN '**' THEN 2 ELSE 3 END, 
             p.rating ASC, p.solved_count DESC
    """)
    rows = cur.fetchall()
    conn.close()

    grouped: Dict[str, Dict[str, Dict[str, List[Dict[str, Any]]]]] = {}

    for r in rows:
        mt = r['main_topic']
        st = r['subtopic']
        sst = r['subsubtopic']
        grouped.setdefault(mt, {}).setdefault(st, {}).setdefault(sst, []).append(dict(r))

    lines = [
        "# Codeforces Quality Algorithmic Curriculum & Roadmap",
        "",
        "> Curated learning path with high-pedagogical problems, key tricks, and importance ratings.",
        "> - `***`: Masterpiece / Must-Solve problem teaching an essential paradigm",
        "> - `**`: Core classical problem for standard technique mastery",
        "> - `*`: Solid practice problem reinforcing the trick",
        "",
        "---",
        ""
    ]

    for main_topic, subtopics in grouped.items():
        lines.append(f"## {main_topic}\n")
        for subtopic, subsubs in subtopics.items():
            lines.append(f"### {subtopic}\n")
            for subsub, probs in subsubs.items():
                lines.append(f"#### {subsub}\n")
                lines.append("| Star | ID | Problem Name | Rating | Solves | Solution Trick / Approach | Editorial |")
                lines.append("|:---:|:---|:---|:---:|:---:|:---|:---:|")

                # Show top 5 curated problems per subsubtopic for maximum pedagogical impact
                for p in probs[:5]:
                    pid = p['id']
                    name = p['name']
                    url = p['problem_url']
                    rating = p['rating'] or "Unrated"
                    solves = p['solved_count']
                    star = p['importance']
                    approach = (p['approach_summary'] or '')[:100] + "..."
                    edit_link = f"[Editorial]({p['editorial_url']})" if p.get('editorial_url') else "—"
                    prob_link = f"[{pid} - {name}]({url})"
                    lines.append(f"| `{star}` | `{pid}` | {prob_link} | {rating} | {solves} | {approach} | {edit_link} |")
                lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"[+] Curriculum Roadmap Markdown generated at {output_path}")
