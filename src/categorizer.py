"""Intelligent Problem Categorizer, Quality Filter, and Solution Strategy Engine."""

import re
import json
from typing import Dict, Any, List, Tuple, Optional
from .taxonomy import TAXONOMY


# Pre-flatten taxonomy for fast keyword and semantic lookup
FLATTENED_TAXONOMY: List[Dict[str, Any]] = []

for main_topic, subtopics in TAXONOMY.items():
    for subtopic, subsubtopics in subtopics.items():
        for item in subsubtopics:
            subsub_id = item[0]
            subsub_name = item[1]
            keywords = item[2]
            FLATTENED_TAXONOMY.append({
                'main_topic': main_topic,
                'subtopic': subtopic,
                'subsubtopic_id': subsub_id,
                'subsubtopic': f"{subsub_id}. {subsub_name}",
                'raw_name': subsub_name,
                'keywords': keywords
            })


# Highly prized pedagogical tricks that immediately boost problem importance to ***
MASTERPIECE_PATTERNS = [
    ("segment tree beats", "Segment Tree Beats"),
    ("aliens trick", "Aliens Trick / WQS Binary Search"),
    ("wqs binary search", "Aliens Trick / WQS Binary Search"),
    ("dsu on tree", "DSU on Tree and Small to Large Merging"),
    ("slope trick", "Slope Trick"),
    ("li chao tree", "Li Chao Tree"),
    ("centroid decomposition", "Centroid Decomposition"),
    ("heavy light decomposition", "Heavy Light Decomposition (HLD) ft Subtrees and Path Query"),
    ("hld", "Heavy Light Decomposition (HLD) ft Subtrees and Path Query"),
    ("rerooting", "Rerooting Technique"),
    ("virtual tree", "Virtual Tree / Auxiliary Tree"),
    ("auxiliary tree", "Virtual Tree / Auxiliary Tree"),
    ("suffix automaton", "Suffix Automaton"),
    ("palindromic tree", "Palindromic Tree / Eertree"),
    ("eertree", "Palindromic Tree / Eertree"),
    ("fft", "Fast Fourier Transform (FFT)"),
    ("ntt", "Number Theoretic Transform (NTT)"),
    ("fwht", "Fast Walsh Hadamard Transform (FWHT) and its Variations"),
    ("berlekamp massey", "Berlekamp Massey"),
    ("xor basis", "Vector Space and XOR Basis"),
    ("linear basis", "Vector Space and XOR Basis"),
    ("meet in the middle", "Meet in the Middle"),
    ("mo's algorithm", "Mo's Algorithm"),
    ("cdq divide and conquer", "CDQ Divide and Conquer"),
    ("link cut tree", "Link Cut Tree (LCT)"),
    ("dinic", "Maximum Flow / Minimum Cut"),
    ("min cost max flow", "Min Cost Max Flow (MCMF)"),
    ("mcmf", "Min Cost Max Flow (MCMF)"),
    ("sos dp", "Sum Over Subsets DP (SOS DP)"),
    ("convex hull trick", "Convex Hull Trick (CHT) and Dynamic CHT"),
    ("cht", "Convex Hull Trick (CHT) and Dynamic CHT"),
    ("two pointers", "Two Pointers"),
    ("binary lifting", "Binary Lifting and LCA"),
    ("2-sat", "2 SAT"),
    ("euler tour", "Euler Tour Technique"),
    ("block cut tree", "Articulation Points and Block Cut Tree"),
    ("bridge", "Articulation Bridges and Bridge Tree"),
    ("scc", "Strongly Connected Components (SCC)"),
    ("tarjan", "Strongly Connected Components (SCC)"),
    ("matrix exponentiation", "Matrix Exponentiation"),
    ("chinese remainder theorem", "Chinese Remainder Theorem (CRT)"),
    ("miller rabin", "Miller-Rabin Primality Test"),
    ("pollard rho", "Pollard Rho"),
    ("mobius inversion", "Mobius Function and Mobius Inversion"),
    ("burnside's lemma", "Burnside's Lemma / Polya Enumeration Theorem"),
    ("grundy", "Grundy Number and Basic Game Theory"),
    ("sprague-grundy", "Grundy Number and Basic Game Theory"),
    ("nim", "Grundy Number and Basic Game Theory"),
    ("convex hull", "Convex Hull(2D)"),
    ("sweep line", "Sweep Line Algorithm and Radial Sweep"),
    ("aho corasick", "Aho Corasick"),
    ("aho-corasick", "Aho Corasick"),
    ("kmp", "Knuth Morris Pratt (KMP) and Prefix Automaton"),
    ("z-algorithm", "Z Algorithm"),
    ("z algorithm", "Z Algorithm")
]


