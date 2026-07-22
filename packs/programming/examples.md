# Few-shot examples

These show the expected depth: assumptions, typed code, complexity, named edge cases, executable tests, and honest tradeoffs. Verification is delegated to code_runner, never asserted from memory.

---

**Q:** Write a function to find duplicates in a list.

**A:** Assuming Python 3.9+, elements are hashable. If they are not hashable, this needs a different approach (sorting or pairwise comparison) — say so if that is your case.

```python
from collections import Counter

def find_duplicates(items: list) -> list:
    """Return elements appearing more than once, in first-seen order."""
    counts = Counter(items)
    seen = set()
    out = []
    for item in items:
        if counts[item] > 1 and item not in seen:
            seen.add(item)
            out.append(item)
    return out

assert find_duplicates([1, 2, 2, 3, 1]) == [1, 2]
assert find_duplicates([]) == []
assert find_duplicates([1]) == []
assert find_duplicates([1, 1, 1]) == [1]
print("ok")
```

Complexity: O(n) time, O(n) space — one pass to count, one to order.

Edge cases handled: empty list, single element, all-identical, preserving first-seen order.

Tradeoff: a `set`-only version is shorter but loses ordering and cannot distinguish "seen twice" from "seen once". Sorting would be O(n log n) and O(1) extra space — better if memory is the constraint and order does not matter.

I will run this via code_runner rather than claiming the assertions pass.

---

**Q:** Is this fine? `for u in users: db.execute("SELECT * FROM t WHERE id=" + u.id)`

**A:** No — two real problems, not style.

1. **SQL injection.** String concatenation into a query is unsafe if `u.id` is ever attacker-controlled. Use parameterized queries: `db.execute("SELECT * FROM t WHERE id = ?", (u.id,))`.
2. **N+1 queries.** One round trip per user. With 1,000 users that is 1,000 network round trips. Fetch in one query with `WHERE id IN (...)` (batched) and group in memory.

The injection issue is the urgent one; fix it regardless of scale.

Here is the corrected version as a self-contained, runnable demonstration — real code with an in-memory database stand-in, so code_runner can actually verify it:

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE t (id INTEGER, name TEXT)")
conn.executemany("INSERT INTO t VALUES (?, ?)", [(1, "ana"), (2, "ben"), (3, "cy")])

class User:
    def __init__(self, id): self.id = id

users = [User(1), User(3)]
ids = [u.id for u in users]

if ids:
    placeholders = ",".join("?" for _ in ids)
    rows = conn.execute(f"SELECT * FROM t WHERE id IN ({placeholders})", ids).fetchall()
else:
    rows = []

assert rows == [(1, "ana"), (3, "cy")]
assert len(ids) == 2          # one query, not N
print("ok:", rows)
```

Note the table name is interpolated only from a trusted literal; the *values* always go through placeholders. Empty-list case returns `[]` instead of emitting invalid SQL.

---

**Q:** Also, what's 15% of 240 for the discount?

**A:** Math sub-task, not code — route to the Math module / calculator: `0.15 * 240`.
