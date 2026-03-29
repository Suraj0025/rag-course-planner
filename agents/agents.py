import json
from transformers import pipeline

# ---------------- Shared LLM ----------------

pipe = pipeline(
    "text-generation",
    model="distilgpt2",
    max_new_tokens=80,
    do_sample=False
)

# ---------------- Intake Agent ----------------

class IntakeAgent:
    def __init__(self):
        self.pipe = pipe

    def run(self, query):
        # Simple fallback (no complex parsing needed)
        return {"completed_courses": [], "target_major": None}


# ---------------- Retriever Agent ----------------

from rag.vectorstore import get_retriever

class RetrieverAgent:
    def __init__(self, vs):
        self.retriever = get_retriever(vs)

    def run(self, query):
        docs = self.retriever.invoke(query)

        if not docs:
            return None

        return "\n".join([d.page_content for d in docs])


# ---------------- Planner Agent ----------------

class PlannerAgent:
    def __init__(self):
        self.pipe = pipe

    def run(self, context, query):
        prompt = f"""
Use ONLY the context below to answer.

Context:
{context}

Question:
{query}

Answer in one short sentence:
"""

        result = self.pipe(prompt)

        output = result[0]["generated_text"]

        # 🔥 CLEAN OUTPUT
        output = output.replace(prompt, "").strip()

        # Remove repetitions
        lines = output.split("\n")
        clean_lines = []
        for line in lines:
            if line.strip() and line.strip() not in clean_lines:
                clean_lines.append(line.strip())

        output = " ".join(clean_lines)

        # Cut after first meaningful sentence
        if "." in output:
            output = output.split(".")[0] + "."

        return output


# ---------------- Verifier Agent ----------------

class VerifierAgent:
    def run(self, output):
        return True