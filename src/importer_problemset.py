"""Importer for Codeforces Problemset problems (Rated 1400-3000)."""

import os
import sys
import time
import concurrent.futures
from typing import Optional, List, Dict, Any

from . import db
from . import cf_api
from . import parser

JSON_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'problemset_1400_3000.json')


def run_metadata_import(min_rating: int = 1400, max_rating: int = 3000) -> int:
    """
    Fetch all rated problems (1400-3000) from the official API and store them in SQLite.
    Also exports initial JSON.
    """
    print(f"[*] Fetching Codeforces Problemset rated {min_rating}-{max_rating} from API...")
    problems = cf_api.fetch_problemset_rated(min_rating=min_rating, max_rating=max_rating)
    print(f"[+] Retrieved {len(problems)} rated problems ({min_rating}-{max_rating}).")

    print("[*] Storing problem metadata and tags into SQLite database...")
    db.init_db()
    db.bulk_upsert_problems(problems)
    print("[+] Successfully inserted/updated problem metadata in database.")

    print(f"[*] Exporting snapshot to {JSON_PATH}...")
    count = db.export_problems_to_json(JSON_PATH, source='problemset', min_rating=min_rating, max_rating=max_rating)
    print(f"[+] Master JSON exported with {count} problems.")

    return count


def scrape_problemset_statements(max_workers: int = 5, limit: Optional[int] = None, batch_size: int = 25):
    """
    Scrape full problem statements (description, input/output, sample tests, editorial)
    for pending problemset problems using ThreadPoolExecutor.
    """
    pending = db.get_pending_statement_problems(source='problemset', limit=limit)
    total_pending = len(pending)
    if total_pending == 0:
        print("[+] All problemset problems already have statements scraped!")
        return

    print(f"[*] Starting statement scraping for {total_pending} problems with {max_workers} workers...")

    updates_buffer: List[Dict[str, Any]] = []
    processed_count = 0
    t0 = time.time()

    def process_item(item: Dict[str, Any]) -> Dict[str, Any]:
        url = item['problem_url']
        result = parser.fetch_problem_statement(url)
        result['id'] = item['id']
        return result

    id_to_item = {item['id']: item for item in pending}

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
                print(f"[{processed_count}/{total_pending}] Processed {item['id']} ({res.get('statement_status')}) | Speed: {rate:.1f} probs/sec")

            if len(updates_buffer) >= batch_size:
                db.bulk_update_problem_statements(updates_buffer)
                for u in updates_buffer:
                    merged = dict(id_to_item.get(u['id'], {}))
                    merged.update(u)
                    db.save_individual_problem_file(merged)
                updates_buffer.clear()

    if updates_buffer:
        db.bulk_update_problem_statements(updates_buffer)
        for u in updates_buffer:
            merged = dict(id_to_item.get(u['id'], {}))
            merged.update(u)
            db.save_individual_problem_file(merged)
        updates_buffer.clear()

    print("[*] Updating master JSON export with completed statements...")
    db.export_problems_to_json(JSON_PATH, source='problemset', min_rating=1400, max_rating=3000)
    print(f"[+] Done! Processed {processed_count} problem statements in {time.time()-t0:.1f}s.")
