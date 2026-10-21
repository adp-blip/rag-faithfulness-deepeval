# Results

Average score per metric, pass count in brackets. Unanswerable questions are only scored on faithfulness, abstention and citations. Citations are only scored for the grounded prompt (the naive prompt doesn't ask for them).

| run | faithfulness | answer_relevancy | contextual_recall | abstention | citations | cases fully passed |
|---|---|---|---|---|---|---|
| `naive__openai_gpt-oss-20b` | 1.00 (16/16) | 0.97 (11/12) | 0.96 (11/12) | 0.91 (15/16) | - | **13/16** |

## By question type

| run | type | passed |
|---|---|---|
| `naive__openai_gpt-oss-20b` | single | 8/9 |
| `naive__openai_gpt-oss-20b` | multi_hop | 2/3 |
| `naive__openai_gpt-oss-20b` | unanswerable | 3/4 |

## Failures

- `naive__openai_gpt-oss-20b` **q04** Can I fly premium economy to a conference in Singapore? The flight is 13 hours.
  - failed: answer_relevancy (The score is 0.60 because the response included unrelated details about budget sources and learning budget, which do not address the user's )
  - answer: 'Yes – because the flight is 13\u202fhours long, premium‑economy is allowed under the travel policy. Since conference travel is paid from the travel budget (not the learning budget), you can book premium‑economy for that leg.'
- `naive__openai_gpt-oss-20b` **q09** I want to buy a 350 EUR online course. Do I need approval, and does it come out of my home office stipend?
  - failed: contextual_recall (The score is 0.50 because sentence 1 aligns with node 3 in the retrieval context, while sentence 2 has no supporting node.)
  - answer: 'Yes – because the course costs €350, it exceeds the €300 threshold for learning purchases, so you’ll need your manager’s approval before you buy it.\n\nAnd no, it won’t be deducted from the €400 home‑office stipend. The st'
- `naive__openai_gpt-oss-20b` **q16** How many PTO days do contractors get?
  - failed: abstention (The expected output requires stating that the handbook doesn't cover the question, but the actual output provides a definitive answer that c)
  - answer: 'The policy only specifies PTO for full‑time and part‑time employees. Contractors are not covered by the PTO provision, so they do not receive any paid time off under this policy.'
