"""Canonical Competitive Programming Taxonomy (11 Main Topics, Subtopics, 576 Subsubtopics)."""

TAXONOMY = {
    "Basics": {
        "Intro to Programming": [
            (1, "What is Programming?", ["first program", "hello world", "syntax basics"])
        ],
        "Learn a Language": [
            (2, "Intro to C++ and Setting up the Environment", ["setting up c++", "cpp environment"]),
            (3, "Data Types, Variables and Input Output", ["primitive types", "integer overflow check", "type casting"]),
            (4, "Operators", ["bitwise operators basics", "relational operators"]),
            (5, "Conditional Statements", ["branching", "if-else switch"]),
            (6, "Loops", ["nested loops", "while loop termination"]),
            (7, "Functions", ["function recursion header", "pass by reference"]),
            (8, "Arrays", ["1d array simulation", "array indexing"]),
            (9, "Strings", ["string manipulation basics", "character frequency count"]),
            (10, "Pointers and References", ["memory pointers", "pointer arithmetic"]),
            (11, "Structures", ["c++ struct definition", "custom data record"])
        ],
        "Intro to Competitive Programming": [
            (12, "What is Competitive Programming?", ["online judge intro", "time limit exceeded intro"])
        ],
        "Bitwise Thinking": [
            (13, "Bitwise Operations and Bitmasks", ["bitwise operations", "bitmasking", "submask"])
        ],
        "Complexity Analysis": [
            (14, "Big O Notation and Time and Space Complexity Analysis", ["complexity", "big o"]),
            (15, "Fast Input Output", ["fast io", "cin.tie"])
        ],
        "Recursion": [
            (16, "Recursion", ["recursion", "recursive function", "call stack"])
        ],
        "Very Basic Math": [
            (17, "Divisors", ["divisors", "factors", "divisibility"]),
            (18, "GCD and LCM", ["gcd", "lcm", "greatest common divisor"]),
            (19, "Harmonic Number", ["harmonic series", "n/1 + n/2"])
        ],
        "Range Queries Without Updates": [
            (20, "Prefix Sum", ["prefix sum", "cumulative sum", "range sum"]),
            (21, "Prefix XOR", ["prefix xor", "xor sum"])
        ],
        "Standard Template Library (STL)": [
            (22, "Intro to STL, Containers and Iterators", ["stl container", "iterators traversal"]),
            (23, "Pairs and Tuples", ["std::pair", "std::tuple", "pair indexing"]),
            (24, "Vector", ["vector", "dynamic array"]),
            (25, "Stack", ["stack", "lifo"]),
            (26, "Queue", ["queue", "fifo"]),
            (27, "Priority Queue / Heap", ["priority queue", "heap", "min-heap", "max-heap"]),
            (28, "Deque", ["deque", "double-ended queue"]),
            (29, "Set, Unordered Set and Multiset", ["set", "multiset", "unordered_set", "balanced bst"]),
            (30, "Map and Unordered Map", ["map", "unordered_map", "hash table"]),
            (31, "Bitset", ["bitset", "std::bitset"]),
            (32, "List / Linked List", ["linked list", "std::list"])
        ],
        "Leveraging Monotonicity": [
            (33, "Binary Search", ["binary search", "binary search on answer", "bsearch", "bisection"]),
            (34, "Two Pointers", ["two pointers", "2 pointers", "caterpillar", "left right pointer"])
        ],
        "Basic Sorting Algorithms": [
            (35, "Bubble Sort", ["bubble sort"]),
            (36, "Selection Sort", ["selection sort"]),
            (37, "Insertion Sort", ["insertion sort"]),
            (38, "Counting Sort", ["counting sort", "frequency array"]),
            (39, "Merge Sort", ["merge sort"]),
            (40, "Quick Sort", ["quick sort", "pivot"]),
            (41, "Radix Sort", ["radix sort"]),
            (42, "C++ STL Sort and Custom Comparator", ["sort", "comparator", "sortings", "stable_sort"])
        ],
        "Divide and Conquer": [
            (43, "Divide and Conquer", ["divide and conquer", "d&c"])
        ],
        "Greedy and Constructive": [
            (44, "Basic Greedy Algorithms", ["greedy", "local optimum"]),
            (45, "Basic Constructive Algorithms", ["constructive algorithms", "construction"])
        ],
        "2D Prefix Sum": [
            (46, "2D Prefix Sum", ["2d prefix sum", "matrix prefix sum", "submatrix sum"])
        ],
        "More Techniques": [
            (47, "Difference Array", ["difference array", "range add"]),
            (48, "Sliding Window Technique", ["sliding window", "fixed window", "variable window"])
        ],
        "Bit Manipulation": [
            (49, "Bit Manipulation", ["bit manipulation", "popcount", "bitmask"]),
            (50, "The XOR Trick", ["xor trick", "xor sum", "a xor b", "xor cancel"])
        ],
        "Basic Modular Arithmetic": [
            (51, "Binary Exponentiation and Basic Modular Arithmetic", ["binary exponentiation", "power mod", "modular arithmetic"]),
            (52, "Fermat's Little Theorem and Modular Inverse", ["fermat's little theorem", "modular inverse", "inv mod"])
        ],
        "Basic Counting": [
            (53, "Permutations, Combinations and Basic Counting Problems", ["ncr", "permutation", "combination", "basic counting"]),
            (54, "Stars and Bars", ["stars and bars", "balls and bins"]),
            (55, "Pigeonhole Principle", ["pigeonhole principle", "pigeonhole"])
        ],
        "Very Basic Graphs": [
            (56, "Introduction to Graphs | Definitions and Representations", ["graph representation", "adjacency list", "adjacency matrix"])
        ]
    },
    "Data Structures (DS)": {
        "Segment Tree": [
            (57, "Segment Tree (Point Update Range Query)", ["segment tree", "point update", "range query", "segtree"]),
            (58, "Segment Tree with Lazy Propagation", ["lazy propagation", "range update range query", "lazy segtree"]),
            (59, "Persistent Segment Tree", ["persistent segment tree", "persistent segtree", "k-th number in range", "versioned tree"]),
            (60, "Persistent Segment Tree with Lazy Propagation", ["persistent lazy", "persistent range update"]),
            (61, "2D Segment Tree", ["2d segment tree", "segment tree of segment trees"]),
            (62, "Dynamic Segment Tree", ["dynamic segment tree", "sparse segment tree", "implicit segment tree"]),
            (63, "2D Dynamic Segment Tree", ["2d dynamic segment tree"]),
            (64, "Merge Sort Tree", ["merge sort tree", "fractional cascading in segtree"]),
            (65, "Iterative Segment Tree", ["iterative segment tree", "zkw segment tree"]),
            (66, "Segment Tree Merging", ["segment tree merging", "segtree merge", "tree query merge"]),
            (67, "Segment Tree Beats", ["segment tree beats", "ji ruida segtree", "chmin chmax segtree"]),
            (68, "XOR Segment Tree", ["xor segment tree", "bitwise segtree"]),
            (69, "Historic Information on Segment Trees", ["historic sum", "historic min", "historical info segtree"])
        ],
        "Binary Indexed Tree (BIT)": [
            (70, "BIT / Fenwick Tree", ["fenwick tree", "bit", "binary indexed tree"]),
            (71, "Lower bound on BIT", ["lower bound on bit", "binary lifting on bit"]),
            (72, "BIT with Range Update and Range Query", ["range update range query bit", "difference bit"]),
            (73, "2D BIT", ["2d bit", "2d fenwick"]),
            (74, "2D BIT with Range Update and Range Query", ["2d bit range update"])
        ],
        "Sparse Table": [
            (75, "Sparse Table", ["sparse table", "rmq", "range minimum query"]),
            (76, "Sparse Table 2D", ["2d sparse table"]),
            (77, "Disjoint Sparse Table", ["disjoint sparse table", "static rmq o(1)"])
        ],
        "Trie": [
            (78, "Trie on Strings and Bits", ["trie", "prefix tree", "xor trie", "binary trie", "maximum xor pair"]),
            (79, "Persistent Trie", ["persistent trie", "persistent xor trie"])
        ],
        "Disjoint Set Union (DSU)": [
            (80, "DSU / Union Find", ["dsu", "union find", "disjoint set union"]),
            (81, "DSU with Rollbacks", ["dsu with rollback", "rollback dsu", "undo dsu"]),
            (82, "Reachability Tree / DSU Tree / Kruskal Reconstruction Tree (KRT)", ["kruskal reconstruction tree", "dsu tree", "reachability tree", "krt"]),
            (83, "Partially Persistent DSU", ["partially persistent dsu"]),
            (84, "Persistent DSU", ["persistent dsu"]),
            (85, "Augmented DSU / Weighted DSU", ["weighted dsu", "potential dsu", "colored dsu"]),
            (86, "DSU on Tree and Small to Large Merging", ["dsu on tree", "small to large", "sack", "merge smaller into larger"]),
            (87, "[Trick] Maintaining Log N DSU / Range Parallel DSU", ["range parallel dsu", "log n dsu"])
        ],
        "Square Root Decomposition": [
            (88, "Basic SQRT Decomposition", ["sqrt decomposition", "block decomposition", "sqrt"]),
            (89, "Splitting Objects into Light and Heavy / Case Processing", ["light heavy", "heavy light vertices", "degree sqrt n"]),
            (90, "Batch Processing / SQRT Decomposition on Queries", ["batch processing", "sqrt queries"]),
            (91, "SQRT Decomposition Split and Build Technique", ["split and build", "block rebuild"]),
            (92, "SQRT Fragmented Tree / Block Tree / SQRT Decomposition on Trees", ["tree sqrt decomposition", "tree block"]),
            (93, "Mo's Algorithm", ["mo's algorithm", "mo algorithm", "offline query mo"]),
            (94, "Rollback Mo and Mo's with DSU", ["rollback mo", "mo with dsu"]),
            (95, "Mo's on Tree", ["mo on tree", "euler tour mo"]),
            (96, "Sweepline Mo", ["sweepline mo"]),
            (97, "Mo's with Update / 3D Mo (Offline)", ["3d mo", "mo with updates"]),
            (98, "Mo's with Update / 3D Mo (Online)", ["online mo"]),
            (99, "4D Mo", ["4d mo"])
        ],
        "Heavy Light Decomposition (HLD)": [
            (100, "Heavy Light Decomposition (HLD) ft Subtrees and Path Query", ["hld", "heavy light decomposition", "path query on tree"])
        ],
        "Centroid Decomposition": [
            (101, "Centroid Decomposition", ["centroid decomposition", "tree centroid"]),
            (102, "Persistent Centroid Decomposition", ["persistent centroid decomposition"])
        ],
        "Long Path Decomposition": [
            (103, "Long Path Decomposition", ["long path decomposition", "tree long path"])
        ],
        "BST": [
            (104, "Binary Search Tree (BST)", ["bst", "binary search tree"])
        ],
        "Balanced Binary Search Tree (BBST)": [
            (105, "Treap", ["treap", "cartesian tree bst"]),
            (106, "Implicit Treap", ["implicit treap", "array split merge"]),
            (107, "Persistent Treap", ["persistent treap"]),
            (108, "Rope", ["rope", "c++ rope"]),
            (109, "Splay Tree", ["splay tree"])
        ],
        "Link Cut Tree (LCT)": [
            (110, "Link Cut Tree (LCT)", ["link cut tree", "lct", "dynamic tree"]),
            (111, "Euler Tour Tree (ETT)", ["euler tour tree", "ett"]),
            (112, "Top Tree / AAA Tree", ["top tree", "aaa tree"]),
            (113, "Link Cut Cactus", ["link cut cactus"])
        ],
        "Policy Based Data Structures": [
            (114, "Ordered Set", ["ordered set", "tree_order_statistics_node_update", "pbds"]),
            (115, "GP Hash Table", ["gp_hash_table", "cc_hash_table", "pbds hash"])
        ],
        "More Tree Data Structures": [
            (116, "Wavelet Tree", ["wavelet tree"]),
            (117, "Cartesian Tree", ["cartesian tree"]),
            (118, "K-Dimensional Tree (KD Tree)", ["kd tree", "k-d tree"]),
            (119, "SQRT Tree", ["sqrt tree"]),
            (120, "Permutation Tree", ["permutation tree"]),
            (121, "PQ Tree", ["pq tree"])
        ],
        "Dynamic Connectivity": [
            (122, "Dynamic Connectivity Problem (Offline)", ["dynamic connectivity offline", "cdq dsu rollback"]),
            (123, "Dynamic Connectivity Problem (Online) / HDLT Algorithm", ["hdlt", "online dynamic connectivity"])
        ],
        "Monotonic Data Structures": [
            (124, "Monotonic Stack: All Nearest Smaller Values and All Subarray Maximum/Minimum", ["monotonic stack", "nearest smaller", "histogram max area"]),
            (125, "Monotonic Queue", ["monotonic queue", "sliding window minimum"]),
            (126, "Monotonic Queue 2D", ["2d monotonic queue"]),
            (127, "Monotonic Deque", ["monotonic deque"])
        ],
        "Miscellaneous": [
            (128, "Interval Set", ["interval set", "std::set intervals", "chtholly tree", "odtree"]),
            (129, "Persistent Array", ["persistent array"]),
            (130, "Persistent Queue", ["persistent queue"]),
            (131, "Persistent Meldable Heap / Leftist Heap", ["leftist heap", "meldable heap", "skew heap"])
        ],
        "Techniques": [
            (132, "Venice Technique", ["venice technique", "offset tracking"]),
            (133, "Offline Queries", ["offline queries", "sorting queries", "offline"]),
            (134, "Static to Dynamic Trick / Log Decomposition", ["static to dynamic", "logarithmic method"]),
            (135, "Divide and Conquer on Queries", ["divide and conquer on queries"]),
            (136, "CDQ Divide and Conquer", ["cdq divide and conquer", "cdq"]),
            (137, "Queue Undo Trick", ["queue undo"]),
            (138, "Priority Queue Undo Trick", ["priority queue undo"])
        ]
    },
    "Graph Theory": {
        "Graph Traversal": [
            (139, "Depth First Search (DFS)", ["dfs", "depth first search"]),
            (140, "Breadth First Search (BFS)", ["bfs", "breadth first search"]),
            (141, "DFS Tree", ["dfs tree", "back edges", "tree edge"]),
            (142, "Topological Sorting", ["topological sort", "toposort", "kahn's algorithm"]),
            (143, "Tree Diameter", ["tree diameter", "two dfs tree diameter"]),
            (144, "Euler Tour Technique", ["euler tour technique", "ett flattening"]),
            (145, "Inverse Graph", ["inverse graph", "complement graph bfs"])
        ],
        "Lowest Common Ancestor (LCA)": [
            (146, "Binary Lifting and LCA", ["binary lifting", "lca", "lowest common ancestor"]),
            (147, "LCA in O(1)", ["o(1) lca", "tarjan lca", "rmq lca"])
        ],
        "Graph Connectivity": [
            (148, "Strongly Connected Components (SCC)", ["scc", "tarjan scc", "kosaraju", "strongly connected components"]),
            (149, "Incremental SCC", ["incremental scc"]),
            (150, "Articulation Bridges and Bridge Tree", ["bridge", "bridges", "bridge block tree", "2-edge-connected"]),
            (151, "Online Articulation Bridges", ["online bridges"]),
            (152, "Articulation Points and Block Cut Tree", ["articulation point", "cut vertex", "block cut tree", "bct", "biconnected"]),
            (153, "Three Edge Connectivity", ["3-edge connected"]),
            (154, "Four Edge Connectivity", ["4-edge connected"]),
            (155, "Dynamic K-Connectivity", ["k-connectivity"]),
            (156, "Ear Decomposition", ["ear decomposition"])
        ],
        "Orientation": [
            (157, "Strong Orientation", ["strong orientation", "robbins theorem"]),
            (158, "ST-numbering / Bipolar Orientation", ["st-numbering", "bipolar orientation"])
        ],
        "Minimum Spanning Tree (MST)": [
            (159, "Minimum Spanning Tree (MST) - Prim's and Kruskal's", ["mst", "kruskal", "prim", "minimum spanning tree"]),
            (160, "Steiner Tree Problem", ["steiner tree"]),
            (161, "Boruvka's Algorithm", ["boruvka", "parallel mst"]),
            (162, "Minimum Diameter Spanning Tree", ["minimum diameter spanning tree"]),
            (163, "Manhattan MST", ["manhattan mst"]),
            (164, "Euclidean MST", ["euclidean mst", "delaunay mst"]),
            (165, "Directed MST", ["edmonds' algorithm", "directed mst", "dmst"]),
            (166, "Dynamic MST", ["dynamic mst"]),
            (167, "Kirchoffs Theorem ft Number of MSTs", ["kirchhoff's matrix tree theorem", "number of spanning trees"])
        ],
        "Shortest Paths": [
            (168, "Dijkstra's Algorithm", ["dijkstra", "shortest path"]),
            (169, "[Trick] Dijkstra on Segment Tree", ["dijkstra on segment tree", "segtree dijkstra", "virtual nodes range edge"]),
            (170, "Floyd Warshall", ["floyd warshall", "all pairs shortest path"]),
            (171, "Bellman Ford", ["bellman ford", "negative cycle detection"]),
            (172, "Shortest Path Faster Algorithm (SPFA)", ["spfa"]),
            (173, "Johnson's Alogrithm", ["johnson's algorithm", "reweighting"]),
            (174, "0/1 BFS", ["0/1 bfs", "0-1 bfs"]),
            (175, "Dial's algorithm", ["dial's algorithm"]),
            (176, "Eppsteins Algorithm", ["k shortest paths", "eppstein"]),
            (177, "Suurballe's Algorithm", ["suurballe", "disjoint shortest paths"]),
            (178, "A* Algorithm", ["a* search", "heuristic search"])
        ],
        "Cycles": [
            (179, "Cycle Detection", ["cycle detection", "has cycle"]),
            (180, "[Problem] Minimum Weight Cycle For Each Vertex", ["min cycle per vertex"]),
            (181, "[Problem] Minimum Weight Cycle For Each Edge", ["min cycle per edge"]),
            (182, "Minimum Mean Weight Cycle", ["karp's minimum mean weight cycle"]),
            (183, "Number of 3 and 4 length Cycles", ["triangles count", "4-cycles count"])
        ],
        "More Tree Stuff": [
            (184, "Virtual Tree / Auxiliary Tree", ["virtual tree", "auxiliary tree"]),
            (185, "Rerooting Technique", ["rerooting", "tree rerooting", "all root tree dp"]),
            (186, "Union of Two Paths on a Tree", ["union of tree paths"]),
            (187, "Intersection of Two Paths on a Tree", ["intersection of tree paths"]),
            (188, "[Problem] Number of Paths of Each Length in a Tree", ["tree path length count"]),
            (189, "Dynamic Online Tree Diameter", ["dynamic tree diameter"]),
            (190, "[Problem] Tree Orientation to Maximize Pairs of Reachable Nodes", ["tree orientation"])
        ],
        "Satisfiability": [
            (191, "2 SAT", ["2-sat", "two satisfiability", "implication graph"]),
            (192, "3 SAT", ["3-sat"]),
            (193, "System Of Difference Constraints", ["difference constraints", "shortest path constraint"])
        ],
        "Eulerian Path": [
            (194, "Eulerian Path and Cycle", ["eulerian path", "eulerian circuit", "hierholzer"])
        ],
        "Hamiltonian Path": [
            (195, "Hamiltonian Path and Cycle", ["hamiltonian path", "hamiltonian cycle"]),
            (196, "Hamiltonian Path Heuristic Algorithm", ["hamiltonian heuristic"])
        ],
        "Cliques and Independent Sets": [
            (197, "Maximum Clique", ["maximum clique", "bron-kerbosch"]),
            (198, "Maximum Independent Set (MIS)", ["maximum independent set", "mis"])
        ],
        "Graph Coloring": [
            (199, "Chromatic Number", ["chromatic number"]),
            (200, "Welsh-Powell Algorithm", ["welsh-powell"]),
            (201, "Chromatic Polynomial ft Number of DAGs", ["chromatic polynomial"]),
            (202, "Edge Coloring of Simple Graph", ["edge coloring", "vizing's theorem"]),
            (203, "Edge Coloring of Bipartite Graph", ["bipartite edge coloring"])
        ],
        "Graph Counting": [
            (204, "Counting Labeled Graphs", ["counting labeled graphs"]),
            (205, "Prufer Code", ["prufer code", "cayley's formula"]),
            (206, "[Problem] Number of Arborescences with n Nodes", ["arborescences count"]),
            (207, "Tuttes Theorem ft Arborescences in a Graph", ["tutte's theorem"]),
            (208, "BEST Theorem", ["best theorem", "eulerian tours count"])
        ],
        "Dynamic Acyclic Graphs (DAG)": [
            (209, "DAG Reachability", ["dag reachability", "bitset reachability"]),
            (210, "Incremental DAG Reachability", ["incremental reachability"])
        ],
        "Dominators": [
            (211, "Dominator Tree", ["dominator tree", "lengauer-tarjan"])
        ],
        "Special Graphs": [
            (212, "Cactus Graph", ["cactus graph"]),
            (213, "Tournament Graph", ["tournament graph", "landau's theorem"]),
            (214, "Chordal Graph", ["chordal graph", "perfect elimination ordering"])
        ],
        "Flow and Min Cut": [
            (215, "Maximum Flow / Minimum Cut", ["max flow", "dinic", "edmonds-karp", "push-relabel", "min cut"]),
            (216, "Min Cost Max Flow (MCMF)", ["min cost max flow", "mcmf", "successive shortest path"]),
            (217, "Min Cost Max Flow with Negative Cycles", ["negative cycle mcmf"]),
            (218, "Maximum Closure Problem", ["maximum closure", "project selection"]),
            (219, "L-R Flow", ["circulation with demands", "lr flow", "lower bound flow"]),
            (220, "Gomory-Hu Tree", ["gomory-hu tree", "all pairs min cut"]),
            (221, "Gomory-Hu Tree of a Planar Graph", ["planar gomory-hu"]),
            (222, "Stoer Wagner Algorithm", ["stoer wagner", "global min cut"]),
            (223, "Chinese Postman Problem", ["chinese postman problem"]),
            (224, "Uniqueness of Min Cut", ["uniqueness of min cut"]),
            (225, "Maximum Density Subgraph", ["maximum density subgraph"]),
            (226, "Min Cut in a Planar Graph", ["planar min cut", "dual graph shortest path"]),
            (227, "Max Cut in a Planar Graph", ["planar max cut"])
        ],
        "Matching": [
            (228, "Bipartite Matching (HopCroft Karp Algorithm and Kuhn's Algorithm)", ["bipartite matching", "hopcroft-karp", "kuhn"]),
            (229, "Hungarian Algorithm / Bipartite Weighted Matching", ["hungarian algorithm", "weighted bipartite matching"]),
            (230, "Blossom Algorithm Unweighted / General Matching / Randomized General Matching", ["blossom algorithm", "general matching", "edmonds blossom"]),
            (231, "Blossom Algorithm Weighted / General Weighted Matching", ["weighted blossom", "general weighted matching"]),
            (232, "Stable Marriage Problem", ["gale-shapley", "stable marriage"]),
            (233, "Konig's Theorem and Maximum Independent Set in Bipartite Graphs", ["konig's theorem", "bipartite vertex cover"]),
            (234, "Halls Theorem", ["hall's marriage theorem", "hall's condition"]),
            (235, "Matching using Determinants", ["tutte matrix", "randomized matching"])
        ],
        "Partially Ordered Set (POSET)": [
            (236, "POSET ft Dilworth's and Mirsky's Theorem", ["dilworth", "poset", "chain antichain", "mirsky"])
        ],
        "Miscellaneous": [
            (237, "Functional Graphs", ["functional graph", "successor graph", "rho algorithm cycle"]),
            (238, "Degree Sequences, Erdos-Gallai Theorem, Gale-Ryser Theorem and Havel–Hakimi Algorithm", ["havel-hakimi", "erdos-gallai"]),
            (239, "Tree Isomorphism", ["tree isomorphism", "tree hash", "ahutree isomorphism"]),
            (240, "Binarizing a Tree", ["binarizing tree"]),
            (241, "Planarity Check", ["planarity", "planar graph"])
        ]
    },
    "Number Theory": {
        "Primes and Divisors": [
            (242, "Sieve, Prime Factorization and Divisors", ["sieve of eratosthenes", "prime factorization", "primes"]),
            (243, "Linear Sieve", ["linear sieve", "euler sieve"]),
            (244, "Segmented Sieve", ["segmented sieve"]),
            (245, "Sieve upto 1e9", ["sieve 1e9"]),
            (246, "Miller-Rabin Primality Test", ["miller rabin", "primality test"]),
            (247, "Pollard Rho", ["pollard rho", "factorization"]),
            (248, "Prime Counting Function", ["meissel-lehmer", "prime count"]),
            (249, "Prime Gap", ["prime gap"]),
            (250, "[Problem] Counting Numbers Having Exactly K Divisors", ["k divisors count"]),
            (251, "[Problem] Smallest Number Having Exactly K Divisors", ["smallest with k divisors"]),
            (252, "Sum of The Number of Divisors in cbrt(n)", ["cbrt n divisors"]),
            (253, "Wilson's Theorem", ["wilson's theorem"]),
            (254, "Implicit Prime Factorization", ["implicit prime factorization"])
        ],
        "Multiplicative Functions": [
            (255, "Number of Divisors / Sum of Divisors / Sigma Function", ["sigma function", "divisor sum", "number of divisors"]),
            (256, "Euler's Totient Function / Phi Function", ["euler totient", "phi function"]),
            (257, "Power Tower / Generalized Euler theorem", ["power tower", "euler's totient theorem"]),
            (258, "Mobius Function and Mobius Inversion", ["mobius inversion", "mobius function", "mu(n)"]),
            (259, "Dirichlet convolution", ["dirichlet convolution", "sub-linear prefix sum"]),
            (260, "Min_25 Sieve", ["min_25 sieve", "min25"]),
            (261, "Powerful Number Sieve / PN Sieve", ["powerful number sieve"])
        ],
        "Euclidean Algorithm": [
            (262, "Euclidean Algorithm", ["euclidean algorithm", "gcd"]),
            (263, "Extended Euclid", ["extended euclidean algorithm", "extgcd"]),
            (264, "Bezout's Identity", ["bezout's identity"]),
            (265, "Chicken McNugget Theorem", ["frobenius coin problem", "chicken mcnugget"])
        ],
        "Modular Arithmetic": [
            (266, "Linear Congruence Equation", ["linear congruence"]),
            (267, "Chinese Remainder Theorem (CRT)", ["chinese remainder theorem", "crt", "garner's algorithm"]),
            (268, "Primitive Root", ["primitive root"]),
            (269, "Multiplicative Order and Carmichael's Lambda Function", ["multiplicative order", "carmichael lambda"]),
            (270, "Discrete Log / Baby Step Giant Step", ["baby step giant step", "bsgs", "discrete log"]),
            (271, "Discrete Root", ["discrete root"]),
            (272, "Discrete Root in O(P^(1/4))", ["fast discrete root"]),
            (273, "Discrete Square Root, Tonelli Shanks Algorithm, Cipolla's Algorithm", ["tonelli-shanks", "cipolla", "modular square root", "quadratic residue"]),
            (274, "Number of Distinct Kth Powers Modulo N", ["kth powers modulo n"]),
            (275, "Number of Solutions to X^2 = 1 mod M", ["square root of 1 mod m"])
        ],
        "Linear Diophantine Equations": [
            (276, "Linear Diophantine Equation with Two Variables", ["linear diophantine", "ax + by = c"]),
            (277, "Linear Diophantine Equation with N Variables", ["n variables diophantine"]),
            (278, "Trivariable Linear Diophantine Equation with Nonnegative Solutions", ["3-variable diophantine"]),
            (279, "Multivariable Linear Diophantine Equation with Nonnegative Solutions", ["multivariable diophantine"]),
            (280, "Linear Diophantine With N Unknowns and Two Equations", ["two diophantine equations"])
        ],
        "Solutions to Equations": [
            (281, "Number of Solutions to a Basic Linear Algebraic Equation", ["linear equations solutions count"]),
            (282, "Number of Solutions to a Basic Linear Algebraic Equation using Meet in the Middle", ["mitm equations"]),
            (283, "Number of Nonnegative Integer Solutions to ax + by ≤ c", ["lattice triangle points"]),
            (284, "Number of Integer Solutions to 1/x + 1/y = 1/k", ["1/x + 1/y = 1/k"]),
            (285, "Two / Three / Four Squares Theorem", ["lagrange four-square", "two squares theorem"]),
            (286, "Pell's Equation", ["pell's equation"])
        ],
        "Floor Sum": [
            (287, "Sum of Floors", ["sum of floors", "hyperbola method"]),
            (288, "Floor Sum and Mod Sum of Arithmetic Progression", ["floor sum", "atcoder floor_sum"]),
            (289, "Generalized Floor Sum of Arithmetic Progression", ["generalized floor sum"])
        ],
        "Fibonacci Numbers": [
            (290, "Fibonacci Numbers", ["fibonacci numbers", "zeckendorf"]),
            (291, "[Problem] LCM of Fibonacci Numbers", ["fibonacci lcm"]),
            (292, "Pisano Period", ["pisano period"]),
            (293, "Phi Field", ["golden ratio mod p"])
        ],
        "Miscellaneous": [
            (294, "Pythagorean Triplets", ["pythagorean triples", "pythagorean triplets"]),
            (295, "[Problem] Min of Mod of Arithmetic Progression", ["min of mod ap"]),
            (296, "Sqrt Decomposition of Mod of Arithmetic Progression", ["sqrt mod ap"]),
            (297, "Factorial Number System", ["lehmer code", "factoradic"]),
            (298, "Stern-Brocot Tree and Rational Approximation", ["stern-brocot tree", "farey sequence"]),
            (299, "[Problem] Number of a * x mod p in a Range", ["a*x mod p in range"]),
            (300, "[Problem] Smallest Nonnegative Integer x s.t. l ≤ a * x mod p ≤ r", ["smallest x in interval mod p"])
        ]
    },
    "Combinatorics": {
        "Techniques": [
            (301, "Contribution Technique", ["contribution to sum", "contribution technique", "linearity of expectation in counting"]),
            (302, "Product Trick", ["product trick", "expected value expansion"])
        ],
        "Catalan": [
            (303, "Catalan Numbers", ["catalan numbers", "dyck paths", "valid parentheses sequences"]),
            (304, "Catalan Convolution", ["catalan convolution"])
        ],
        "Inclusion Exclusion": [
            (305, "Principle of Inclusion and Exclusion (PIE)", ["inclusion exclusion", "pie"]),
            (306, "Derangements", ["derangements", "subfactorial"]),
            (307, "Inclusion Exclusion on Multiples", ["pie on multiples"])
        ],
        "Factorials and Binomial Coefficients (nCr)": [
            (308, "Lucas Theorem", ["lucas theorem", "ncr mod p prime"]),
            (309, "nCr Modulo Any Mod", ["ncr non prime mod", "prime factorization ncr"]),
            (310, "Large Factorials and Binomial Coefficients", ["large factorials"]),
            (311, "Legendre's Formula", ["legendre formula", "vp(n!)"]),
            (312, "Prefix Sum Queries of Binomial Coefficients", ["binomial prefix sum"]),
            (313, "Prefix Sum of Binomial Coefficients for a Fixed Large N", ["fixed n binomial sum"]),
            (314, "Sum of nCr Over a Fixed Congruence Class", ["roots of unity filter", "ncr mod k"]),
            (315, "[Problem] Sum of nCr(a[i], K) for each K from 1 to N", ["sum of ncr"])
        ],
        "Stirling Numbers": [
            (316, "Stirling Numbers (Basic)", ["stirling numbers"]),
            (317, "Stirling Number of the First Kind for Fixed N", ["stirling 1st kind fixed n"]),
            (318, "Stirling Number of the First Kind for Fixed K", ["stirling 1st kind fixed k"]),
            (319, "Stirling Number of the Second Kind for Fixed N", ["stirling 2nd kind fixed n"]),
            (320, "Stirling Number of the Second Kind for Fixed K", ["stirling 2nd kind fixed k"])
        ],
        "Partitions": [
            (321, "Partitions of an Integer, Partition Function and Pentagonal Number Theorem", ["integer partition", "euler pentagonal", "partition function"]),
            (322, "Partitions of a Set / Bell Number", ["bell numbers", "set partitions"])
        ],
        "Miscellaneous": [
            (323, "Burnside's Lemma / Polya Enumeration Theorem", ["burnside's lemma", "polya enumeration", "orbit counting"]),
            (324, "Bertrand's Ballot Theorem", ["ballot theorem", "reflection principle"]),
            (325, "Young Tableaus and the Hook Length Formula", ["hook length formula", "standard young tableau", "rsy correspondence"])
        ]
    },
    "Math": {
        "Convolution": [
            (326, "Fast Fourier Transform (FFT)", ["fft", "fast fourier transform", "polynomial multiplication"]),
            (327, "Number Theoretic Transform (NTT)", ["ntt", "number theoretic transform", "998244353"]),
            (328, "2D FFT / NTT", ["2d fft", "2d ntt"]),
            (329, "Online FFT / NTT", ["online fft", "cdq fft", "semi-online convolution"]),
            (330, "Fast Walsh Hadamard Transform (FWHT) and its Variations", ["fwht", "walsh hadamard", "xor convolution", "and convolution", "or convolution"]),
            (331, "GCD Convolution", ["gcd convolution"]),
            (332, "LCM Convolution", ["lcm convolution"])
        ],
        "Polynomial": [
            (333, "Generating Functions", ["generating functions", "ogf", "egf"]),
            (334, "Polynomial Inverse", ["polynomial inverse"]),
            (335, "Polynomial Exp", ["polynomial exp"]),
            (336, "Polynomial Log", ["polynomial log"]),
            (337, "Polynomial Pow", ["polynomial pow"]),
            (338, "Polynomial Sqrt", ["polynomial sqrt"]),
            (339, "Polynomial Composition", ["polynomial composition"]),
            (340, "Multipoint Evaluation", ["multipoint evaluation"]),
            (341, "Chirp Z Transform", ["chirp z transform", "bluestein algorithm"]),
            (342, "Polynomial Interpolation", ["polynomial interpolation"]),
            (343, "Polynomial Shift", ["polynomial shift"]),
            (344, "Shift of Sampling Points of Polynomial", ["shift sampling points"]),
            (345, "Polyomial Division and Remainder", ["polynomial division"]),
            (346, "Polynomial Roots Under a Modulo", ["polynomial roots"]),
            (347, "Resultant of Two Polynomials and Half-GCD Algorithm", ["resultant", "half-gcd"]),
            (348, "Lagrange Interpolation", ["lagrange interpolation", "o(n) interpolation"]),
            (349, "[Problem] Sum of r^i * poly(i)", ["sum r^i * poly(i)"]),
            (350, "Polynomial with Binomial Coefficients", ["binomial polynomial"]),
            (351, "Subset Sum Problem using Generating Functions", ["generating function subset sum"]),
            (352, "Polynomial Factorization of (x^n - 1) and Cyclotomic Polynomials", ["cyclotomic polynomials"]),
            (353, "Schwartz–Zippel Lemma", ["schwartz-zippel lemma", "polynomial identity testing"]),
            (354, "Lagrange Inversion Theorem", ["lagrange inversion formula"])
        ],
        "Matrices": [
            (355, "Matrix Exponentiation", ["matrix exponentiation", "matrix power", "transition matrix"]),
            (356, "Permanent of a Matrix", ["permanent of matrix"]),
            (357, "Freivald's Algorithm", ["freivalds' algorithm", "randomized matrix check"]),
            (358, "Vandermonde Matrix", ["vandermonde matrix"]),
            (359, "Hafnian of a Matrix / Number of Perfect Matchings in a Graph", ["hafnian", "perfect matchings count"]),
            (360, "Frobenius Form of a Matrix and Fast Matrix Power", ["frobenius form", "companion matrix"])
        ],
        "Linear Recurrence": [
            (361, "Linear Recurrence Relations", ["linear recurrence"]),
            (362, "Linear Recurrence using Cayley-Hamilton Theorem in O(N^2 log K)", ["cayley-hamilton", "fast recurrence"]),
            (363, "Linear Recurrence using Generating Functions in O(N log N log K)", ["bostan-mori", "fiduccia algorithm"]),
            (364, "Linear Recurrence with Polynomial Coefficients", ["polynomial coefficients recurrence"]),
            (365, "Linear Recurrence on Matrices", ["matrix linear recurrence"]),
            (366, "Generating Function of a Linear Recurrence", ["gf of linear recurrence"]),
            (367, "Berlekamp Massey", ["berlekamp massey", "find shortest linear recurrence"]),
            (368, "Reeds-Sloane Algorithm", ["reeds-sloane algorithm"])
        ],
        "Linear Algebra": [
            (369, "Gaussian Elimination", ["gaussian elimination", "rref", "row reduction"]),
            (370, "Gaussian Elimination Modulo 2", ["gaussian elimination mod 2", "bitset gaussian"]),
            (371, "Determinant of a Matrix", ["determinant"]),
            (372, "Determinant under Composite Modulo", ["determinant composite mod"]),
            (373, "Characteristic Polynomial and Hesserberg Matrix", ["characteristic polynomial", "hessenberg matrix"]),
            (374, "[Problem] Determinant of Product Matrix", ["determinant product"]),
            (375, "Determinant of Sparse Matrix and Black Box Linear Algebra", ["wiedemann algorithm"]),
            (376, "[Problem] Determinant of Permutant and Circulant Matrix", ["circulant matrix"]),
            (377, "GCD Determinant / Smith's Determinant", ["smith determinant"]),
            (378, "Cauchy–Binet formula", ["cauchy-binet"]),
            (379, "Inverse of a Matrix", ["matrix inverse"]),
            (380, "Inverse of a Matrix modulo 2", ["matrix inverse mod 2"]),
            (381, "Thomas Algorithm", ["tridiagonal matrix", "thomas algorithm"]),
            (382, "Vector Space and XOR Basis", ["xor basis", "linear basis", "maximum xor subset"]),
            (383, "[Technique] XOR Basis ft Reduced Row Echelon Form", ["xor basis rref"]),
            (384, "[Technique] XOR Basis ft Lexicographically Largest Basis", ["lexicographically largest basis"]),
            (385, "XOR Basis with Deletions (Online)", ["online xor basis deletion"]),
            (386, "q Binomial", ["gaussian binomial coefficients", "q-binomial"])
        ],
        "Formulas": [
            (387, "Gauss's Eureka Theorem", ["gauss eureka"]),
            (388, "Titu's Lemma", ["titu's lemma", "cauchy-schwarz"]),
            (389, "Lifting-the-exponent(LTE) Lemma", ["lte lemma", "lifting the exponent"]),
            (390, "Faulhaber's Formula and Bernoulli Numbers", ["faulhaber's formula", "bernoulli numbers", "sum of powers"])
        ],
        "Calculus": [
            (391, "Differentiation and Integration", ["numerical integration", "simpson's rule"]),
            (392, "Line Integral", ["line integral"])
        ],
        "Probabilities and Expected Values": [
            (393, "Probabilities and Expected Values", ["probability", "expected value", "linearity of expectation"]),
            (394, "Expected Value Powers Technique", ["powers of random variables"]),
            (395, "The Slime Trick", ["slime trick expected value"]),
            (396, "Expected Occurrence Time as Substring", ["expected substring appearance"]),
            (397, "Gambler's Ruin", ["gambler's ruin"]),
            (398, "Martingale", ["martingale", "stopping time theorem"])
        ],
        "Mathematical Optimization": [
            (399, "Lagrange Multiplier", ["lagrange multiplier"]),
            (400, "Linear Programming / Simplex Algorithm", ["linear programming", "simplex"]),
            (401, "Duality in Linear Programming (LP <> Flow)", ["lp duality"]),
            (402, "Dinkelbach Algorithm", ["0-1 fractional programming", "dinkelbach"])
        ],
        "Miscellaneous": [
            (403, "Continued Fractions", ["continued fractions"]),
            (404, "Polynomial Real Roots", ["sturm's theorem", "newton-raphson"]),
            (405, "Finite Field Arithmetic Binary", ["nim multiplication", "finite fields"])
        ]
    },
    "Strings": {
        "String Matching": [
            (406, "Knuth Morris Pratt (KMP) and Prefix Automaton", ["kmp", "prefix function", "pi array", "knuth morris pratt"]),
            (407, "Z Algorithm", ["z-algorithm", "z-function", "z array"]),
            (408, "String Matching using Bitsets", ["bitset string matching", "shift-and"]),
            (409, "String Matching with FFT ft Wildcard Matching", ["string matching with fft", "wildcard matching"])
        ],
        "Hashing": [
            (410, "String Hashing", ["string hashing", "polynomial rolling hash", "double hash"]),
            (411, "2D String Hashing", ["2d string hashing", "subgrid hash"]),
            (412, "XOR Hashing", ["xor hashing", "random weight hash"]),
            (413, "Multiset Hashing", ["multiset hashing"])
        ],
        "Aho Corasick": [
            (414, "Aho Corasick", ["aho-corasick", "aho corasick", "dictionary matching automaton"]),
            (415, "Dynamic Aho Corasick", ["dynamic aho corasick"])
        ],
        "Suffix Structures": [
            (416, "Suffix Array", ["suffix array", "lcp array", "kasai's algorithm"]),
            (417, "Isomorphic Suffix Array", ["isomorphic suffix array"]),
            (418, "Dynamic Suffix Array", ["dynamic suffix array"]),
            (419, "Suffix Automaton", ["suffix automaton", "sam", "directed acyclic word graph"]),
            (420, "[Problem] Distinct Substring Queries in Range", ["distinct substring in range"]),
            (421, "Suffix Tree", ["suffix tree", "ukkonen's algorithm"])
        ],
        "Palindromes": [
            (422, "Palindromic Tree / Eertree", ["palindromic tree", "eertree"]),
            (423, "Persistent Palindromic Tree", ["persistent eertree"]),
            (424, "Manachers Algorithm", ["manacher", "longest palindromic substring"]),
            (425, "[Problem] Minimum Palindrome Factorization", ["palindrome factorization"]),
            (426, "[Problem] Number of Palindromes in Range", ["palindromes in range"])
        ],
        "Longest Common Subsequence (LCS)": [
            (427, "Longest Common Subsequence (LCS)", ["lcs", "longest common subsequence"]),
            (428, "All Substring Longest Common Subsequence", ["all substring lcs"]),
            (429, "Bit LCS", ["bit-parallel lcs"]),
            (430, "Cyclic LCS", ["cyclic lcs"]),
            (431, "LCS on RLE compressed string", ["rle lcs"])
        ],
        "Miscellaneous": [
            (432, "Balanced Brackets", ["balanced brackets", "parentheses validation"]),
            (433, "Expression Parsing", ["shunting yard", "expression parsing", "recursive descent"]),
            (434, "Lyndon Factorization / Duval Algorithm", ["lyndon factorization", "duval's algorithm", "minimal string rotation"]),
            (435, "Finding Repetitions / Main-Lorentz Algorithm", ["main-lorentz", "runs", "repetitions in string"]),
            (436, "De Bruijn Sequence", ["de bruijn sequence"])
        ]
    },
    "Dynamic Programming (DP)": {
        "Intro to DP": [
            (437, "Knapsack and Basic Dynamic Programming", ["knapsack", "0/1 knapsack", "unbounded knapsack", "dp basics"]),
            (438, "Knapsack and Subset Sum Optimizations", ["subset sum bitset", "item grouping knapsack"])
        ],
        "Digit DP": [
            (439, "Digit DP", ["digit dp", "count numbers in range [l, r] satisfying condition"])
        ],
        "DP Optimizations": [
            (440, "Divide and Conquer Optimization", ["d&c dp", "divide and conquer optimization", "quadrangle inequality"]),
            (441, "Knuth Optimization", ["knuth optimization"]),
            (442, "Aliens Trick / WQS Binary Search", ["aliens trick", "wqs binary search", "lagrangian relaxation dp"]),
            (443, "1D1D DP Optimization", ["1d/1d dp", "smawk dp"]),
            (444, "DP Optimization using Data Structures [Some Practice Problems]", ["data structure optimized dp", "segtree dp", "fenwick dp"])
        ],
        "Convex Hull Trick (CHT)": [
            (445, "Convex Hull Trick (CHT) and Dynamic CHT", ["convex hull trick", "cht", "line container"]),
            (446, "Persistent CHT", ["persistent cht"])
        ],
        "Li Chao Tree": [
            (447, "Li Chao Tree", ["li chao tree", "li-chao segment tree"]),
            (448, "Persistent Li Chao Tree", ["persistent li chao tree"]),
            (449, "Extended Li Chao tree", ["extended li chao tree"])
        ],
        "Bit Related DP": [
            (450, "Bitmask DP", ["bitmask dp", "submask enumeration", "tsp dp"]),
            (451, "Sum Over Subsets DP (SOS DP)", ["sos dp", "sum over subsets"]),
            (452, "[Problem] Subset Union of Bitsets", ["subset union"]),
            (453, "Subset Convolution", ["subset convolution", "fwt subset convolution"]),
            (454, "[Trick] Dynamic Submask Count", ["dynamic submask"]),
            (455, "[Problem] XOR Equation", ["xor equation dp"])
        ],
        "More Tricks": [
            (456, "Open and Close Interval Trick", ["open and close interval trick", "endpoint matching dp"]),
            (457, "Slope Trick", ["slope trick", "convex piecewise linear"]),
            (458, "x2 +1 Trick", ["collatz dp trick"]),
            (459, "Combining Subtrees Technique", ["combining subtrees", "tree knapsack o(n^2)"])
        ],
        "Classic DP": [
            (460, "Longest Increasing Subsequence (LIS)", ["lis", "longest increasing subsequence", "patience sorting"]),
            (461, "Interval DP / Range DP / Matrix Chain Multiplication (MCM)", ["range dp", "interval dp", "matrix chain multiplication"]),
            (462, "Edit Distance", ["edit distance", "levenshtein distance"])
        ],
        "Dp on Different Structures": [
            (463, "DP on Trees and DAGs", ["tree dp", "dag dp", "toposort dp"]),
            (464, "DP over Divisors", ["divisor dp", "gcd dp"]),
            (465, "Substring DP", ["substring dp"]),
            (466, "DP on Convex Hulls", ["convex hull dp"])
        ],
        "Miscellaneous": [
            (467, "Connected Component DP", ["connected component dp", "insertion dp"]),
            (468, "Broken Profile DP / Plug DP", ["broken profile dp", "plug dp", "domino tiling"]),
            (469, "Hirschberg's Algorithm", ["hirschberg", "linear space lcs"]),
            (470, "[Problem] Number of Subsequences Having Product at least K", ["product at least k subsequences"]),
            (471, "[Problem] Range LIS Query", ["range lis"])
        ]
    },
    "Game Theory": {
        "Grundy Number / Nim": [
            (472, "Grundy Number and Basic Game Theory", ["sprague-grundy", "grundy value", "nim", "mex game"]),
            (473, "Nimber", ["nimber", "field of nimbers"])
        ],
        "Hackenbush": [
            (474, "Green Hackenbush on Trees and Graphs", ["green hackenbush", "colon principle"]),
            (475, "Blue Red HackenBush", ["surreal numbers hackenbush"])
        ],
        "Graph Games": [
            (476, "Games on Arbitrary Graphs", ["game on graph", "winning losing states graph"]),
            (477, "[Problem] Matching Game On A Graph", ["matching game", "maximum matching game"])
        ],
        "Miscellaneous": [
            (478, "Alpha Beta Pruning", ["alpha beta pruning", "minimax"])
        ]
    },
    "Geometry": {
        "Euclidean Geometry": [
            (479, "Euclidean Geometry", ["euclidean geometry"])
        ],
        "Geometry 2D": [
            (480, "Points, Vectors, Transformations, Dot Products, Cross Products, Precision Issues and Polar Sort(2D)", ["cross product", "dot product", "polar sort", "point 2d"]),
            (481, "Lines, Segments, Rays, Distance and Relation Between Two Structures, Projections and Reflections(2D)", ["segment intersection", "line distance", "projection"]),
            (482, "Circles, Circle Relations, Intersections, Inscribed Circles and Circumcircles(2D)", ["circle intersection", "circumcircle", "incircle"]),
            (483, "Tangents(2D)", ["tangent lines to circle"]),
            (484, "Circles of Apollonius(2D)", ["apollonius circle"]),
            (485, "Circle Union(2D)", ["circle union area"]),
            (486, "Polygons(2D)", ["shoelace formula", "polygon area"]),
            (487, "Centroid of a Polygon(2D)", ["polygon centroid"]),
            (488, "Geometric Median(2D)", ["weiszfeld algorithm", "geometric median"]),
            (489, "Convex Hull(2D)", ["convex hull", "graham scan", "monotone chain", "andrew convex hull"]),
            (490, "Point in Convex Polygon in log(N)(2D)", ["point in convex polygon"]),
            (491, "Winding Number and Point in Simple Polygon(2D)", ["point in simple polygon", "ray casting", "winding number"]),
            (492, "Extreme Vertex(2D)", ["extreme vertex of polygon"]),
            (493, "Rotating Calipers ft Diameter and Width of a Convex Polygon and Minimum Enclosing Rectangle(2D)", ["rotating calipers", "polygon diameter", "minimum bounding box"]),
            (494, "Minimum Enclosing Circle(2D)", ["welzl's algorithm", "minimum enclosing circle"]),
            (495, "Polygon Line and Convex Line Intersection, and Polygon Cutting(2D)", ["polygon cutting", "sutherland-hodgman"]),
            (496, "Tangents from Point to Convex and Convex to Convex(2D)", ["tangents to convex polygon"]),
            (497, "Distance from Point to Convex, Convex to Line and Convex to Convex(2D)", ["distance to convex polygon"]),
            (498, "Maximum Distance from Convex to Convex(2D)", ["max distance convex"]),
            (499, "Polygon Union(2D)", ["polygon union area", "greiner-hormann"]),
            (500, "Polygon Triangulation(2D)", ["ear clipping", "polygon triangulation"]),
            (501, "Maximum Circle Cover(2D)", ["maximum circle cover"]),
            (502, "Maximum Inscribed Circle in a Convex(2D)", ["chebyshev center", "inscribed circle"]),
            (503, "Triangle Circle and Polygon Circle Intersection(2D)", ["polygon circle intersection"])
        ],
        "Geometry 3D": [
            (504, "Points, Vectors, Dot Products, Cross Products and Mixed Products(3D)", ["3d vectors", "scalar triple product"]),
            (505, "Planes(3D)", ["plane equation"]),
            (506, "Plane Based Coordinate System(3D)", ["plane coordinate"]),
            (507, "Lines, Segments, and Distances, Angles and Intersections Between Lines and Planes(3D)", ["3d line plane distance"]),
            (508, "Triangles and Distance from Triangle to Triangle(3D)", ["3d triangles distance"]),
            (509, "Spherical Geometry and Winding Number(3D)", ["great circle distance", "spherical geometry"]),
            (510, "Minimum Enclosing Sphere(3D)", ["minimum enclosing sphere"]),
            (511, "Polyhedron, Pyramid, Cone and Cylinder(3D)", ["polyhedron volume"]),
            (512, "Convex Hull(3D)", ["3d convex hull"])
        ],
        "Delaunay": [
            (513, "Delaunay Triangulation and Voronoi Diagram", ["delaunay triangulation", "voronoi diagram", "fortune's algorithm"])
        ],
        "Half Plane": [
            (514, "Half Plane Intersection", ["half-plane intersection", "half plane intersection"]),
            (515, "Dynamic Half Plane Intersection", ["dynamic half plane"])
        ],
        "Convex Polygon": [
            (516, "Minkowski Sum", ["minkowski sum"]),
            (517, "Dynamic Convex Hull", ["dynamic convex hull"]),
            (518, "Onion Decomposition / Convex Layers", ["convex layers", "onion decomposition"])
        ],
        "Lattice Points": [
            (519, "Picks Theorem", ["pick's theorem", "lattice polygon area"]),
            (520, "Lattice Points inside a Non-Lattice Polygon", ["lattice points count"])
        ],
        "Sweep Line": [
            (521, "Sweep Line Algorithm and Radial Sweep", ["sweep line", "radial sweep", "angle sort"]),
            (522, "Closest Pair of Points", ["closest pair of points"]),
            (523, "Rectangle Union", ["klee's measure", "rectangle union area", "segtree sweep"]),
            (524, "All Pair Segment Intersection.", ["bentley-ottmann"]),
            (525, "Vertical decomposition", ["trapezoidal map", "vertical decomposition"])
        ],
        "Planar Geometry": [
            (526, "Faces in Planar Graph", ["euler planar formula v-e+f=2"]),
            (527, "Point Location", ["kirkpatrick's point location"])
        ],
        "Miscellaneous": [
            (528, "Hill Climbing and Simulated Annealing", ["simulated annealing", "hill climbing"]),
            (529, "[Trick] Linear Combination of Vectors", ["linear combination vectors"]),
            (530, "Reflections on a Rectangle", ["billards reflection"]),
            (531, "[Problem] Maximum Area of a Triangle from Given Lengths", ["heron's formula max triangle"]),
            (532, "[Problem] Maximum Area of a Polygon using Given Lengths in CCW Order", ["cyclic polygon"]),
            (533, "[Problem] Circle/Polygon Inclusion Tree", ["polygon nesting tree"])
        ]
    },
    "Miscellaneous": {
        "Greedy Algorithms": [
            (534, "Activity Selection Problem", ["interval scheduling", "activity selection"]),
            (535, "Fractional Knapsack Problem", ["fractional knapsack"]),
            (536, "Huffman Coding", ["huffman coding"]),
            (537, "Exchange Arguments", ["exchange argument", "sorting order greedy"])
        ],
        "Search Techniques": [
            (538, "Ternary Search", ["ternary search", "unimodal function"]),
            (539, "Parallel Binary Search", ["parallel binary search", "pbs"]),
            (540, "Fraction Binary Search", ["fraction binary search", "mediant search"]),
            (541, "Fracturing Search", ["fracturing search"])
        ],
        "Interactive Problems": [
            (542, "Interactive Problems", ["interactive", "query limit", "hidden array"]),
            (543, "Interactive Problems on Centroids", ["interactive tree centroid"])
        ],
        "Communication / Run-Twice Problems": [
            (544, "Communication / Run-Twice Problems", ["communication problem", "run-twice"])
        ],
        "Permutations": [
            (545, "Permutations and Permutation Cycles", ["permutation cycle decomposition", "disjoint cycles"]),
            (546, "[Problem] K-th Root of a Permutation", ["k-th root permutation"]),
            (547, "Schreier–Sims Algorithm", ["schreier-sims algorithm", "permutation group"])
        ],
        "Matroids": [
            (548, "Matroid Intersection", ["matroid intersection", "graphic matroid", "colorful spanning tree"])
        ],
        "Chess": [
            (549, "[Problem] Knight Moves in Infinity Grid", ["knight moves"]),
            (550, "[Problem] Knight's Tour Problem", ["knight's tour"]),
            (551, "[Problem] Bishop Placement", ["bishops placement"])
        ],
        "Techniques": [
            (552, "Coordinate Compression", ["coordinate compression", "compression"]),
            (553, "Direction Array", ["dx dy", "grid directions"]),
            (554, "Meet in the Middle", ["meet in the middle", "mitm"]),
            (555, "Invariants and Monovariants", ["invariant", "monovariant"]),
            (556, "Manhattan <> Chebyshev", ["manhattan to chebyshev", "x+y x-y"]),
            (557, "LCM OR Technique", ["lcm or trick"]),
            (558, "[Trick] Logarithmic Subarray Aggregator (LSA Trick)", ["logarithmic subarray aggregator"]),
            (559, "Bitwise Disjoint Partitioning", ["bitwise disjoint"]),
            (560, "[Trick] Efficient Non-Increasing Sequence Recovery of Length n with a[i] <= n/i", ["sequence recovery trick"])
        ],
        "Min Plus Convolution": [
            (561, "Min Plus Convolution (Convex and Convex)", ["min plus convolution", "tropical convolution"]),
            (562, "SMAWK Algorithm and Min Plus Convolution (Convex and Arbitrary)", ["smawk algorithm", "concave matrix"])
        ],
        "Randomized": [
            (563, "Randomized Algorithms", ["randomized", "mt19937", "random check"]),
            (564, "Birthday Paradox", ["birthday paradox"])
        ],
        "Bigint": [
            (565, "Big Integers", ["bigint", "arbitrary precision"]),
            (566, "Trygub Numbers", ["trygub numbers"])
        ],
        "Miscellaneous": [
            (567, "Inversions", ["inversions count", "number of inversions"]),
            (568, "Josephus Problem", ["josephus problem", "josephus"]),
            (569, "Gray Code", ["gray code"]),
            (570, "Backtracking", ["backtracking", "branch and bound"]),
            (571, "[Problem] MEX of all Subarrays", ["mex of all subarrays", "mex query"]),
            (572, "Lindstrom Gessel Viennot(LGV) Lemma", ["lgv lemma", "non-intersecting paths"]),
            (573, "Dynamic Bitsets", ["dynamic bitset"]),
            (574, "Pragmas", ["#pragma GCC optimize"]),
            (575, "Boyer–Moore Majority Voting Algorithm and Misra–Gries Algorithm", ["boyer-moore majority vote", "misra-gries"]),
            (576, "Heavy Implementation Problems", ["heavy implementation", "simulation"])
        ]
    }
}
