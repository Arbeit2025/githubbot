"""CLI: read an issue/PR payload (JSON file or stdin), print a TriagePlan.

Dry-run by default: it only prints what it *would* label. Applying labels
is done by the GitHub Actions workflow step, not by this script, so a
local run can never modify a repository.
Usage: python -m bot.triage --kind issue --title '...' --body '...'
       python -m bot.triage --kind pr --title '...' --files a.py,docs/x.md --lines 120
"""
from __future__ import annotations
import argparse, json
from .label_logic import triage_issue, triage_pr

def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kind", choices=["issue", "pr"], required=True)
    p.add_argument("--title", default="")
    p.add_argument("--body", default="")
    p.add_argument("--files", default="", help="comma-separated changed files (PR)")
    p.add_argument("--lines", type=int, default=0, help="changed lines (PR)")
    a = p.parse_args()
    if a.kind == "issue":
        plan = triage_issue(a.title, a.body)
    else:
        plan = triage_pr(a.title, [f for f in a.files.split(",") if f], a.lines)
    print(json.dumps({"labels": plan.labels, "needs_info": plan.needs_info,
                      "reasons": plan.reasons}, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
