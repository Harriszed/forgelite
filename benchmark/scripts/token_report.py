"""Sum token usage for one or more Claude Code sessions, split by model and by main vs subagent.

Usage:
    python -I token_report.py <project-folder-pattern> [--sonnet-price 0.2]

<project-folder-pattern> is a glob under ~/.claude/projects, for example
    "*my-project--claude-worktrees-my-branch*"

Cost index (a rough, relative number, not a bill):
    input + 5 x output + 1.25 x cache writes + 0.1 x cache reads
then multiplied by --sonnet-price for Sonnet models (default 0.2 = Sonnet tokens cost a fifth of Opus tokens;
this is an assumption, so pass your own), and by --haiku-price for Haiku models (default 0.08).
"""
import argparse
import collections
import glob
import json
import os

ap = argparse.ArgumentParser()
ap.add_argument("pattern")
ap.add_argument("--sonnet-price", type=float, default=0.2)
ap.add_argument("--haiku-price", type=float, default=0.08)
args = ap.parse_args()

root = os.path.expanduser("~/.claude/projects")
files = [f for d in glob.glob(os.path.join(root, args.pattern)) for f in glob.glob(d + "/**/*.jsonl", recursive=True)]
if not files:
    raise SystemExit(f"No transcripts match {args.pattern!r} under {root}")

seen = set()
by = collections.defaultdict(collections.Counter)
calls = 0
for f in files:
    is_sub = "subagents" in f.replace("\\", "/")
    with open(f, encoding="utf-8", errors="replace") as fh:
        lines = fh.readlines()
    for line in lines:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        m = d.get("message")
        if not isinstance(m, dict) or m.get("role") != "assistant" or not m.get("usage"):
            continue
        key = m.get("id") or d.get("uuid")
        if key in seen:
            continue
        seen.add(key)
        calls += 1
        u = m["usage"]
        k = (m.get("model", "?"), "subagent" if is_sub else "main")
        for a in ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"):
            by[k][a] += u.get(a, 0) or 0

print(f"{calls} API calls in {len(files)} transcript files")
total = 0.0
for (model, role), c in sorted(by.items()):
    if model.startswith("<"):
        continue
    idx = c["input_tokens"] + 5 * c["output_tokens"] + 1.25 * c["cache_creation_input_tokens"] + 0.1 * c["cache_read_input_tokens"]
    price = args.sonnet_price if "sonnet" in model else args.haiku_price if "haiku" in model else 1.0
    total += idx * price
    print(f"{model:28} {role:9} out {c['output_tokens']:>9,}  cache-write {c['cache_creation_input_tokens']:>10,}  cache-read {c['cache_read_input_tokens']:>12,}  index {idx/1e6:5.2f}M x{price}")
print(f"\nWeighted cost index: {total/1e6:.2f}M")
