# Problem patterns

Recognising the pattern usually matters more than clever code.

Find pairs summing to a target: use a hash set of seen values for O(n), instead of nested loops for O(n^2).

Detect duplicates: compare len(items) with len(set(items)) for O(n), or use a set while iterating to find the first duplicate early.

Count frequencies: collections.Counter in one pass, O(n).

Contiguous subarray or substring problems: sliding window with two pointers, O(n), instead of checking every pair of indices at O(n^2).

Sorted array searching: two pointers from both ends, or bisect for O(log n).

Top k elements: heapq.nlargest, O(n log k), rather than a full sort.

Overlapping subproblems (fibonacci, grid paths, knapsack): dynamic programming or memoization with functools.lru_cache turns exponential recursion into linear or polynomial time by trading memory.

Shortest path in an unweighted graph: breadth-first search with a deque. Depth-first search does not give shortest paths.

Cycle detection in a linked list or sequence: Floyd's fast and slow pointers, O(1) space.

Repeated queries over a static dataset: precompute an index or prefix-sum array once, then answer each query in O(1).
