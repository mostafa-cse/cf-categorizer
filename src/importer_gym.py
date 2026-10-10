"""Importer for Codeforces GYM Contests and problems."""

import os
import time
import concurrent.futures
from typing import Optional, List, Dict, Any

from . import db
from . import cf_api
from . import parser

GYM_JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'gym_problems.json')


def import_gym_contests_and_problems(max_contests: Optional[int] = None, workers: int = 3) -> int:
    """
    Import GYM contests and discover all problems submitted to each contest via status API.
    Uses concurrent workers with rate limiting to comply with Codeforces API guidelines.
    """
    print("[*] Fetching list of all GYM contests from Codeforces API...")
    contests = cf_api.fetch_gym_contests()
    print(f"[+] Found {len(contests)} GYM contests.")

    # Store contests in SQLite if not present
    conn = db.get_db_connection()
    cur = conn.cursor()
    cur.executemany("""
    INSERT INTO contests (id, name, type, phase, is_gym, difficulty, inspected)
    VALUES (?, ?, ?, ?, 1, ?, 0)
    ON CONFLICT(id) DO UPDATE SET
        name = excluded.name,
        type = excluded.type,
        phase = excluded.phase,
        difficulty = excluded.difficulty
    """, [(c['id'], c.get('name', ''), c.get('type'), c.get('phase'), c.get('difficulty')) for c in contests])
    conn.commit()

    already_done = set(r[0] for r in cur.execute("SELECT id FROM contests WHERE is_gym = 1 AND inspected = 1").fetchall())
    conn.close()

    remaining_contests = [c for c in contests if c['id'] not in already_done]
    target_contests = remaining_contests if max_contests is None else remaining_contests[:max_contests]
    total_to_process = len(target_contests)
    print(f"[*] Found {len(already_done)} Gym contests already inspected. Processing {total_to_process} remaining Gym contests with {workers} workers...")

    total_gym_problems = 0
    batch_problems: List[Dict[str, Any]] = []
    inspected_cids_buffer: List[int] = []
    processed_count = 0

    def process_contest(c: Dict[str, Any]) -> List[Dict[str, Any]]:
        cid = c['id']
        time.sleep(0.3)  # Gentle polite delay per thread
        return cf_api.fetch_gym_problems_from_status(cid)

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        future_to_contest = {executor.submit(process_contest, c): c for c in target_contests}

        for future in concurrent.futures.as_completed(future_to_contest):
            c = future_to_contest[future]
            processed_count += 1
            cid = c['id']
            inspected_cids_buffer.append(cid)
            try:
                probs = future.result()
                if probs:
                    batch_problems.extend(probs)
                    total_gym_problems += len(probs)
            except Exception as e:
                pass

            if processed_count % 25 == 0 or processed_count == total_to_process:
                print(f"[{processed_count}/{total_to_process}] Inspected Gym {cid} | Total Gym problems discovered so far: {total_gym_problems}")

            if len(batch_problems) >= 100 or len(inspected_cids_buffer) >= 50:
                if batch_problems:
                    db.bulk_upsert_problems(batch_problems)
                    for p in batch_problems:
                        db.save_individual_problem_file(p)
                    batch_problems.clear()
                if inspected_cids_buffer:
                    conn = db.get_db_connection()
                    conn.executemany("UPDATE contests SET inspected = 1 WHERE id = ?", [(cid,) for cid in inspected_cids_buffer])
                    conn.commit()
                    conn.close()
                    inspected_cids_buffer.clear()

    if batch_problems:
        db.bulk_upsert_problems(batch_problems)
        for p in batch_problems:
            db.save_individual_problem_file(p)
        batch_problems.clear()

    if inspected_cids_buffer:
        conn = db.get_db_connection()
        conn.executemany("UPDATE contests SET inspected = 1 WHERE id = ?", [(cid,) for cid in inspected_cids_buffer])
        conn.commit()
        conn.close()
        inspected_cids_buffer.clear()

    print(f"[*] Exporting Gym problems to {GYM_JSON_PATH}...")
    count = db.export_problems_to_json(GYM_JSON_PATH, source='gym')
    print(f"[+] Exported {count} Gym problems to JSON.")
    return count


def scrape_gym_statements(max_workers: int = 5, limit: Optional[int] = None, batch_size: int = 25):
    """Scrape statements / detect PDFs for pending Gym problems."""
    pending = db.get_pending_statement_problems(source='gym', limit=limit)
    total_pending = len(pending)
    if total_pending == 0:
        print("[+] No pending Gym statements to scrape.")
        return

    print(f"[*] Scraping statements for {total_pending} Gym problems with {max_workers} workers...")
    updates_buffer: List[Dict[str, Any]] = []
    processed_count = 0
    t0 = time.time()

    def process_item(item: Dict[str, Any]) -> Dict[str, Any]:
        url = item['problem_url']
        result = parser.fetch_problem_statement(url)
        result['id'] = item['id']
        return result

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_item = {executor.submit(process_item, item): item for item in pending}

        for future in concurrent.futures.as_completed(future_to_item):
            item = future_to_item[future]
            try:
                res = future.result()
            except Exception as e:
                res = {'id': item['id'], 'statement_status': 'error', 'description': str(e)}

            updates_buffer.append(res)
            processed_count += 1

            if processed_count % 10 == 0 or processed_count == total_pending:
                elapsed = time.time() - t0
                rate = processed_count / elapsed if elapsed > 0 else 0
                print(f"[{processed_count}/{total_pending}] Gym {item['id']} ({res.get('statement_status')}) | Speed: {rate:.1f} probs/sec")

            if len(updates_buffer) >= batch_size:
                db.bulk_update_problem_statements(updates_buffer)
                updates_buffer.clear()

    if updates_buffer:
        db.bulk_update_problem_statements(updates_buffer)
        updates_buffer.clear()

    print("[*] Updating master Gym JSON export...")
    db.export_problems_to_json(GYM_JSON_PATH, source='gym')
    print(f"[+] Completed {processed_count} Gym problem statements in {time.time()-t0:.1f}s.")
