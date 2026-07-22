# Accidental quadratic and other pitfalls

These look innocent in review and destroy performance at scale.

Membership test against a list inside a loop: `if x in big_list` is O(n), so inside a loop it is O(n*m). Convert the list to a set first.

list.insert(0, x) or list.pop(0) inside a loop: each is O(n) because every element shifts. Use collections.deque with appendleft and popleft, both O(1).

String concatenation in a loop: `s += piece` creates a new string each time, giving O(n^2) total copying. Collect the pieces in a list and use "".join(pieces) instead.

Calling sorted() inside a loop: sort once outside the loop, or maintain a heap.

Re-computing an expensive value each iteration: hoist it out of the loop, or cache it with functools.lru_cache.

Nested loops over the same data to find matches: usually replaceable by a dict or set lookup, turning O(n^2) into O(n).

Mutating a list while iterating over it: this skips elements and causes subtle bugs. Iterate over a copy, or build a new list with a comprehension.

Deep recursion: Python's default recursion limit is about 1000 frames, and each frame costs stack space. Convert to an iterative loop with an explicit stack for large inputs.

Premature optimisation: if n is small and fixed, an O(n^2) loop is fine. Measure before optimising, and optimise the part that actually dominates the runtime.
