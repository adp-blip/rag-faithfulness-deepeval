"""Two answer pipelines over the same retriever, so the eval can compare prompts."""
from .llm import chat
from .retriever import BM25, load_chunks

NAIVE_PROMPT = """Use the context to answer the question.

Context:
{context}

Question: {question}"""

GROUNDED_PROMPT = """You answer questions about the Lumen Labs employee handbook.

Rules:
- Use ONLY the context below. Do not use outside knowledge or guess.
- After each sentence, cite the source in square brackets, e.g. [pto].
- If the context does not contain the answer, reply exactly: "The handbook doesn't cover this." and nothing else.
- Keep it to 1-3 sentences.

Context:
{context}

Question: {question}"""

PROMPTS = {"naive": NAIVE_PROMPT, "grounded": GROUNDED_PROMPT}

_index = None


def index():
    global _index
    if _index is None:
        _index = BM25(load_chunks())
    return _index


def answer(question, variant="grounded", model="groq:openai/gpt-oss-20b", k=3):
    hits = index().search(question, k=k)
    context = "\n".join(f"[{c.doc_id}] {c.text}" for c in hits)
    prompt = PROMPTS[variant].format(context=context, question=question)
    reply = chat(model, [{"role": "user", "content": prompt}], max_tokens=1024)
    return reply, [f"[{c.doc_id}] {c.text}" for c in hits]
