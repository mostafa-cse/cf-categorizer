"""Codeforces API client for fetching problemset and GYM contests."""

import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def make_cf_request(url: str, max_retries: int = 5, backoff: float = 2.0) -> Optional[Dict[str, Any]]:
    """Execute a request against Codeforces official API with retries and exponential backoff."""
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                if data.get('status') == 'OK':
                    return data
                elif 'FAILED' in data.get('status', ''):
                    comment = data.get('comment', '')
                    # If contest not found or requires auth, return None immediately
                    if 'not found' in comment.lower() or 'authenticated' in comment.lower():
                        return data
        except urllib.error.HTTPError as e:
            if e.code == 400:
                try:
                    err_body = json.loads(e.read().decode('utf-8'))
                    return err_body
                except Exception:
                    pass
            if e.code in (429, 503, 502):
                time.sleep(backoff * (attempt + 1))
            else:
                time.sleep(1.0)
        except Exception:
            time.sleep(backoff * (attempt + 1))
    return None


def fetch_problemset_rated(min_rating: int = 1400, max_rating: int = 3000) -> List[Dict[str, Any]]:
    """
    Fetch all problems from the problemset and filter by rating (1400-3000).
    Merges problemStatistics to include solved_count.
    """
    url = "https://codeforces.com/api/problemset.problems"
    response = make_cf_request(url)
    if not response or response.get('status') != 'OK':
        raise RuntimeError(f"Failed to fetch problemset from Codeforces API: {response}")

    result = response['result']
    problems_raw = result.get('problems', [])
    stats_raw = result.get('problemStatistics', [])

    # Map (contestId, index) -> solvedCount
    stats_map: Dict[Tuple[int, str], int] = {}
    for st in stats_raw:
        cid = st.get('contestId')
        idx = st.get('index')
        if cid is not None and idx is not None:
            stats_map[(cid, idx)] = st.get('solvedCount', 0)

    standardized_problems: List[Dict[str, Any]] = []

    for p in problems_raw:
        contest_id = p.get('contestId')
        index = p.get('index')
        rating = p.get('rating')

        # Filter rated problems within specified bounds
        if contest_id is None or index is None:
            continue
        if rating is None or not (min_rating <= rating <= max_rating):
            continue

        prob_id = f"{contest_id}{index}"
        solved = stats_map.get((contest_id, index), 0)
        prob_url = f"https://codeforces.com/problemset/problem/{contest_id}/{index}"

        standardized_problems.append({
            'id': prob_id,
            'source': 'problemset',
            'contest_id': contest_id,
            'problem_index': index,
            'name': p.get('name', ''),
            'rating': rating,
            'tags': p.get('tags', []),
            'solved_count': solved,
            'problem_url': prob_url,
            'statement_status': 'pending'
        })

    return standardized_problems


def fetch_gym_contests() -> List[Dict[str, Any]]:
    """Fetch the full list of GYM contests from Codeforces."""
    url = "https://codeforces.com/api/contest.list?gym=true"
    response = make_cf_request(url)
    if not response or response.get('status') != 'OK':
        raise RuntimeError(f"Failed to fetch GYM contests from Codeforces API: {response}")

    contests = response.get('result', [])
    return contests


def fetch_gym_problems_from_status(contest_id: int, count: int = 100) -> List[Dict[str, Any]]:
    """
    Extract problems from public submissions for a GYM contest via contest.status API.
    Does not require API keys or authentication.
    """
    url = f"https://codeforces.com/api/contest.status?contestId={contest_id}&from=1&count={count}"
    response = make_cf_request(url)
    if not response or response.get('status') != 'OK':
        return []

    submissions = response.get('result', [])
    problems_dict: Dict[str, Dict[str, Any]] = {}

    for sub in submissions:
        p = sub.get('problem')
        if not p:
            continue
        index = p.get('index')
        if not index:
            continue

        prob_id = f"gym_{contest_id}_{index}"
        if prob_id not in problems_dict:
            problems_dict[prob_id] = {
                'id': prob_id,
                'source': 'gym',
                'contest_id': contest_id,
                'problem_index': index,
                'name': p.get('name', f"Problem {index}"),
                'rating': p.get('rating'),  # usually None for gym
                'tags': p.get('tags', []),
                'solved_count': 0,
                'problem_url': f"https://codeforces.com/gym/{contest_id}/problem/{index}",
                'statement_status': 'pending'
            }

    # Sort by problem index
    return sorted(list(problems_dict.values()), key=lambda x: x['problem_index'])
