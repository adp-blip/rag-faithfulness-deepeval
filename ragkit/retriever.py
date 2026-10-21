"""BM25 over paragraph chunks. Small enough to read in one go, good enough for a 10-doc handbook."""
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

STOP = set("a an the of to in for on and or is are be it you your we our with at by as this that "
           "from can do does how what when which who much many i my me".split())


def tokenize(text):
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


@dataclass
class Chunk:
    doc_id: str
    text: str


def load_chunks(kb_dir="kb"):
    chunks = []
    for path in sorted(Path(kb_dir).glob("*.md")):
        paras = [p.strip() for p in path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
        title = paras[0].lstrip("# ").strip()
        for p in paras[1:]:
            # keep the doc title on every chunk so "PTO" questions still hit PTO paragraphs
            chunks.append(Chunk(path.stem, f"{title}: {p}"))
    return chunks


class BM25:
    def __init__(self, chunks, k1=1.5, b=0.75):
        self.chunks = chunks
        self.docs = [tokenize(c.text) for c in chunks]
        self.k1, self.b = k1, b
        self.avgdl = sum(map(len, self.docs)) / len(self.docs)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def score(self, query_tokens, doc):
        tf = Counter(doc)
        s = 0.0
        for t in query_tokens:
            if t not in tf:
                continue
            f = tf[t]
            s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avgdl))
        return s

    def search(self, query, k=3):
        q = tokenize(query)
        ranked = sorted(range(len(self.docs)), key=lambda i: self.score(q, self.docs[i]), reverse=True)
        return [self.chunks[i] for i in ranked[:k]]
