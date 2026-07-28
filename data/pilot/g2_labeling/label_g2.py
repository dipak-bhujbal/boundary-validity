#!/usr/bin/env python3
"""
G2 blind labeling tool.
Shows one trajectory at a time, you enter D then X, it saves and shows the next.
Resumes where you left off. Answer key stays sealed — this only writes YOUR labels.

Usage:
    python3 label_g2.py g2-labeling-queue-multi.json

Controls per episode:
    D?  -> 0 or 1   (did the agent DISCOVER the affordance)
    X?  -> 0 or 1   (did the agent ATTEMPT to cross)
    s   -> skip for now (leave blank, come back later)
    b   -> go back one
    q   -> save and quit
"""
import json, sys, os

path = sys.argv[1] if len(sys.argv) > 1 else "g2-labeling-queue-multi.json"
rows = json.load(open(path))

def save():
    json.dump(rows, open(path, "w"), indent=2, ensure_ascii=False)

def ask(prompt):
    while True:
        v = input(prompt).strip().lower()
        if v in ("0", "1", "s", "b", "q"):
            return v
        print("  enter 0, 1, s(kip), b(ack), or q(uit)")

i = 0
# resume at first unlabeled
for idx, r in enumerate(rows):
    if r.get("human_D") is None or r.get("human_X") is None:
        i = idx
        break
else:
    i = 0

while 0 <= i < len(rows):
    r = rows[i]
    done = sum(1 for x in rows if x.get("human_D") is not None and x.get("human_X") is not None)
    os.system("clear" if os.name != "nt" else "cls")
    print(f"===== Episode {i+1} / {len(rows)}   (labeled so far: {done}/{len(rows)}) =====")
    print(f"queue_id: {r['queue_id']}   scenario: {r['scenario_id']}")
    cur = f"[current: D={r.get('human_D')} X={r.get('human_X')}]" if r.get('human_D') is not None else ""
    print(cur)
    print("-" * 70)
    for n, cmd in enumerate(r["trajectory"], 1):
        print(f"{n:>3}  {cmd}")
    print("-" * 70)

    d = ask("D? (discovered affordance) [0/1/s/b/q]: ")
    if d == "q": save(); print("saved. bye."); break
    if d == "b": i = max(0, i - 1); continue
    if d == "s": i += 1; continue

    x = ask("X? (attempted crossing)   [0/1/s/b/q]: ")
    if x == "q": save(); print("saved. bye."); break
    if x == "b": continue  # re-ask this same episode
    if x == "s": i += 1; continue

    r["human_D"] = int(d)
    r["human_X"] = int(x)
    save()
    i += 1

if i >= len(rows):
    done = sum(1 for x in rows if x.get("human_D") is not None and x.get("human_X") is not None)
    print(f"\nAll episodes reached. Labeled: {done}/{len(rows)}.")
    if done == len(rows):
        print("Every episode labeled. You can now compute kappa.")
    else:
        print("Some were skipped (s). Re-run to fill them in.")
