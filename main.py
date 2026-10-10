"""CLI entry point for Codeforces Problem Importer."""

import argparse
import sys
from src import db
from src import importer_problemset
from src import importer_gym
from src import exporter
from src import curriculum_pipeline

# Configure Windows UTF-8 console output
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass


def main():
    parser = argparse.ArgumentParser(description="Codeforces Problem Importer for CF Categorizer")
    parser.add_argument('--all', action='store_true', help="Import problemset (1400-3000) then GYM contest problems")
    parser.add_argument('--problemset', action='store_true', help="Import rated problemset metadata (1400-3000)")
    parser.add_argument('--scrape-statements', action='store_true', help="Scrape statements & editorials for problemset")
    parser.add_argument('--gym', action='store_true', help="Import GYM contest problems")
    parser.add_argument('--scrape-gym', action='store_true', help="Scrape statements for GYM problems")
    parser.add_argument('--status', action='store_true', help="Show database statistics and status")
    parser.add_argument('--export', action='store_true', help="Export database to master JSON files")
    parser.add_argument('--export-individual', action='store_true', help="Export each problem to its own individual JSON file in data/problems/")
    parser.add_argument('--categorize', action='store_true', help="Classify problems into 576 subtopics, filter quality, and generate roadmap")
    parser.add_argument('--workers', type=int, default=5, help="Number of concurrent scraper workers (default: 5)")
    parser.add_argument('--limit', type=int, default=None, help="Limit number of statements to scrape/categorize")
    parser.add_argument('--max-gym-contests', type=int, default=None, help="Limit number of Gym contests to inspect")
    parser.add_argument('--force', action='store_true', help="Force recomputation and overwrite existing categorized records")
    parser.add_argument('--serve', action='store_true', help="Launch interactive web browser application")
    parser.add_argument('--port', type=int, default=8000, help="Web server port (default: 8000)")

    args = parser.parse_args()

    # Initialize database
    db.init_db()

    if args.serve:
        import uvicorn
        from src.server import app
        print("=" * 65)
        print("       🚀 CODEFORCES CATEGORIZER WEB APPLICATION 🚀      ")
        print("=" * 65)
        print(f"[*] Starting local server at http://127.0.0.1:{args.port}")
        print("[*] Open http://127.0.0.1:8000 in your browser to view all topics & problems")
        print("=" * 65)
        uvicorn.run(app, host="127.0.0.1", port=args.port, log_level="info")
        return

    if args.status:
        exporter.print_summary()
        return

    if args.export:
        exporter.export_all()
        return

    if args.export_individual:
        print("[*] Exporting all problems one by one into data/problems/...")
        count = db.export_all_individual_problems()
        print(f"[+] Successfully exported {count} problems individually.")
        return

    if args.categorize:
        print("[*] Running curriculum categorization pipeline...")
        stats = curriculum_pipeline.run_curriculum_categorization(limit=args.limit, force=args.force)
        print(f"[+] Categorization complete! Processed {stats['total_processed']} problems. Quality Selected: {stats['selected_quality_count']}.")
        return

    if args.problemset:
        importer_problemset.run_metadata_import(min_rating=1400, max_rating=3000)
        exporter.print_summary()
        return

    if args.scrape_statements:
        importer_problemset.scrape_problemset_statements(max_workers=args.workers, limit=args.limit)
        exporter.print_summary()
        return

    if args.gym:
        importer_gym.import_gym_contests_and_problems(max_contests=args.max_gym_contests, workers=min(args.workers, 4))
        exporter.print_summary()
        return

    if args.scrape_gym:
        importer_gym.scrape_gym_statements(max_workers=args.workers, limit=args.limit)
        exporter.print_summary()
        return

    if args.all:
        print("\n=======================================================")
        print("STAGE 1: Codeforces Problemset (Rated 1400-3000)")
        print("=======================================================")
        importer_problemset.run_metadata_import(min_rating=1400, max_rating=3000)

        print("\nScraping problem statements & editorials...")
        importer_problemset.scrape_problemset_statements(max_workers=args.workers, limit=args.limit)

        print("\n=======================================================")
        print("STAGE 2: Codeforces GYM Contests")
        print("=======================================================")
        importer_gym.import_gym_contests_and_problems(max_contests=args.max_gym_contests, workers=min(args.workers, 4))

        exporter.print_summary()
        return

    # Default action if no arguments provided: show help and summary
    exporter.print_summary()
    print("\nUsage options:")
    print("  python main.py --problemset             # Fetch rated 1400-3000 metadata into SQLite & JSON")
    print("  python main.py --scrape-statements      # Scrape full descriptions, samples & editorials")
    print("  python main.py --gym                    # Import GYM contest problems")
    print("  python main.py --all                    # Run full import pipeline")
    print("  python main.py --status                 # Display current import statistics")


if __name__ == '__main__':
    main()
