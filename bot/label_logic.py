"""Pure logic for GitHub repo automation: no network, fully testable.

Decides labels / actions from issue text, changed files and PR size.
The GitHub Actions workflows call this logic (via triage.py) in dry-run
first, and only apply labels when explicitly enabled.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field

# keyword -> label (lowercase substring / word match, JP + EN)
KEYWORD_LABELS: dict[str, list[str]] = {
    "bug": ["bug", "error", "fail", "crash", "エラー", "バグ", "不具合", "落ちる", "動かない"],
    "enhancement": ["feature", "enhancement", "要望", "追加したい", "改善案", "提案"],
    "documentation": ["readme", "docs", "document", "ドキュメント", "説明文"],
    "question": ["question", "how to", "質問", "教えて", "わからない"],
    "security": ["security", "vulnerability", "セキュリティ", "脆弱性", "漏洩"],
    "performance": ["slow", "performance", "遅い", "重い", "パフォーマンス"],
}

# changed-file path prefix/glob -> label
PATH_LABELS: list[tuple[str, str]] = [
    ("docs/", "documentation"), ("*.md", "documentation"),
    ("tests/", "tests"), ("test_", "tests"),
    (".github/workflows/", "ci"), ("*.yml", "ci"), ("*.yaml", "ci"),
    ("requirements", "dependencies"), ("package.json", "dependencies"),
    ("package-lock.json", "dependencies"), ("Pipfile", "dependencies"),
]

SIZE_THRESHOLDS = [(50, "size/S"), (200, "size/M"), (500, "size/L")]

@dataclass
class TriagePlan:
    labels: list[str] = field(default_factory=list)
    needs_info: bool = False
    reasons: dict[str, str] = field(default_factory=dict)

def labels_for_text(title: str, body: str = "") -> dict[str, str]:
    text = f"{title}\n{body}".lower()
    found: dict[str, str] = {}
    for label, words in KEYWORD_LABELS.items():
        for w in words:
            if w.lower() in text:
                found[label] = f"keyword: {w}"
                break
    return found

def labels_for_files(files: list[str]) -> dict[str, str]:
    found: dict[str, str] = {}
    for f in files:
        for pat, label in PATH_LABELS:
            if pat.startswith("*") and f.endswith(pat[1:]):
                found[label] = f"file: {f}"
            elif pat in f:
                found[label] = f"file: {f}"
    return found

def size_label(changed_lines: int) -> str:
    for limit, label in SIZE_THRESHOLDS:
        if changed_lines <= limit:
            return label
    return "size/XL"

def triage_issue(title: str, body: str = "") -> TriagePlan:
    plan = TriagePlan()
    found = labels_for_text(title, body)
    plan.labels = sorted(found)
    plan.reasons = found
    # needs-info: body too short to act on (and not a question)
    if len((body or "").strip()) < 20 and "question" not in found:
        plan.needs_info = True
        if "needs-info" not in plan.labels:
            plan.labels.append("needs-info")
    return plan

def triage_pr(title: str, files: list[str], changed_lines: int) -> TriagePlan:
    plan = TriagePlan()
    found = labels_for_text(title) | labels_for_files(files)
    plan.reasons = found
    labels = sorted(found)
    labels.append(size_label(changed_lines))
    plan.labels = labels
    return plan
