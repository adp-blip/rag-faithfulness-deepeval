"""Lets deepeval use a Groq model as the judge instead of OpenAI."""
import json
import re

from deepeval.models import DeepEvalBaseLLM

from .llm import chat


class GroqJudge(DeepEvalBaseLLM):
    def __init__(self, model="groq:openai/gpt-oss-120b"):
        self.model_id = model
        super().__init__(model)

    def load_model(self):
        return self.model_id

    def generate(self, prompt, schema=None):
        if schema is not None:
            prompt += "\n\nReturn only valid JSON, no markdown fences."
        text = chat(self.model_id, [{"role": "user", "content": prompt}], max_tokens=2048)
        if schema is None:
            return text
        m = re.search(r"\{.*\}", text, re.DOTALL)
        raw = m.group(0) if m else text
        try:
            return schema.model_validate(json.loads(raw))
        except Exception:
            return raw  # deepeval falls back to its own lenient JSON parsing

    async def a_generate(self, prompt, schema=None):
        return self.generate(prompt, schema)

    def get_model_name(self):
        return self.model_id
