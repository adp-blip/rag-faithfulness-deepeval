"""Run both RAG variants over the golden set and score them with deepeval.

    python run_eval.py                         # defaults
    python run_eval.py --model groq:qwen/qwen3.8-27b --variants grounded
"""
import argparse
import json
import os
from pathlib import Path

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")

from deepeval.metrics import (AnswerRelevancyMetric, ContextualRecallMetric,
                              FaithfulnessMetric, GEval)
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

import report
from ragkit.judge import GroqJudge
from ragkit.metrics import CitationMetric
from ragkit.pipeline import answer


def build_metrics(judge):
    abstain = GEval(
        name="Abstention",
        model=judge,
        threshold=0.7,
        async_mode=False,
        evaluation_steps=[
            "If the expected output says the handbook doesn't cover this, the actual output must clearly say the "
            "information isn't available and must NOT give a concrete answer, number or policy.",
            "If the expected output contains a real answer, the actual output must give that answer and must not "
            "claim the handbook doesn't cover it.",
            "Ignore citation brackets and wording differences.",
        ],
        evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT,
                           LLMTestCaseParams.EXPECTED_OUTPUT],
    )
    return {
        "faithfulness": FaithfulnessMetric(threshold=0.8, model=judge, async_mode=False),
        "answer_relevancy": AnswerRelevancyMetric(threshold=0.7, model=judge, async_mode=False),
        "contextual_recall": ContextualRecallMetric(threshold=0.7, model=judge, async_mode=False),
        "abstention": abstain,
        "citations": CitationMetric(),
    }


def applicable(metric_name, case):
    # recall and relevancy are meaningless when the right answer is "not in the handbook"
    if case["type"] == "unanswerable":
        return metric_name in ("faithfulness", "abstention", "citations")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="groq:openai/gpt-oss-20b")
    ap.add_argument("--judge", default="groq:openai/gpt-oss-120b")
    ap.add_argument("--variants", nargs="+", default=["naive", "grounded"])
    ap.add_argument("--only", nargs="*")
    args = ap.parse_args()

    golden = json.loads(Path("data/golden.json").read_text(encoding="utf-8"))
    if args.only:
        golden = [g for g in golden if g["id"] in args.only]
    metrics = build_metrics(GroqJudge(args.judge))
    out = Path("results")
    out.mkdir(exist_ok=True)

    for variant in args.variants:
        rows = []
        print(f"\n== {variant} / {args.model}")
        for g in golden:
            reply, ctx = answer(g["input"], variant=variant, model=args.model)
            tc = LLMTestCase(input=g["input"], actual_output=reply,
                             expected_output=g["expected_output"], retrieval_context=ctx)
            scores = {}
            for name, m in metrics.items():
                if not applicable(name, g):
                    continue
                try:
                    m.measure(tc)
                    scores[name] = {"score": round(m.score, 3), "pass": bool(m.is_successful()),
                                    "reason": m.reason}
                except Exception as e:  # one flaky judge call shouldn't sink the whole run
                    scores[name] = {"score": None, "pass": False, "reason": f"error: {e}"}
            ok = all(s["pass"] for k, s in scores.items() if not (k == "citations" and variant == "naive"))
            print(f"  {'PASS' if ok else 'FAIL'} {g['id']} "
                  + " ".join(f"{k[:5]}={v['score']}" for k, v in scores.items()))
            rows.append({**g, "variant": variant, "model": args.model, "actual_output": reply,
                         "retrieved": [c.split("]")[0][1:] for c in ctx], "scores": scores, "passed": ok})
        name = f"{variant}__{args.model.split(':')[-1].replace('/', '_')}.json"
        (out / name).write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")

    report.main()


if __name__ == "__main__":
    main()
