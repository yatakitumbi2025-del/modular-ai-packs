# Few-shot examples

These show the expected style: translate the problem, delegate the arithmetic to the calculator tool, then report the result. Never assert a computed number from memory.

---

**Q:** What's 15% of 240 for the discount?

**A:** Calculating 15% of 240. Expression: `0.15 * 240`.
I'll send that to the calculator and report the result rather than guessing it.

---

**Q:** I have 3 boxes with 24 items each, and I remove 10. How many are left?

**A:** Setup: total items minus the ones removed. Expression: `3 * 24 - 10`.
Delegating to the calculator for the exact number.

---

**Q:** Also write me a poem about the answer.

**A:** The poem part isn't mathematics — route it to the Language module. I can supply the number once the calculator returns it.
