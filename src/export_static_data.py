"""Export Static Data for GitHub Pages Hosting.

Generates:
1. data/stats.json - Curriculum stats and topic counts
2. data/taxonomy.json - 576-technique curriculum tree with problem and masterpiece counts
3. data/problems_catalog.json - Complete lightweight problem catalog for instant client-side search, filtering, and sorting
"""

import os
import sys
import json
import sqlite3
import gzip

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import db
from src.taxonomy import TAXONOMY


def main():
    print("[*] Generating static data assets for GitHub Pages...")
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
    os.makedirs(data_dir, exist_ok=True)

    conn = db.get_db_connection()
    cur = conn.cursor()

    # 1. Stats Export
    cur.execute("SELECT count(*) FROM problems")
    total_problems = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM problems WHERE source = 'problemset'")
    ps_count = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM problems WHERE source = 'gym'")
    gym_count = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM categorized_problems WHERE is_selected = 1")
    quality_count = cur.fetchone()[0]

    cur.execute("""
    SELECT importance, count(*) 
    FROM categorized_problems 
    WHERE is_selected = 1 
    GROUP BY importance
    """)
    stars_map = {'***': 0, '**': 0, '*': 0}
    for row in cur.fetchall():
        stars_map[row[0]] = row[1]

    cur.execute("""
    SELECT main_topic, count(*) 
    FROM categorized_problems 
    WHERE is_selected = 1 
    GROUP BY main_topic
    ORDER BY count(*) DESC
    """)
    topics = [{'topic': r[0], 'count': r[1]} for r in cur.fetchall()]

    stats_data = {
        'total_problems': total_problems,
        'problemset_rated_count': ps_count,
        'gym_problems_count': gym_count,
        'curriculum_quality_count': quality_count,
        'stars': stars_map,
        'topic_breakdown': topics,
        'user_solved_count': 0,
        'user_bookmarked_count': 0
    }

    stats_path = os.path.join(data_dir, 'stats.json')
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats_data, f, indent=2)
    print(f"[+] Written {stats_path}")

    # 2. Taxonomy Export
    cur.execute("""
    SELECT 
        subsubtopic_id, 
        count(*) as total_count,
        sum(CASE WHEN importance = '***' THEN 1 ELSE 0 END) as masterpiece_count,
        sum(CASE WHEN importance = '**' THEN 1 ELSE 0 END) as core_count
    FROM categorized_problems
    WHERE is_selected = 1
    GROUP BY subsubtopic_id
    """)
    stats_map_counts = {r['subsubtopic_id']: dict(r) for r in cur.fetchall()}

    enriched_taxonomy = []
    for main_topic, subtopics in TAXONOMY.items():
        main_topic_item = {
            'name': main_topic,
            'total_problems': 0,
            'total_masterpieces': 0,
            'subtopics': []
        }
        for subtopic, items in subtopics.items():
            subtopic_item = {
                'name': subtopic,
                'total_problems': 0,
                'total_masterpieces': 0,
                'subsubtopics': []
            }
            for it in items:
                sid = it[0]
                sname = it[1]
                st_info = stats_map_counts.get(sid, {'total_count': 0, 'masterpiece_count': 0, 'core_count': 0})
                cnt = st_info['total_count']
                mp_cnt = st_info['masterpiece_count'] or 0

                subtopic_item['total_problems'] += cnt
                subtopic_item['total_masterpieces'] += mp_cnt
                main_topic_item['total_problems'] += cnt
                main_topic_item['total_masterpieces'] += mp_cnt

                subtopic_item['subsubtopics'].append({
                    'id': sid,
                    'name': sname,
                    'full_title': f"{sid}. {sname}",
                    'problem_count': cnt,
                    'masterpiece_count': mp_cnt,
                    'core_count': st_info.get('core_count', 0) or 0
                })

            main_topic_item['subtopics'].append(subtopic_item)

        enriched_taxonomy.append(main_topic_item)

    taxonomy_path = os.path.join(data_dir, 'taxonomy.json')
    with open(taxonomy_path, 'w', encoding='utf-8') as f:
        json.dump(enriched_taxonomy, f, indent=2)
    print(f"[+] Written {taxonomy_path}")

    # 3. Problems Catalog Export
    cur.execute("""
    SELECT 
        p.id, p.name, p.rating, p.solved_count, p.problem_url, p.editorial_url,
        p.tags, p.time_limit, p.memory_limit,
        c.main_topic, c.subtopic, c.subsubtopic_id, c.subsubtopic,
        c.importance, c.quality_score, c.approach_summary
    FROM categorized_problems c
    JOIN problems p ON c.problem_id = p.id
    WHERE c.is_selected = 1
    ORDER BY p.rating ASC, p.solved_count DESC
    """)
    rows = cur.fetchall()
    conn.close()

    catalog = []
    for r in rows:
        tags = []
        if r[6]:
            try:
                tags = json.loads(r[6]) if isinstance(r[6], str) else r[6]
            except Exception:
                tags = []
        catalog.append({
            'id': r[0],
            'name': r[1],
            'rating': r[2],
            'solved_count': r[3],
            'problem_url': r[4],
            'editorial_url': r[5],
            'tags': tags,
            'time_limit': r[7],
            'memory_limit': r[8],
            'main_topic': r[9],
            'subtopic': r[10],
            'subsubtopic_id': r[11],
            'subsubtopic': r[12],
            'importance': r[13],
            'quality_score': r[14],
            'approach_summary': r[15]
        })

    catalog_path = os.path.join(data_dir, 'problems_catalog.json')
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, separators=(',', ':'))
    
    file_size_mb = os.path.getsize(catalog_path) / (1024 * 1024)
    print(f"[+] Written {catalog_path} with {len(catalog)} problems ({file_size_mb:.2f} MB)")
    print("[+] All static data exports complete successfully!")


if __name__ == '__main__':
    main()