def evaluate_quality(problem: Dict[str, Any]) -> Tuple[bool, int, str]:
    """
    Evaluates whether a problem is high quality for learning algorithms/tricks.
    Filters out pure tedious implementation, uninformative problems, or non-educational problems.
    Returns: (is_selected, quality_score, reason)
    """
    name = (problem.get('name') or '').lower()
    desc = (problem.get('description') or '').lower()
    tags = [t.lower() for t in problem.get('tags', [])]
    rating = problem.get('rating') or 1500
    solved_count = problem.get('solved_count') or 0

    # Red flag keywords for boring/trivial/pure implementation problems
    boilerplate_flags = [
        "tic-tac-toe", "rock-paper-scissors", "calculator", "roman numerals",
        "calendar", "leap year", "rubik", "chess board simulation"
    ]
    if any(flag in name for flag in boilerplate_flags) and rating < 1600:
        return False, 20, "Boilerplate simulation problem with low algorithmic value"

    # Problems with only tag 'implementation' and no statement structure
    if tags == ['implementation'] and rating < 1500 and not any(k in desc for k in ['dp', 'tree', 'graph', 'xor', 'mod', 'query']):
        return False, 30, "Pure routine implementation without generalizable tricks"

    # Problems without a description (e.g. missing statement)
    if not desc or len(desc.strip()) < 50:
        return False, 10, "Statement text unavailable or incomplete"

    # High quality calculation
    score = 60
    # Rating bonus
    if 1600 <= rating <= 2400:
        score += 20  # Sweet spot for contest tricks
    elif rating > 2400:
        score += 15

    # Solved count / popularity bonus
    if solved_count > 1000:
        score += 15
    elif solved_count > 300:
        score += 10

    # Trick indicators in statement/editorial
    trick_indicators = [
        "optimal", "minimum operations", "modulo", "bitwise", "tree", "graph",
        "maximum possible", "lexicographically", "independent", "subarray",
        "subsequence", "inversion", "parity", "construct", "queries"
    ]
    matches = sum(1 for ind in trick_indicators if ind in desc)
    score += min(matches * 2, 20)

    is_selected = score >= 65
    return is_selected, score, "Selected for core algorithmic trick and educational value" if is_selected else "Excluded as low pedagogical impact"


