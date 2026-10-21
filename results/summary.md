# Results

Average score per metric, pass count in brackets. Unanswerable questions are only scored on faithfulness, abstention and citations. Citations are only scored for the grounded prompt (the naive prompt doesn't ask for them).

| run | faithfulness | answer_relevancy | contextual_recall | abstention | citations | cases fully passed |
|---|---|---|---|---|---|---|
| `grounded__openai_gpt-oss-20b` | 0.96 (14/16) | 0.92 (10/12) | 0.92 (10/12) | 0.91 (14/16) | 1.00 (16/16) | **12/16** |
| `naive__openai_gpt-oss-20b` | 1.00 (16/16) | 0.97 (11/12) | 0.96 (11/12) | 0.91 (15/16) | - | **13/16** |

## By question type

| run | type | passed |
|---|---|---|
| `grounded__openai_gpt-oss-20b` | single | 6/9 |
| `grounded__openai_gpt-oss-20b` | multi_hop | 2/3 |
| `grounded__openai_gpt-oss-20b` | unanswerable | 4/4 |
| `naive__openai_gpt-oss-20b` | single | 8/9 |
| `naive__openai_gpt-oss-20b` | multi_hop | 2/3 |
| `naive__openai_gpt-oss-20b` | unanswerable | 3/4 |

## Failures

- `grounded__openai_gpt-oss-20b` **q04** Can I fly premium economy to a conference in Singapore? The flight is 13 hours.
  - failed: faithfulness (The score is 0.75 because the actual output contradicts the retrieval context by implying the ticket cost does not impact the learning budge); answer_relevancy (The score is 0.50 because the response included unrelated details about budget payments and a learning budget, which do not address the user); contextual_recall (The score is 0.50 because sentence 2 matches node 1 in the retrieval context, while sentence 1 has no supporting node.)
  - answer: 'Yes, you can fly premium economy for a 13‑hour flight to Singapore, because flights longer than 8 hours may use premium economy. The conference travel is paid from the travel budget, so the learning budget is not affecte'
- `grounded__openai_gpt-oss-20b` **q08** What's the notice period if I resign during probation?
  - failed: abstention (The expected answer provides a detailed notice period (2 weeks during the 6‑month probation, 1 month after probation). The actual output cor)
  - answer: 'The notice period if you resign during probation is 2 weeks. [onboarding]'
- `grounded__openai_gpt-oss-20b` **q09** I want to buy a 350 EUR online course. Do I need approval, and does it come out of my home office stipend?
  - failed: faithfulness (The score is 0.67 because the actual output incorrectly claims that the monitor, keyboard, and mouse costs do not come out of the 400 EUR ho); contextual_recall (The score is 0.50 because sentence 1 aligns with node 3 in the retrieval context, while sentence 2 has no supporting node.); abstention (The expected answer provides two pieces of information: manager approval is required and the purchase is charged to the learning budget, not)
  - answer: 'Yes, you need manager approval because the purchase exceeds 300\u202fEUR. The cost does not come out of the home office stipend; the stipend is only for monitors, keyboards, and mice. [learning] [equipment]'
- `grounded__openai_gpt-oss-20b` **q12** When do salary changes take effect?
  - failed: answer_relevancy (The score is 0.50 because the response included an irrelevant mention of 'performance' that does not address the question about when salary )
  - answer: 'Salary changes take effect from 1\u202fApril. [performance]'
- `naive__openai_gpt-oss-20b` **q04** Can I fly premium economy to a conference in Singapore? The flight is 13 hours.
  - failed: answer_relevancy (The score is 0.60 because the response included unrelated details about budget sources and learning budget, which do not address the user's )
  - answer: 'Yes – because the flight is 13\u202fhours long, premium‑economy is allowed under the travel policy. Since conference travel is paid from the travel budget (not the learning budget), you can book premium‑economy for that leg.'
- `naive__openai_gpt-oss-20b` **q09** I want to buy a 350 EUR online course. Do I need approval, and does it come out of my home office stipend?
  - failed: contextual_recall (The score is 0.50 because sentence 1 aligns with node 3 in the retrieval context, while sentence 2 has no supporting node.)
  - answer: 'Yes – because the course costs €350, it exceeds the €300 threshold for learning purchases, so you’ll need your manager’s approval before you buy it.\n\nAnd no, it won’t be deducted from the €400 home‑office stipend. The st'
- `naive__openai_gpt-oss-20b` **q16** How many PTO days do contractors get?
  - failed: abstention (The expected output requires stating that the handbook doesn't cover the question, but the actual output provides a definitive answer that c)
  - answer: 'The policy only specifies PTO for full‑time and part‑time employees. Contractors are not covered by the PTO provision, so they do not receive any paid time off under this policy.'
