import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import time

# Ensure UTF-8 output on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def log_test(step_num, test_name, status, details=""):
    symbol = "[PASS]" if status else "[FAIL]"
    print(f"{symbol} Step {step_num}: {test_name}")
    if details:
        print(f"       -> {details}")

def get_json(endpoint):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def post_json(endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    payload = json.dumps(data).encode('utf-8') if data else b"{}"
    req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return resp.status, json.loads(resp.read().decode('utf-8'))

def run_all_tests():
    total_passed = 0
    total_failed = 0

    print("=================================================================")
    print("  [*] STEP-BY-STEP VERIFICATION SUITE FOR CF CATEGORIZER")
    print("=================================================================\n")

    # -------------------------------------------------------------
    # STEP 1: Static Web Assets & Health
    # -------------------------------------------------------------
    print("--- [SECTION 1: Static Assets & Web Health] ---")
    try:
        req = urllib.request.Request(f"{BASE_URL}/", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode('utf-8')
            assert resp.status == 200
            assert "CF Categorizer" in html
            assert "MathJax" in html
            assert "marked.min.js" in html
            log_test("1.1", "Home Page HTML serving", True, f"Status 200, length {len(html)} bytes")
            total_passed += 1
    except Exception as e:
        log_test("1.1", "Home Page HTML serving", False, str(e))
        total_failed += 1

    try:
        req = urllib.request.Request(f"{BASE_URL}/static/style.css", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            css = resp.read().decode('utf-8')
            assert resp.status == 200
            assert ".glass-card" in css
            assert ".cf-rating" in css
            log_test("1.2", "Static Stylesheet serving", True, f"Status 200, length {len(css)} bytes")
            total_passed += 1
    except Exception as e:
        log_test("1.2", "Static Stylesheet serving", False, str(e))
        total_failed += 1

    try:
        req = urllib.request.Request(f"{BASE_URL}/static/app.js", headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            js = resp.read().decode('utf-8')
            assert resp.status == 200
            assert "switchModalTab" in js
            assert "downloadCode" in js
            log_test("1.3", "Static App JavaScript serving", True, f"Status 200, length {len(js)} bytes")
            total_passed += 1
    except Exception as e:
        log_test("1.3", "Static App JavaScript serving", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 2: System Stats API
    # -------------------------------------------------------------
    print("\n--- [SECTION 2: System Stats API] ---")
    try:
        status, stats = get_json("/api/stats")
        assert status == 200
        assert stats['total_problems'] >= 28000
        assert stats['curriculum_quality_count'] >= 28000
        assert stats['stars']['***'] > 0
        assert stats['stars']['**'] > 0
        assert stats['stars']['*'] > 0
        assert len(stats['topic_breakdown']) == 11
        log_test("2.1", "Stats endpoint data integrity", True, 
                 f"Total: {stats['total_problems']}, Quality: {stats['curriculum_quality_count']}, Masterpieces: {stats['stars']['***']}")
        total_passed += 1
    except Exception as e:
        log_test("2.1", "Stats endpoint data integrity", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 3: Taxonomy Hierarchy API
    # -------------------------------------------------------------
    print("\n--- [SECTION 3: Taxonomy Hierarchy API] ---")
    try:
        status, taxonomy = get_json("/api/taxonomy")
        assert status == 200
        assert len(taxonomy) == 11

        total_sst_count = 0
        total_problems_in_tax = 0
        for main in taxonomy:
            assert 'name' in main and 'subtopics' in main
            for sub in main['subtopics']:
                assert 'name' in sub and 'subsubtopics' in sub
                for sst in sub['subsubtopics']:
                    total_sst_count += 1
                    total_problems_in_tax += sst['problem_count']

        assert total_sst_count == 576
        log_test("3.1", "576-Technique taxonomy structure", True, 
                 f"11 Main Topics, 576 Subsubtopics, {total_problems_in_tax} problems mapped")
        total_passed += 1
    except Exception as e:
        log_test("3.1", "576-Technique taxonomy structure", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 4: Problem Listing & Filtering API
    # -------------------------------------------------------------
    print("\n--- [SECTION 4: Problem Listing & Filtering API] ---")
    
    # 4.1 Default list
    try:
        status, data = get_json("/api/problems?page=1&page_size=30")
        assert status == 200
        assert data['total'] >= 28000
        assert len(data['problems']) == 30
        log_test("4.1", "Default problem listing & pagination", True, f"Returned 30 of {data['total']} problems")
        total_passed += 1
    except Exception as e:
        log_test("4.1", "Default problem listing & pagination", False, str(e))
        total_failed += 1

    # 4.2 Page size control
    try:
        status, data60 = get_json("/api/problems?page=1&page_size=60")
        assert status == 200
        assert len(data60['problems']) == 60
        log_test("4.2", "Page size selector (60 per page)", True, f"Returned {len(data60['problems'])} items")
        total_passed += 1
    except Exception as e:
        log_test("4.2", "Page size selector (60 per page)", False, str(e))
        total_failed += 1

    # 4.3 Main topic filter
    try:
        status, data_dp = get_json("/api/problems?main_topic=" + urllib.parse.quote("Dynamic Programming (DP)"))
        assert status == 200
        assert data_dp['total'] > 0
        all_dp = all(p['main_topic'] == "Dynamic Programming (DP)" for p in data_dp['problems'])
        assert all_dp
        log_test("4.3", "Filter by Main Topic (Dynamic Programming)", True, f"Found {data_dp['total']} DP problems")
        total_passed += 1
    except Exception as e:
        log_test("4.3", "Filter by Main Topic (Dynamic Programming)", False, str(e))
        total_failed += 1

    # 4.4 Subsubtopic filter (450. Bitmask DP)
    try:
        status, data_bitmask = get_json("/api/problems?subsubtopic_id=450")
        assert status == 200
        assert data_bitmask['total'] > 0
        all_bitmask = all(p['subsubtopic_id'] == 450 for p in data_bitmask['problems'])
        assert all_bitmask
        log_test("4.4", "Filter by Subsubtopic ID #450 (Bitmask DP)", True, f"Found {data_bitmask['total']} Bitmask DP problems")
        total_passed += 1
    except Exception as e:
        log_test("4.4", "Filter by Subsubtopic ID #450 (Bitmask DP)", False, str(e))
        total_failed += 1

    # 4.5 Rating range filter (1800 - 2000)
    try:
        status, data_rating = get_json("/api/problems?min_rating=1800&max_rating=2000")
        assert status == 200
        assert data_rating['total'] > 0
        valid_range = all(1800 <= p['rating'] <= 2000 for p in data_rating['problems'] if p['rating'])
        assert valid_range
        log_test("4.5", "Filter by Rating Range (1800 - 2000)", True, f"Found {data_rating['total']} problems in range")
        total_passed += 1
    except Exception as e:
        log_test("4.5", "Filter by Rating Range (1800 - 2000)", False, str(e))
        total_failed += 1

    # 4.6 Importance filter (Masterpieces)
    try:
        status, data_stars = get_json("/api/problems?importance=" + urllib.parse.quote("***"))
        assert status == 200
        assert data_stars['total'] > 0
        all_masterpieces = all(p['importance'] == '***' for p in data_stars['problems'])
        assert all_masterpieces
        log_test("4.6", "Filter by Importance (★★★ Masterpieces)", True, f"Found {data_stars['total']} Masterpiece problems")
        total_passed += 1
    except Exception as e:
        log_test("4.6", "Filter by Importance (★★★ Masterpieces)", False, str(e))
        total_failed += 1

    # 4.7 Text search query
    try:
        status, data_q = get_json("/api/problems?q=1497D")
        assert status == 200
        assert data_q['total'] >= 1
        found_id = any(p['id'] == '1497D' for p in data_q['problems'])
        assert found_id
        log_test("4.7", "Full-text search by ID (1497D)", True, f"Successfully matched problem 1497D")
        total_passed += 1
    except Exception as e:
        log_test("4.7", "Full-text search by ID (1497D)", False, str(e))
        total_failed += 1

    # 4.8 Sorting orders
    try:
        status, data_asc = get_json("/api/problems?sort_by=rating_asc&page_size=10")
        ratings_asc = [p['rating'] for p in data_asc['problems'] if p['rating'] is not None]
        assert ratings_asc == sorted(ratings_asc)

        status, data_desc = get_json("/api/problems?sort_by=rating_desc&page_size=10")
        ratings_desc = [p['rating'] for p in data_desc['problems'] if p['rating'] is not None]
        assert ratings_desc == sorted(ratings_desc, reverse=True)

        log_test("4.8", "Sorting orders (rating_asc & rating_desc)", True, "Ascending and Descending verified")
        total_passed += 1
    except Exception as e:
        log_test("4.8", "Sorting orders (rating_asc & rating_desc)", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 5: Problem Detail & Statement API
    # -------------------------------------------------------------
    print("\n--- [SECTION 5: Problem Detail & Statement API] ---")
    test_problem_ids = ['1497D', '1000B', '504D', '1520F1']
    for pid in test_problem_ids:
        try:
            status, p = get_json(f"/api/problems/{pid}")
            assert status == 200
            assert p['id'] == pid
            assert len(p['name']) > 0
            assert p['rating'] is not None
            assert len(p['description']) > 0
            assert 'sample_testcases' in p
            assert len(p['editorial_title']) > 0
            assert len(p['editorial_key_invariant']) > 0
            assert len(p['editorial_solution_walkthrough']) > 0
            assert len(p['editorial_complexity_analysis']) > 0
            assert len(p['editorial_cpp_code']) > 0
            assert len(p['editorial_full_markdown']) > 0
            log_test(f"5.{pid}", f"Problem Statement & Editorial: {pid} ({p['name']})", True, 
                     f"Rating: {p['rating']}, Subtopic: {p['subsubtopic']}, C++ Code: {len(p['editorial_cpp_code'])} chars")
            total_passed += 1
        except Exception as e:
            log_test(f"5.{pid}", f"Problem Statement & Editorial: {pid}", False, str(e))
            total_failed += 1

    # -------------------------------------------------------------
    # STEP 6: Dedicated Editorial API
    # -------------------------------------------------------------
    print("\n--- [SECTION 6: Dedicated Editorial API] ---")
    try:
        status, ed = get_json("/api/problems/1497D/editorial")
        assert status == 200
        assert ed['problem_id'] == '1497D'
        assert "Bitmask DP" in ed['title']
        assert "#include <bits/stdc++.h>" in ed['cpp_code']
        assert "Time Complexity" in ed['complexity_analysis']
        log_test("6.1", "Dedicated Editorial endpoint (/api/problems/1497D/editorial)", True, 
                 f"Title: {ed['title']}, Markdown length: {len(ed['full_markdown'])}")
        total_passed += 1
    except Exception as e:
        log_test("6.1", "Dedicated Editorial endpoint (/api/problems/1497D/editorial)", False, str(e))
        total_failed += 1

    try:
        # Non-existent problem should 404 cleanly
        url = f"{BASE_URL}/api/problems/999999Z/editorial"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            with urllib.request.urlopen(req) as resp:
                pass
            log_test("6.2", "404 for invalid problem editorial", False, "Expected 404 but got success")
            total_failed += 1
        except urllib.error.HTTPError as he:
            assert he.code == 404
            log_test("6.2", "404 Error handling for non-existent editorial", True, "Returned HTTP 404 correctly")
            total_passed += 1
    except Exception as e:
        log_test("6.2", "404 Error handling for non-existent editorial", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 7: User Progress & Interaction API
    # -------------------------------------------------------------
    print("\n--- [SECTION 7: User Progress & Interaction API] ---")
    test_pid = "1497D"
    
    # 7.1 Toggle Solved
    try:
        status1, res1 = post_json(f"/api/user/toggle_solved/{test_pid}")
        state1 = res1['is_solved']
        status2, res2 = post_json(f"/api/user/toggle_solved/{test_pid}")
        state2 = res2['is_solved']
        assert state1 != state2
        log_test("7.1", "Toggle solved status", True, f"Flipped from {not state1} -> {state1} -> {state2}")
        total_passed += 1
    except Exception as e:
        log_test("7.1", "Toggle solved status", False, str(e))
        total_failed += 1

    # 7.2 Toggle Bookmark
    try:
        status1, res1 = post_json(f"/api/user/toggle_bookmark/{test_pid}")
        state1 = res1['is_bookmarked']
        status2, res2 = post_json(f"/api/user/toggle_bookmark/{test_pid}")
        state2 = res2['is_bookmarked']
        assert state1 != state2
        log_test("7.2", "Toggle bookmark status", True, f"Flipped from {not state1} -> {state1} -> {state2}")
        total_passed += 1
    except Exception as e:
        log_test("7.2", "Toggle bookmark status", False, str(e))
        total_failed += 1

    # 7.3 Save Note
    try:
        test_note = f"Verification note written at {time.time()}: Bitmask size is 2^n!"
        status, res = post_json(f"/api/user/save_note/{test_pid}", {"notes": test_note})
        assert status == 200
        assert res['notes'] == test_note
        
        # Verify note is loaded back via problem detail
        _, detail = get_json(f"/api/problems/{test_pid}")
        assert detail['notes'] == test_note

        log_test("7.3", "Save & persist personal notes", True, f"Saved & verified: '{test_note[:35]}...'")
        total_passed += 1
    except Exception as e:
        log_test("7.3", "Save & persist personal notes", False, str(e))
        total_failed += 1

    # 7.4 User Progress Summary
    try:
        status, prog = get_json("/api/user/progress")
        assert status == 200
        assert 'solved' in prog and 'bookmarked' in prog and 'notes' in prog
        log_test("7.4", "User progress snapshot", True, 
                 f"Solved: {len(prog['solved'])}, Bookmarked: {len(prog['bookmarked'])}, Notes: {len(prog['notes'])}")
        total_passed += 1
    except Exception as e:
        log_test("7.4", "User progress snapshot", False, str(e))
        total_failed += 1

    # -------------------------------------------------------------
    # STEP 8: External Link Formatting Verification
    # -------------------------------------------------------------
    print("\n--- [SECTION 8: External Link Formatting Verification] ---")
    try:
        status, sample_data = get_json("/api/problems?page=1&page_size=50")
        assert status == 200
        valid_links = 0
        for p in sample_data['problems']:
            url = p['problem_url']
            assert url.startswith("https://codeforces.com/")
            assert "/problem/" in url or "/gym/" in url
            if p.get('editorial_url'):
                assert p['editorial_url'].startswith("https://codeforces.com/blog/entry/")
            valid_links += 1

        log_test("8.1", "Codeforces Problem & Editorial Link URLs", True, 
                 f"Verified {valid_links} external problem & editorial URLs format")
        total_passed += 1
    except Exception as e:
        log_test("8.1", "Codeforces Problem & Editorial Link URLs", False, str(e))
        total_failed += 1

    print("\n=================================================================")
    print(f"  [+] TEST SUITE FINISHED: {total_passed} PASSED | {total_failed} FAILED")
    print("=================================================================")
    return total_failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