def match_topics(problem: Dict[str, Any]) -> Dict[str, Any]:
    """
    Matches problem text, tags, and constraints against the 576 subsubtopics taxonomy.
    """
    text = f"{problem.get('name', '')} {problem.get('description', '')} {problem.get('input_specification', '')}".lower()
    tags = [t.lower() for t in problem.get('tags', [])]
    rating = problem.get('rating') or 1500

    best_entry = None
    best_score = -1
    detected_tricks = []

    # 1. First check Masterpiece patterns with word boundaries
    for pat, canonical_subsub in MASTERPIECE_PATTERNS:
        if re.search(rf'\b{re.escape(pat)}\b', text) or any(pat == t or re.search(rf'\b{re.escape(pat)}\b', t) for t in tags):
            detected_tricks.append(canonical_subsub)
            for entry in FLATTENED_TAXONOMY:
                if canonical_subsub.lower() in entry['raw_name'].lower():
                    best_entry = entry
                    best_score = 100
                    break
        if best_entry and best_score >= 100:
            break

    # Fast lookup table by subsubtopic ID
    lookup_by_id = {e['subsubtopic_id']: e for e in FLATTENED_TAXONOMY}

    # 2. Semantic matching rules by tag combinations and domain signals
    if not best_entry:
        if 'dp' in tags:
            if 'trees' in tags or 'subtree' in text or 'tree dp' in text:
                best_entry = lookup_by_id.get(463)  # DP on Trees and DAGs
            elif 'bitmasks' in tags or 'bitmask' in text or 'submask' in text:
                best_entry = lookup_by_id.get(450)  # Bitmask DP
            elif 'probabilities' in tags or 'expected' in text:
                best_entry = lookup_by_id.get(459)  # Probability DP
            elif 'digit' in text or 'digits' in text:
                best_entry = lookup_by_id.get(439)  # Digit DP
            elif 'interval' in text or 'range dp' in text:
                best_entry = lookup_by_id.get(461)  # Interval DP
            elif 'subsequence' in text and 'longest' in text:
                best_entry = lookup_by_id.get(460)  # LIS
            elif 'sos' in text:
                best_entry = lookup_by_id.get(451)  # SOS DP
            else:
                best_entry = lookup_by_id.get(437)  # Knapsack and Basic DP
        elif 'games' in tags:
            if 'grundy' in text or 'nim' in text or 'mex' in text:
                best_entry = lookup_by_id.get(472)  # Grundy Number and Basic Game Theory
            elif 'graphs' in tags:
                best_entry = lookup_by_id.get(476)  # Games on Arbitrary Graphs
            else:
                best_entry = lookup_by_id.get(472)
        elif 'flows' in tags:
            if 'cost' in text or 'min cost' in text:
                best_entry = lookup_by_id.get(216)  # Min Cost Max Flow (MCMF)
            else:
                best_entry = lookup_by_id.get(215)  # Maximum Flow / Minimum Cut
        elif 'shortest paths' in tags:
            if '0-1' in text or '0/1' in text or 'deque' in text:
                best_entry = lookup_by_id.get(174)  # 0/1 BFS
            elif 'floyd' in text or 'all pairs' in text:
                best_entry = lookup_by_id.get(170)  # Floyd Warshall
            elif 'bellman' in text:
                best_entry = lookup_by_id.get(171)  # Bellman Ford
            else:
                best_entry = lookup_by_id.get(168)  # Dijkstra's Algorithm
        elif 'string suffix structures' in tags:
            if 'automaton' in text or 'sam' in text:
                best_entry = lookup_by_id.get(419)  # Suffix Automaton
            else:
                best_entry = lookup_by_id.get(416)  # Suffix Array
        elif 'hashing' in tags:
            best_entry = lookup_by_id.get(410)      # String Hashing
        elif 'matrices' in tags:
            best_entry = lookup_by_id.get(355)      # Matrix Exponentiation
        elif 'fft' in tags:
            if 'ntt' in text or '998244353' in text:
                best_entry = lookup_by_id.get(327)  # Number Theoretic Transform (NTT)
            else:
                best_entry = lookup_by_id.get(326)  # Fast Fourier Transform (FFT)
        elif 'meet-in-the-middle' in tags:
            best_entry = lookup_by_id.get(554)      # Meet in the Middle
        elif 'ternary search' in tags:
            best_entry = lookup_by_id.get(538)      # Ternary Search
        elif '2-sat' in tags:
            best_entry = lookup_by_id.get(191)      # 2 SAT
        elif 'interactive' in tags:
            best_entry = lookup_by_id.get(542)      # Interactive Problems
        elif 'trees' in tags and 'dp' not in tags:
            if 'diameter' in text:
                best_entry = lookup_by_id.get(143)  # Tree Diameter
            elif 'lca' in text or 'ancestor' in text or 'binary lifting' in text:
                best_entry = lookup_by_id.get(146)  # Binary Lifting and LCA
            elif 'euler' in text:
                best_entry = lookup_by_id.get(144)  # Euler Tour Technique
            elif 'centroid' in text:
                best_entry = lookup_by_id.get(101)  # Centroid Decomposition
            elif 'heavy' in text and 'light' in text:
                best_entry = lookup_by_id.get(100)  # Heavy Light Decomposition (HLD)
            elif 'data structures' in tags:
                best_entry = lookup_by_id.get(57)   # Segment Tree
            else:
                best_entry = lookup_by_id.get(146)  # Binary Lifting and LCA
        elif 'dsu' in tags:
            if 'rollback' in text:
                best_entry = lookup_by_id.get(81)   # DSU with Rollbacks
            else:
                best_entry = lookup_by_id.get(80)   # DSU / Union Find
        elif 'combinatorics' in tags:
            if 'inclusion' in text or 'exclusion' in text:
                best_entry = lookup_by_id.get(305)  # Principle of Inclusion and Exclusion (PIE)
            elif 'catalan' in text:
                best_entry = lookup_by_id.get(303)  # Catalan Numbers
            elif 'stirling' in text:
                best_entry = lookup_by_id.get(316)  # Stirling Numbers
            elif 'partition' in text:
                best_entry = lookup_by_id.get(321)  # Partitions of an Integer
            elif 'burnside' in text or 'polya' in text:
                best_entry = lookup_by_id.get(323)  # Burnside's Lemma
            else:
                best_entry = lookup_by_id.get(310)  # Large Factorials and Binomial Coefficients
        elif 'number theory' in tags:
            if 'mobius' in text:
                best_entry = lookup_by_id.get(258)  # Mobius Function and Mobius Inversion
            elif 'gcd' in text or 'lcm' in text:
                best_entry = lookup_by_id.get(262)  # Euclidean Algorithm
            elif 'modulo' in text or 'inverse' in text:
                best_entry = lookup_by_id.get(266)  # Modular Arithmetic
            else:
                best_entry = lookup_by_id.get(242)  # Sieve, Prime Factorization and Divisors
        elif 'strings' in tags:
            if 'kmp' in text or 'prefix function' in text:
                best_entry = lookup_by_id.get(406)  # Knuth Morris Pratt (KMP)
            elif 'z-algorithm' in text or 'z algorithm' in text:
                best_entry = lookup_by_id.get(407)  # Z Algorithm
            elif 'aho' in text:
                best_entry = lookup_by_id.get(414)  # Aho Corasick
            elif 'palindrome' in text:
                best_entry = lookup_by_id.get(422)  # Palindromic Tree / Eertree
            elif 'subsequence' in text:
                best_entry = lookup_by_id.get(427)  # Longest Common Subsequence (LCS)
            else:
                best_entry = lookup_by_id.get(406)  # KMP and Prefix Automaton
        elif 'geometry' in tags:
            if 'convex hull' in text:
                best_entry = lookup_by_id.get(491)  # Convex Hull (2D)
            elif 'sweep line' in text:
                best_entry = lookup_by_id.get(521)  # Sweep Line Algorithm and Radial Sweep
            else:
                best_entry = lookup_by_id.get(480)  # 2D Geometry Basics
        elif 'data structures' in tags:
            if 'fenwick' in text or 'bit' in text:
                best_entry = lookup_by_id.get(70)   # BIT / Fenwick Tree
            elif 'sparse table' in text:
                best_entry = lookup_by_id.get(75)   # Sparse Table
            elif 'trie' in text:
                best_entry = lookup_by_id.get(78)   # Trie on Strings and Bits
            elif 'treap' in text:
                best_entry = lookup_by_id.get(105)  # Treap
            elif 'lazy' in text:
                best_entry = lookup_by_id.get(58)   # Segment Tree with Lazy Propagation
            elif 'stack' in text:
                best_entry = lookup_by_id.get(124)  # Monotonic Stack
            else:
                best_entry = lookup_by_id.get(57)   # Segment Tree (Point Update Range Query)
        elif 'two pointers' in tags:
            best_entry = lookup_by_id.get(34)       # Two Pointers
        elif 'binary search' in tags:
            best_entry = lookup_by_id.get(33)       # Binary Search
        elif 'divide and conquer' in tags:
            best_entry = lookup_by_id.get(43)       # Divide and Conquer
        elif 'bitmasks' in tags:
            best_entry = lookup_by_id.get(13)       # Bitwise Operations and Bitmasks
        elif 'sortings' in tags:
            best_entry = lookup_by_id.get(42)       # C++ STL Sort and Custom Comparator
        elif 'greedy' in tags:
            best_entry = lookup_by_id.get(44)       # Basic Greedy Algorithms
        elif 'constructive algorithms' in tags:
            best_entry = lookup_by_id.get(45)       # Basic Constructive Algorithms
        elif 'graphs' in tags or 'dfs and similar' in tags:
            if 'topological' in text or 'dag' in text or 'cycle' in text:
                best_entry = lookup_by_id.get(142)  # Topological Sorting
            elif 'bridge' in text:
                best_entry = lookup_by_id.get(150)  # Articulation Bridges and Bridge Tree
            elif 'articulation' in text:
                best_entry = lookup_by_id.get(152)  # Articulation Points and Block Cut Tree
            elif 'scc' in text:
                best_entry = lookup_by_id.get(148)  # Strongly Connected Components (SCC)
            elif 'mst' in text or 'spanning tree' in text:
                best_entry = lookup_by_id.get(159)  # Minimum Spanning Tree (MST)
            elif 'bfs' in text:
                best_entry = lookup_by_id.get(140)  # Breadth First Search (BFS)
            else:
                best_entry = lookup_by_id.get(139)  # Depth First Search (DFS)
        elif 'math' in tags:
            if 'matrix' in text:
                best_entry = lookup_by_id.get(355)  # Matrix Exponentiation
            elif 'probability' in text or 'expected' in text:
                best_entry = lookup_by_id.get(393)  # Probabilities and Expected Values
            elif 'gaussian' in text:
                best_entry = lookup_by_id.get(369)  # Gaussian Elimination
            else:
                best_entry = lookup_by_id.get(242)  # Sieve, Prime Factorization and Divisors
        else:
            best_entry = lookup_by_id.get(44)       # Default: Basic Greedy Algorithms

    # Default fallback to first entry if somehow still None
    if not best_entry:
        best_entry = FLATTENED_TAXONOMY[0]

    # Determine Importance: *, **, ***
    solved_count = problem.get('solved_count') or 0
    if rating >= 2200 or best_score >= 80 or any(t in best_entry['raw_name'].lower() for t in [
        'segment tree', 'flow', 'dsu on tree', 'centroid', 'fft', 'ntt', 'xor basis', 'cht', 'slope trick', 'automaton'
    ]):
        importance = "***"
    elif rating >= 1600 or solved_count > 1500 or best_score >= 35:
        importance = "**"
    else:
        importance = "*"

    # Derive Core Algorithmic Approach & Key Trick
    approach = generate_approach_summary(problem, best_entry)

    return {
        'main_topic': best_entry['main_topic'],
        'subtopic': best_entry['subtopic'],
        'subsubtopic_id': best_entry['subsubtopic_id'],
        'subsubtopic': best_entry['subsubtopic'],
        'importance': importance,
        'approach_summary': approach,
        'detected_tricks': detected_tricks
    }


