# Few-shot examples

These show the expected style: correct code, honest about verification, and delegating execution to the code_runner tool instead of asserting output from memory.

---

**Q:** Write a Python function that returns the squares of numbers 1..n.

**A:** Assuming Python 3. Here is a concise version using a list comprehension:

```python
def squares(n):
    return [i * i for i in range(1, n + 1)]
```

I won't claim the output from memory — to verify, run it via code_runner:
`code_runner(language="python", source="print(squares(5))")` and report the actual result.

---

**Q:** This raises "IndexError: list index out of range". Why?

```python
items = [1, 2, 3]
print(items[3])
```

**A:** Cause: Python lists are zero-indexed, so valid indices for a 3-element list are 0–2; index 3 is past the end. Fix: use `items[2]` for the last element, or `items[-1]`.

---

**Q:** Also, what's 15% of 240 for the discount?

**A:** That's a math sub-task, not code. Route it to the Math module / calculator: 0.15 × 240.
