"""Builds results/summary.md from the per-run JSON files."""
import json
from pathlib import Path

METRICS = ["faithfulness", "answer_relevancy", "contextual_recall", "abstention", "citations"]


def main():
    files = sorted(Path("results").glob("*.json"))
    lines = ["# Results", "",
             "Average score per metric, pass count in brackets. Unanswerable questions are only scored on "
             "faithfulness, abstention and citations.", "",
             "| run | " + " | ".join(METRICS) + " | cases fully passed |",
             "|---" * (len(METRICS) + 2) + "|"]
    by_type = []
    for f in files:
        rows = json.loads(f.read_text(encoding="utf-8"))
        cells = []
        for m in METRICS:
            vals = [r["scores"][m] for r in rows if m in r["scores"] and r["scores"][m]["score"] is not None]
            if not vals:
                cells.append("-")
                continue
            avg = sum(v["score"] for v in vals) / len(vals)
            cells.append(f"{avg:.2f} ({sum(v['pass'] for v in vals)}/{len(vals)})")
        passed = sum(r["passed"] for r in rows)
        lines.append(f"| `{f.stem}` | " + " | ".join(cells) + f" | **{passed}/{len(rows)}** |")
        for t in ("single", "multi_hop", "unanswerable"):
            xs = [r for r in rows if r["type"] == t]
            if xs:
                by_type.append((f.stem, t, sum(r["passed"] for r in xs), len(xs)))

    lines += ["", "## By question type", "", "| run | type | passed |", "|---|---|---|"]
    lines += [f"| `{run}` | {t} | {p}/{n} |" for run, t, p, n in by_type]

    lines += ["", "## Failures", ""]
    for f in files:
        for r in json.loads(f.read_text(encoding="utf-8")):
            if r["passed"]:
                continue
            failed = [f"{k} ({(v['reason'] or '')[:140]})" for k, v in r["scores"].items() if not v["pass"]]
            lines.append(f"- `{f.stem}` **{r['id']}** {r['input']}")
            lines.append("  - failed: " + "; ".join(failed))
            lines.append(f"  - answer: {r['actual_output'][:220]!r}")
    Path("results/summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote results/summary.md")


if __name__ == "__main__":
    main()
