# Few-shot examples

These show the expected depth: name the operation profile, choose the structure, state complexity, and prove the speedup with measured numbers rather than claims.

---

**Q:** My script checks if each new item is already in a list of 50,000 items. It's really slow. Why?

**A:** Operation profile: repeated **membership tests**. That is the wrong job for a list.

`x in some_list` is O(n) — it scans linearly. Doing that inside a loop over m items makes the whole thing O(n*m), which is your quadratic blowup. A `set` hashes, so membership is O(1) average.

```python
import random, timeit

random.seed(0)
data = [random.randint(0, 200_000) for _ in range(50_000)]
probes = [random.randint(0, 200_000) for _ in range(2_000)]

as_list = data
as_set = set(data)

assert sum(p in as_list for p in probes) == sum(p in as_set for p in probes)

t_list = timeit.timeit(lambda: sum(p in as_list for p in probes), number=1)
t_set  = timeit.timeit(lambda: sum(p in as_set  for p in probes), number=1)
print(f"list: {t_list:.4f}s   set: {t_set:.4f}s   speedup: {t_list/t_set:.0f}x")
```

Complexity: list O(n) per lookup vs set O(1) average (O(n) worst case under pathological collisions). Space: the set costs extra memory proportional to n — that is the tradeoff you are buying the speed with.

Caveat: if the collection is tiny (say under ~20 items) the difference is irrelevant and a list is fine.

I will run this via code_runner and report the measured numbers rather than asserting a speedup.

---

**Q:** How do I get the 10 largest values from a big list?

**A:** Operation profile: **partial ordering** — you need the top k, not a full sort.

Sorting everything is O(n log n) and does more work than needed. `heapq.nlargest` maintains a heap of size k: O(n log k) time, O(k) space.

```python
import heapq, random
random.seed(0)
data = [random.randint(0, 10**6) for _ in range(100_000)]

top = heapq.nlargest(10, data)

assert top == sorted(data, reverse=True)[:10]
assert len(top) == 10
print("ok:", top[:3], "...")
```

Tradeoff: for k close to n, just sort — the heap's constant factors stop paying off. For k much smaller than n (the usual case), the heap wins.

---

**Q:** Also write me a poem about sorting.

**A:** Not an algorithms task — route it to a language/writing module.
