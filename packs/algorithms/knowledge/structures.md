# Choosing a data structure

Pick by the operation you do most, not by habit.

Frequent membership tests: use a set. Converting a list to a set costs O(n) once and turns every later O(n) lookup into O(1).

Keyed lookup or counting: use a dict, or collections.Counter for counting occurrences. Counter.most_common(k) gives top-k directly.

Queue (add at one end, remove from the other): use collections.deque. Using a list and pop(0) is O(n) per removal and becomes quadratic.

Stack (last in, first out): a plain list with append and pop is correct and O(1).

Top-k or repeatedly extracting the minimum: use heapq. A priority queue beats re-sorting.

Ordered data with frequent lookups by range: keep a sorted list and use the bisect module for O(log n) searches.

Fixed-size grouping or deduplication while preserving order: dict.fromkeys(items) deduplicates and keeps insertion order in Python 3.7 and later.

Immutable or hashable records: tuples and frozensets can be dict keys and set members; lists and dicts cannot.

Graphs: an adjacency dict mapping node to list of neighbours is usually the practical representation. Use BFS with a deque for shortest path in an unweighted graph, DFS with recursion or an explicit stack for exhaustive traversal, and heapq for Dijkstra on weighted graphs.
