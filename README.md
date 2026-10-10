# Codeforces Categorizer Problem Importer

Comprehensive dataset importer and statement scraper for Codeforces problems, designed to feed categorizer models, tagging systems, and analytics.

## Features

- **Problemset (Rated 1400–3000)**:
  - Total **7,101** rated problems fetched from the official Codeforces API (**100% complete**).
  - Stored in SQLite (`data/cf_problems.db`) and exported to `data/problemset_1400_3000.json`.
  - Full statement scraping:
    - Problem description (with LaTeX math preserved)
    - Input specifications
    - Output specifications
    - Sample test cases (`[{"input": "...", "output": "..."}]`)
    - Official editorial / tutorial links
    - Time and memory limits
- **GYM Contests**:
  - All **2,653** Gym contests inspected across Codeforces.
  - Automatically queries public submissions via Codeforces API to discover contest problems.
  - Total **21,270** Gym problems extracted and indexed.
  - Exported to `data/gym_problems.json`.
- **Individual Problem Exports**:
  - Every single problem (**28,371 files**) is exported to `data/problems/<id>.json`.
- **Fault-Tolerant & Resumable**:
  - Scraping can be paused and resumed anytime; already scraped problems and inspected contests are skipped.
  - SQLite database with transactions, indexes, and full relational tag tables.

---

## Directory Structure

```
CF categorizer/
├── data/
│   ├── cf_problems.db             # Primary SQLite database (28.7 MB)
│   ├── problemset_1400_3000.json  # Master JSON for rated problemset (18.9 MB)
│   ├── gym_problems.json          # Master JSON for Gym problems (12.8 MB)
│   └── problems/                  # 28,371 individual JSON files (<id>.json)
├── src/
│   ├── db.py                      # SQLite models, upsert, stats, and JSON export
│   ├── cf_api.py                  # Codeforces API client
│   ├── parser.py                  # Statement HTML/PDF and editorial parser
│   ├── importer_problemset.py     # Stage 1: Problemset metadata & statement scraper
│   ├── importer_gym.py            # Stage 2: Gym contests & problems importer
│   └── exporter.py                # Statistics reporting and data export
├── main.py                        # Unified CLI interface
├── requirements.txt
└── README.md
```

---

## SQLite Database Schema

### `problems` Table
| Column | Type | Description |
|---|---|---|
| `id` | `TEXT PRIMARY KEY` | e.g., `"1900A"` or `"gym_100001_A"` |
| `source` | `TEXT` | `'problemset'` or `'gym'` |
| `contest_id` | `INTEGER` | Codeforces contest ID |
| `problem_index` | `TEXT` | Problem letter/code (e.g., `'A'`, `'C1'`) |
| `name` | `TEXT` | Title of the problem |
| `rating` | `INTEGER` | Difficulty rating (1400–3000 for problemset, NULL for Gym) |
| `tags` | `TEXT` | JSON array of tags (e.g., `["dp", "math"]`) |
| `solved_count` | `INTEGER` | Number of accepted submissions |
| `problem_url` | `TEXT` | Codeforces problem URL |
| `editorial_url` | `TEXT` | Direct link to official editorial / tutorial |
| `time_limit` | `TEXT` | e.g., `"1 second"` |
| `memory_limit` | `TEXT` | e.g., `"256 megabytes"` |
| `description` | `TEXT` | Problem description statement |
| `input_specification` | `TEXT` | Input format requirements |
| `output_specification` | `TEXT` | Output format requirements |
| `sample_testcases` | `TEXT` | JSON array of `[{"input": "...", "output": "..."}]` |
| `statement_status` | `TEXT` | `'completed'`, `'pending'`, `'error'`, `'pdf_attachment'` |

### `contests` Table
Stores metadata for all contests (standard and GYM), including `id`, `name`, `type`, `phase`, `is_gym`, `difficulty`.

### `problem_tags` Table
Normalized many-to-many relationship between problems and tags for fast indexed querying.

---

## CLI Usage

### 1. Show Current Database Status
```bash
python main.py --status
```

### 2. Import Problemset Metadata (1400–3000)
```bash
python main.py --problemset
```

### 3. Scrape Problem Statements & Editorials
Scrapes descriptions, input/outputs, samples, and tutorial links with multithreading:
```bash
# Scrape all pending problemset statements (default 5 workers)
python main.py --scrape-statements --workers 8

# Scrape next 100 statements
python main.py --scrape-statements --limit 100 --workers 8
```

### 4. Launch Interactive Web Application
Launch the web curriculum explorer to view topics, subtopics, subsubtopics, problem statements with LaTeX math, solution tricks, and personal notes:
```bash
python run_web.py
# or
python main.py --serve --port 8000
```
Open **`http://127.0.0.1:8000`** in any web browser!

### 5. Curriculum Categorization & Roadmap Generation
Classify problems into 576 subtopics, filter quality, and generate Markdown curriculum:
```bash
python main.py --categorize
```

### 6. Export Database to Master JSON Files
```bash
python main.py --export
```

### 7. Export Every Problem to Individual Files
```bash
python main.py --export-individual
```

