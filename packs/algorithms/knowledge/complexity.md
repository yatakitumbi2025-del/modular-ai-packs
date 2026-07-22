# Complexity reference

Big-O describes how cost grows with input size n. It ignores constant factors, so an O(n) algorithm can lose to an O(n log n) one at small n.

## Python operation costs

List: index access O(1), append amortised O(1), pop from end O(1), pop from front O(n), insert at front O(n), membership `x in list` O(n), length O(1).

Dict and set: lookup, insert and delete are O(1) average and O(n) worst case under pathological hash collisions. Iteration is O(n). Keys must be hashable.

Deque (collections.deque): append and popleft are both O(1). This is the correct queue. Random index access is O(n), unlike a list.

Heap (heapq): push O(log n), pop smallest O(log n), peek smallest O(1), heapify a list O(n), nlargest/nsmallest of k items O(n log k).

Sorting: Python's sort is Timsort, O(n log n) worst case, O(n) on already-sorted data, and it is stable. Sorting requires O(n) extra space.

Binary search (bisect): O(log n), but only on an already-sorted sequence. Sorting first to enable one binary search is not worth it; sorting costs more than a linear scan.

## Growth rates

O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n) linearithmic, O(n^2) quadratic, O(2^n) exponential. For n = 1,000,000: log n is about 20, n log n is about 20 million, n^2 is a trillion — the difference between instant and never finishing.

## Space complexity

Space counts extra memory beyond the input. Recursion uses O(depth) stack space. Memoization trades O(n) space for a large time saving. An in-place algorithm is O(1) extra space.

## Amortised versus worst case

Amortised means averaged over many operations. list.append is amortised O(1) because occasional resizing is O(n) but rare. Report both when they differ; do not quote the average as a guarantee.
