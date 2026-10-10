"""FastAPI backend server for Codeforces Categorizer Web Application."""

import os
import json
import sqlite3
import math
from typing import Optional, List, Dict, Any

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import db
from .taxonomy import TAXONOMY

app = FastAPI(title="Codeforces Categorizer API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
WEB_DIR = os.path.join(ROOT_DIR, 'web')

# Mount static directory
static_mount_dir = STATIC_DIR if os.path.exists(STATIC_DIR) else WEB_DIR
app.mount("/static", StaticFiles(directory=static_mount_dir), name="static")

# Mount data directory for static asset fallback
if os.path.exists(DATA_DIR):
    app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")


class NotePayload(BaseModel):
    notes: str


@app.get("/", response_class=HTMLResponse)
@app.get("/index.html", response_class=HTMLResponse)
async def serve_index():
    for candidate in [os.path.join(ROOT_DIR, 'index.html'), os.path.join(WEB_DIR, 'index.html')]:
        if os.path.exists(candidate):
            with open(candidate, 'r', encoding='utf-8') as f:
                return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>CF Categorizer: index.html not found</h1>", status_code=404)


@app.get("/api/taxonomy")
async def get_taxonomy():
    """
    Returns the complete 11-topic competitive programming taxonomy
    enriched with problem counts and masterpiece counts per subsubtopic.
    """
    conn = db.get_db_connection()
    cur = conn.cursor()

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
    stats_map = {r['subsubtopic_id']: dict(r) for r in cur.fetchall()}
    conn.close()

    result = []
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
                st_info = stats_map.get(sid, {'total_count': 0, 'masterpiece_count': 0, 'core_count': 0})
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

        result.append(main_topic_item)

    return result


@app.get("/api/stats")
async def get_stats():
    """Returns overarching database and curriculum statistics."""
    conn = db.get_db_connection()
    cur = conn.cursor()

    total_probs = cur.execute("SELECT count(*) FROM problems").fetchone()[0]
    ps_probs = cur.execute("SELECT count(*) FROM problems WHERE source = 'problemset'").fetchone()[0]
    gym_probs = cur.execute("SELECT count(*) FROM problems WHERE source = 'gym'").fetchone()[0]

    cur.execute("""
    SELECT 
        count(*) as quality_count,
        sum(CASE WHEN importance = '***' THEN 1 ELSE 0 END) as star_3,
        sum(CASE WHEN importance = '**' THEN 1 ELSE 0 END) as star_2,
        sum(CASE WHEN importance = '*' THEN 1 ELSE 0 END) as star_1
    FROM categorized_problems
    WHERE is_selected = 1
    """)
    cat_summary = dict(cur.fetchone())

    cur.execute("""
    SELECT 
        main_topic,
        count(*) as count,
        sum(CASE WHEN importance = '***' THEN 1 ELSE 0 END) as masterpieces
    FROM categorized_problems
    WHERE is_selected = 1
    GROUP BY main_topic
    ORDER BY count DESC
    """)
    topic_breakdown = [dict(r) for r in cur.fetchall()]

    progress = db.get_user_progress()
    conn.close()

    return {
        'total_problems': total_probs,
        'problemset_rated_count': ps_probs,
        'gym_problems_count': gym_probs,
        'curriculum_quality_count': cat_summary['quality_count'],
        'stars': {
            '***': cat_summary['star_3'] or 0,
            '**': cat_summary['star_2'] or 0,
            '*': cat_summary['star_1'] or 0
        },
        'topic_breakdown': topic_breakdown,
        'user_solved_count': len(progress['solved']),
        'user_bookmarked_count': len(progress['bookmarked'])
    }


@app.get("/api/problems")
async def list_problems(
    main_topic: Optional[str] = None,
    subtopic: Optional[str] = None,
    subsubtopic_id: Optional[int] = None,
    importance: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None,
    status: Optional[str] = None,
    q: Optional[str] = None,
    sort_by: str = 'rating_asc',
    page: int = 1,
    page_size: int = 40
):
    """
    Search and filter curriculum problems with pagination.
    """
    conn = db.get_db_connection()
    cur = conn.cursor()

    conditions = ["c.is_selected = 1"]
    params = []

    if main_topic and main_topic.strip() and main_topic != 'all':
        conditions.append("c.main_topic = ?")
        params.append(main_topic.strip())

    if subtopic and subtopic.strip() and subtopic != 'all':
        conditions.append("c.subtopic = ?")
        params.append(subtopic.strip())

    if subsubtopic_id is not None and subsubtopic_id > 0:
        conditions.append("c.subsubtopic_id = ?")
        params.append(subsubtopic_id)

    if importance and importance in ['***', '**', '*']:
        conditions.append("c.importance = ?")
        params.append(importance)

    if min_rating:
        conditions.append("p.rating >= ?")
        params.append(min_rating)

    if max_rating:
        conditions.append("p.rating <= ?")
        params.append(max_rating)

    if q and q.strip():
        term = f"%{q.strip().lower()}%"
        conditions.append("(LOWER(p.id) LIKE ? OR LOWER(p.name) LIKE ? OR LOWER(p.tags) LIKE ? OR LOWER(c.approach_summary) LIKE ?)")
        params.extend([term, term, term, term])

    if status == 'solved':
        conditions.append("u.is_solved = 1")
    elif status == 'unsolved':
        conditions.append("(u.is_solved IS NULL OR u.is_solved = 0)")
    elif status == 'bookmarked':
        conditions.append("u.is_bookmarked = 1")

    where_clause = " WHERE " + " AND ".join(conditions)

    # Count total matching
    count_sql = f"""
    SELECT count(*) 
    FROM categorized_problems c
    JOIN problems p ON c.problem_id = p.id
    LEFT JOIN user_progress u ON p.id = u.problem_id
    {where_clause}
    """
    cur.execute(count_sql, params)
    total_count = cur.fetchone()[0]

    # Order by logic
    order_clause = " ORDER BY "
    if sort_by == 'rating_desc':
        order_clause += "p.rating DESC, p.solved_count DESC"
    elif sort_by == 'solves_desc':
        order_clause += "p.solved_count DESC, p.rating ASC"
    elif sort_by == 'id_asc':
        order_clause += "p.id ASC"
    elif sort_by == 'importance_desc':
        order_clause += "CASE c.importance WHEN '***' THEN 1 WHEN '**' THEN 2 ELSE 3 END, p.rating ASC"
    else:  # rating_asc (default)
        order_clause += "p.rating ASC, p.solved_count DESC"

    # Pagination
    limit = max(1, min(page_size, 100))
    offset = max(0, (page - 1) * limit)

    query_sql = f"""
    SELECT 
        p.id, p.name, p.rating, p.solved_count, p.problem_url, p.editorial_url,
        p.tags, p.time_limit, p.memory_limit,
        c.main_topic, c.subtopic, c.subsubtopic_id, c.subsubtopic,
        c.importance, c.quality_score, c.approach_summary,
        COALESCE(u.is_solved, 0) as is_solved,
        COALESCE(u.is_bookmarked, 0) as is_bookmarked
    FROM categorized_problems c
    JOIN problems p ON c.problem_id = p.id
    LEFT JOIN user_progress u ON p.id = u.problem_id
    {where_clause}
    {order_clause}
    LIMIT ? OFFSET ?
    """
    params.extend([limit, offset])

    cur.execute(query_sql, params)
    rows = cur.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        if isinstance(d.get('tags'), str):
            try:
                d['tags'] = json.loads(d['tags'])
            except Exception:
                d['tags'] = []
        d['is_solved'] = bool(d['is_solved'])
        d['is_bookmarked'] = bool(d['is_bookmarked'])
        results.append(d)

    total_pages = math.ceil(total_count / limit) if total_count > 0 else 1

    return {
        'total': total_count,
        'page': page,
        'page_size': limit,
        'total_pages': total_pages,
        'problems': results
    }


@app.get("/api/problems/{problem_id}")
async def get_problem_detail(problem_id: str):
    """
    Returns complete problem statement, test cases, solution trick, and user notes.
    """
    conn = db.get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT 
        p.id, p.source, p.contest_id, p.problem_index, p.name, p.rating,
        p.solved_count, p.problem_url, p.editorial_url, p.time_limit, p.memory_limit,
        p.description, p.input_specification, p.output_specification,
        p.sample_testcases, p.tags, p.statement_status,
        c.main_topic, c.subtopic, c.subsubtopic_id, c.subsubtopic,
        c.importance, c.quality_score, c.approach_summary,
        COALESCE(u.is_solved, 0) as is_solved,
        COALESCE(u.is_bookmarked, 0) as is_bookmarked,
        COALESCE(u.notes, '') as notes,
        e.title as editorial_title,
        e.key_invariant as editorial_key_invariant,
        e.solution_walkthrough as editorial_solution_walkthrough,
        e.complexity_analysis as editorial_complexity_analysis,
        e.cpp_code as editorial_cpp_code,
        e.full_markdown as editorial_full_markdown
    FROM problems p
    LEFT JOIN categorized_problems c ON p.id = c.problem_id
    LEFT JOIN user_progress u ON p.id = u.problem_id
    LEFT JOIN problem_editorials e ON p.id = e.problem_id
    WHERE p.id = ?
    """, (problem_id,))

    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Problem not found")

    d = dict(row)
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

    d['is_solved'] = bool(d['is_solved'])
    d['is_bookmarked'] = bool(d['is_bookmarked'])

    return d


@app.get("/api/problems/{problem_id}/editorial")
async def get_problem_editorial(problem_id: str):
    """Returns markdown and structured editorial for a problem."""
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM problem_editorials WHERE problem_id = ?", (problem_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Editorial not found")
    return dict(row)


@app.post("/api/user/toggle_solved/{problem_id}")
async def toggle_solved(problem_id: str):
    new_state = db.toggle_problem_solved(problem_id)
    return {'problem_id': problem_id, 'is_solved': new_state}


@app.post("/api/user/toggle_bookmark/{problem_id}")
async def toggle_bookmark(problem_id: str):
    new_state = db.toggle_problem_bookmarked(problem_id)
    return {'problem_id': problem_id, 'is_bookmarked': new_state}


@app.post("/api/user/save_note/{problem_id}")
async def save_note(problem_id: str, payload: NotePayload):
    saved = db.save_problem_note(problem_id, payload.notes)
    return {'problem_id': problem_id, 'notes': saved}


@app.get("/api/user/progress")
async def get_user_progress_data():
    return db.get_user_progress()
