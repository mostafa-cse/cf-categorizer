"""Export and statistics reporting utilities."""

import os
from . import db


def print_summary():
    """Display comprehensive database statistics."""
    stats = db.get_db_stats()
    print("=" * 60)
    print("           CODEFORCES CATEGORIZER DATABASE SUMMARY          ")
    print("=" * 60)
    print(f"Total problems stored:           {stats.get('total_problems', 0)}")
    print(f"Problemset problems (all):       {stats.get('problemset_total', 0)}")
    print(f"Problemset rated (1400-3000):    {stats.get('problemset_1400_3000', 0)}")
    print(f"GYM contest problems:            {stats.get('gym_total', 0)}")
    print(f"Unique algorithm tags:           {stats.get('unique_tags_count', 0)}")
    print("-" * 60)
    print("Statement Status Breakdown:")
    for status, cnt in stats.get('status_breakdown', {}).items():
        print(f"  - {status:15}: {cnt}")
    print("=" * 60)


def export_all():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    ps_path = os.path.join(data_dir, 'problemset_1400_3000.json')
    gym_path = os.path.join(data_dir, 'gym_problems.json')

    c1 = db.export_problems_to_json(ps_path, source='problemset', min_rating=1400, max_rating=3000)
    c2 = db.export_problems_to_json(gym_path, source='gym')
    print(f"[+] Exported {c1} problemset problems to {ps_path}")
    print(f"[+] Exported {c2} gym problems to {gym_path}")