def generate_approach_summary(problem: Dict[str, Any], taxonomy_entry: Dict[str, Any]) -> str:
    """
    Synthesizes the core algorithmic logic and trick explanation for the problem.
    Provides precise, pedagogy-focused invariants, state definitions, and asymptotic bounds.
    """
    subsub = taxonomy_entry['raw_name']
    main_topic = taxonomy_entry['main_topic']
    subsub_id = taxonomy_entry['subsubtopic_id']

    if subsub_id == 463 or "Tree" in subsub and "DP" in subsub:
        return "Define tree DP state dp[u][state] computing optimal subproblem values for the subtree rooted at u. Aggregate transitions across children in post-order traversal in O(N × S) time."
    elif subsub_id == 450 or "Bitmask DP" in subsub:
        return "Define state dp[mask][i] capturing the subset of visited/chosen elements. Transition by iterating over valid unset bits in O(2^N × N) time."
    elif subsub_id == 439 or "Digit DP" in subsub:
        return "Express count as f(R) - f(L-1). Define memoized state dp[pos][tight][leading_zeros][cond] scanning digits from most to least significant in O(digits × base × states)."
    elif subsub_id == 461 or "Interval DP" in subsub:
        return "Iterate over interval length len from 1 to N and left endpoint l. Transition by splitting at midpoint k: dp[l][r] = min/max_k (dp[l][k] + dp[k+1][r] + cost) in O(N^3)."
    elif subsub_id == 451 or "SOS DP" in subsub:
        return "Apply Sum Over Subsets DP using iterative prefix SOS transformations over dimension i from 0 to D-1. Compute sum over all submasks/supermasks in O(D × 2^D) time."
    elif subsub_id == 445 or "Convex Hull Trick" in subsub or "CHT" in subsub:
        return "Model the DP transition as y = m*x + c. Maintain the upper/lower envelope of linear functions via CHT or Li Chao Tree to query the optimum in O(log N) or O(1) amortized."
    elif subsub_id == 460 or "LIS" in subsub:
        return "Compute the Longest Increasing Subsequence using patience sorting with binary search (std::lower_bound) in O(N log N) time."
    elif subsub_id == 459 or "Probability" in subsub:
        return "Formulate expectation as E[X] = ∑ P(e) * v(e). Formulate linear transition equations on states and solve via DAG DP or Gaussian elimination."
    elif "Segment Tree" in subsub and "Lazy" in subsub:
        return "Maintain pending range modifications with lazy tags on tree nodes. Push down updates on traversal to achieve O(log N) per range update and range query."
    elif "Segment Tree" in subsub:
        return "Build a Segment Tree over the array. Implement point update and associative range query operations in O(log N) time per query."
    elif "BIT" in subsub or "Fenwick" in subsub:
        return "Maintain prefix sums and dynamic point updates via Fenwick tree using lowbit operations (i & -i) in O(log N) time and O(N) space."
    elif subsub_id == 80 or "DSU" in subsub or "Union Find" in subsub:
        return "Maintain disjoint sets using path compression and union by rank/size. Process edge additions and component queries in O(α(N)) amortized time."
    elif subsub_id == 81 or "DSU with Rollbacks" in subsub:
        return "Omit path compression and use union by size with an operation history stack. Roll back edge additions during offline divide and conquer in O(log N) per step."
    elif subsub_id == 86 or "DSU on Tree" in subsub:
        return "Process tree queries offline. Preserve the heavy child's data structure while clearing light children, achieving O(N log N) total merging cost."
    elif subsub_id == 101 or "Centroid Decomposition" in subsub:
        return "Divide the tree recursively at its centroid into subtrees of size at most N/2. Count paths passing through the centroid in O(N log N) total time."
    elif subsub_id == 100 or "Heavy Light Decomposition" in subsub or "HLD" in subsub:
        return "Decompose the tree into heavy chains and light edges. Flatten chains into segment tree intervals to query paths and subtrees in O(log^2 N) time."
    elif subsub_id == 146 or "LCA" in subsub or "Binary Lifting" in subsub:
        return "Precompute 2^k ancestor jumps up[u][k] and node depths in O(N log N). Compute LCA and path aggregates in O(log N) per query."
    elif subsub_id == 168 or "Dijkstra" in subsub:
        return "Formulate the state transition graph with non-negative weights. Execute Dijkstra's algorithm with priority queue to find shortest paths in O((V + E) log V)."
    elif subsub_id == 174 or "0/1 BFS" in subsub:
        return "Traverse state transitions with edge weights 0 and 1 using std::deque. Push 0-weight edges to front and 1-weight edges to back in O(V + E) time."
    elif subsub_id == 170 or "Floyd Warshall" in subsub:
        return "Compute all-pairs shortest paths or reachability using triple loop dynamic programming d[i][j] = min(d[i][j], d[i][k] + d[k][j]) in O(V^3) time."
    elif subsub_id == 215 or "Maximum Flow" in subsub:
        return "Construct a residual flow network with source S and sink T. Apply Dinic's blocking flow algorithm with level graphs and scaling in O(V^2 E) time."
    elif subsub_id == 216 or "MCMF" in subsub or "Min Cost Max Flow" in subsub:
        return "Model constraint matching as minimum-cost flow. Augment along the shortest augmenting path using SPFA or Dijkstra with Johnson's potentials."
    elif subsub_id == 142 or "Topological Sorting" in subsub:
        return "Compute in-degrees of all DAG vertices. Process vertices with in-degree 0 using a queue to establish a valid linear ordering in O(V + E) time."
    elif subsub_id == 148 or "SCC" in subsub or "Strongly Connected" in subsub:
        return "Identify maximal strongly connected components using Tarjan's or Kosaraju's algorithm in O(V + E). Condense into a DAG for subsequent DP processing."
    elif subsub_id == 150 or "Bridge" in subsub:
        return "Perform DFS and compute tin[u] and low[u] entry times. Edges with low[v] > tin[u] form critical bridges; condense 2-edge connected components into a bridge tree."
    elif subsub_id == 191 or "2 SAT" in subsub:
        return "Convert boolean constraints to implication edges (¬A => B, ¬B => A). Compute SCCs using Tarjan's; a valid assignment exists iff no variable shares an SCC with its negation."
    elif subsub_id == 472 or "Grundy" in subsub or "Nim" in subsub:
        return "Compute Sprague-Grundy values g(u) = mex({g(v) : u -> v}). Game state is winning iff XOR sum of independent game components is non-zero."
    elif subsub_id == 476 or "Games on Arbitrary Graphs" in subsub:
        return "Determine winning and losing positions using backward induction / retrograde analysis. Propagate definitive states through the inverse edge graph in O(V + E)."
    elif subsub_id == 303 or "Catalan" in subsub:
        return "Model valid non-crossing partition, balanced bracket, or Dyck path configurations. Compute C_n = (1/(n+1)) * binom(2n, n) modulo P in O(N) preprocessing."
    elif subsub_id == 305 or "Inclusion" in subsub or "PIE" in subsub:
        return "Count elements with specified properties using Principle of Inclusion-Exclusion: |⋃ A_i| = ∑ |A_i| - ∑ |A_i ∩ A_j| + ... iterating over sign (-1)^|S| in O(2^K)."
    elif subsub_id == 310 or "Binomial" in subsub or "Factorials" in subsub:
        return "Precompute factorials and inverse factorials up to N using Fermat's Little Theorem (mod 10^9+7 or 998244353). Answer nCr queries in O(1) time per query."
    elif subsub_id == 242 or "Sieve" in subsub:
        return "Precompute linear sieve to store minimum prime factor (spf[x]) up to N in O(N). Factorize any number x ≤ N in O(log x) steps."
    elif subsub_id == 266 or "Modular Arithmetic" in subsub:
        return "Apply modular properties, binary exponentiation (a^b mod P in O(log b)), and modular multiplicative inverse using Extended Euclidean Algorithm."
    elif subsub_id == 326 or subsub_id == 327 or "FFT" in subsub or "NTT" in subsub:
        return "Transform coefficient polynomials to point-value form via FFT/NTT in O(N log N). Multiply point values in O(N) and invert back to achieve fast polynomial convolution."
    elif subsub_id == 355 or "Matrix Exponentiation" in subsub:
        return "Formulate linear recurrence as state transition vector V_{n+1} = M * V_n. Compute M^K via binary matrix exponentiation in O(D^3 log K) time."
    elif subsub_id == 382 or "XOR Basis" in subsub:
        return "Insert bitwise values into a linear basis of size 60. Check reachability, maximize XOR sum, or count distinct subset XOR values in O(bits) per insertion."
    elif subsub_id == 406 or "KMP" in subsub:
        return "Precompute the prefix function π[i] matching longest proper prefix-suffix in O(M). Traverse text string with π transitions to locate all occurrences in O(N) time."
    elif subsub_id == 407 or "Z Algorithm" in subsub:
        return "Compute Z-array where Z[i] is the length of longest common prefix between S and S[i..] in linear O(N) time using two-pointer interval jumps."
    elif subsub_id == 410 or "String Hashing" in subsub:
        return "Compute polynomial rolling hashes hash(s[0..i]) with prime base B and large modulo M. Check substring equality s[l1..r1] == s[l2..r2] in O(1) time."
    elif subsub_id == 419 or "Suffix Automaton" in subsub:
        return "Construct the minimal deterministic finite automaton recognizing all substrings of S online in O(N) time and space. Answer substring count, occurrence, and LCS queries."
    elif subsub_id == 416 or "Suffix Array" in subsub:
        return "Sort all suffixes lexicographically with LCP array in O(N log N) using prefix doubling. Answer pattern matching and distinct substring queries in O(log N)."
    elif subsub_id == 414 or "Aho Corasick" in subsub:
        return "Build a trie of dictionary patterns and construct BFS suffix/failure links with output links. Match all dictionary occurrences simultaneously in text in O(Text + Matches)."
    elif subsub_id == 491 or "Convex Hull" in subsub:
        return "Compute minimal convex polygon enclosing the point set using Graham Scan or Monotone Chain (Andrew's algorithm) sorted by coordinates in O(N log N)."
    elif subsub_id == 521 or "Sweep Line" in subsub:
        return "Sort event points along the X-axis. Process events sequentially while maintaining active segments in a balanced BST (std::set) in O(N log N) total time."
    elif subsub_id == 33 or "Binary Search" in subsub:
        return "Verify predicate monotonicity: P(x) is true for x ≤ K and false otherwise. Binary search over the answer domain to find the boundary in O(log(Range) × Verify_Time)."
    elif subsub_id == 34 or "Two Pointers" in subsub:
        return "Exploit monotonicity of two-pointer invariant [L, R]. Advance R while shifting L forward to maintain validity, running in O(N) amortized time."
    elif subsub_id == 554 or "Meet in the Middle" in subsub:
        return "Split N-element search space into two halves of size N/2. Compute states for each half in O(2^(N/2)) and combine via sorting / two pointers / hash map."
    elif subsub_id == 542 or "Interactive" in subsub:
        return "Design an adaptive query strategy maintaining uncertainty bounds. Halve candidate space or probe tree centroids using at most the allowed query budget."
    elif subsub_id == 44 or "Greedy" in subsub:
        return "Identify exchange argument or greedy choice property. Sort elements by payoff ratio or deadline and greedily pick candidates to achieve global optimum."
    elif subsub_id == 45 or "Constructive" in subsub:
        return "Uncover mathematical invariant or parity constraint. Construct the solution step-by-step maintaining the validity condition without exhaustive search."
    else:
        return f"Apply {subsub} paradigm under the {main_topic} framework. Exploit problem invariants to reduce state space and achieve optimal complexity."

