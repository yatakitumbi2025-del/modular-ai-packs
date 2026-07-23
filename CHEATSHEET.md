# Modular AI — reference card

Core: `~/modular-ai-core` (local, Termux)
Packs: `~/modular-ai-packs` → github.com/yatakitumbi2025-del/modular-ai-packs

---

## Run it

```bash
cd ~/modular-ai-core
python server.py
```

Open **127.0.0.1:8000**. Leave that Termux session alone while it runs.

Stop with **Ctrl+C**. Not Ctrl+Z — that suspends the job instead of ending it,
and the suspended process keeps holding port 8000, which shows up later as
`Errno 98: address already in use`.

Stuck server:

```bash
pkill -f server.py
jobs          # should be empty
```

---

## The cache rule

**Changed a pack on GitHub → clear caches. Changed a core file on the phone →
just restart.**

```bash
cd ~/modular-ai-core
rm -rf pack_cache && rm -f routing_cache.json
```

- `pack_cache/` — downloaded pack files (pack.json, prompt.md, examples.md,
  vectors.json)
- `routing_cache.json` — embedded domain vectors (each rebuild costs Jina calls)

Neither checks whether GitHub changed. Push an edit, restart, and the core
reads yesterday's copy with no error and no warning. Clearing unnecessarily
costs five seconds; forgetting costs an hour.

`routing_cache.json` is built *from* `pack_cache`, so clearing only the routing
cache does nothing if the pack files are stale. Clear both or neither.

Full sequence after a pack edit:

```bash
cd ~/modular-ai-packs
# ...edit...
git add . && git commit -m "what changed" && git push

cd ~/modular-ai-core
rm -rf pack_cache && rm -f routing_cache.json
python server.py
```

---

## Test routing without burning tokens

```bash
cd ~/modular-ai-core
python router.py
```

Prints domain and score without calling the model. Type **one question per
line** — pasting several at once merges them into a single garbled query and
the results are meaningless.

Baseline set:

```
How many grams of NaCl are in 400 mL of a 0.75 M solution?    science  ~0.26
explain photosynthesis                                         science
a 2 kg block slides down a 3 m ramp, how fast at the bottom?   science  (margin)
reverse a string in python                                     programming ~0.34
thanks that helped                                             general (chitchat guard)
hello                                                          general (chitchat guard)
```

---

## Score a description before pushing it

The tool that actually solves routing problems. Guessing at descriptions cost
a whole afternoon; this takes two minutes.

```bash
cd ~/modular-ai-core
python - <<'EOF'
import embed, router
t = router.build_routing_table()

QS = ["...5 real questions the pack should answer..."]

CAND = {
  "A": "first candidate description",
  "B": "second candidate description",
}

qv = [embed.embed(q) for q in QS]
for e in t:
    print(e["id"].ljust(12),
          [round(embed.cosine(v, e["vector"]), 3) for v in qv])
for name, text in CAND.items():
    dv = embed.embed(text)
    s = [round(embed.cosine(v, dv), 3) for v in qv]
    print(name.ljust(12), s, " min", min(s))
EOF
```

Pick the candidate that beats every existing domain on every question. Check
the **minimum**, not the average — one question falling below threshold is a
question that routes to general.

---

## Writing a `description_for_router`

Describe **what questions the pack answers**, not what the pack is.

- Bad: "Physics, chemistry, and biology fundamentals — units and dimensional
  analysis, mechanics, energy, stoichiometry." → abstract, scored 0.143
- Good: "Answers physics, chemistry and biology questions, including
  calculations: molarity and moles, grams of solute in a solution, balancing
  chemical equations, a block sliding down a ramp..." → scored 0.28

Use the vocabulary a person would actually type. "A block sliding down a ramp"
beats "mechanics" because that's what appears in the question.

Keywords get appended to the embedded profile, so a long list is fine — tested,
and ~60 keywords scored slightly *better* than 9.

---

## Routing internals

`router.py`:

- `ROUTE_THRESHOLD = 0.25` — absolute cosine floor
- `MARGIN_FLOOR = 0.10`, `MARGIN_RATIO = 2.0` — if nothing clears the
  threshold, take the leader when it reaches the floor AND is ≥2× the
  runner-up. Catches genuine wins that score low in absolute terms.
- `CHITCHAT` set + `_is_chitchat()` — returns `[]` before scoring for greetings
  and thanks. Necessary because short social messages have no subject matter,
  so their vectors are noise and land near arbitrary packs. No description
  tuning fixes that.

Watch: science scores ~0.256 on the NaCl question against a 0.25 threshold.
Six thousandths of headroom. If a future description edit breaks that question,
this is why.

---

## Debugging method

Every wrong guess this session came from reasoning about what *should* match.
Every fix came from printing actual cosine numbers.

Order to check things in:

1. Is the pack loaded? Header should list it.
2. Is the push live? `curl -s <raw github url> | grep -c <new text>`
3. Are the caches cleared? Both of them.
4. What are the actual scores? Run the scoring script.
5. Only then edit anything.

---

## Known limitation

Significant figures. The model reports 17.5 g where two sig figs means 18 g.
Three prompt versions failed to fix it, including one spelling out the exact
case. Looks like a llama-3.3-70b limitation rather than a prompt problem.

Option if it matters: drop the sig-fig rule and ask for the full computed value
plus a statement of input precision — no counting required, nothing to get
wrong.

---

## Backup

No git on the core, so this is the only copy:

```bash
cd ~
tar --exclude='*/pack_cache' --exclude='*/__pycache__' \
    -czf storage/downloads/modular-ai-core-backup.tar.gz modular-ai-core
```

(`zip` isn't installed in Termux; `tar` is.)
