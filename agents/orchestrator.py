from rag.vectorstore import load_vectorstore
from agents.agents import IntakeAgent, RetrieverAgent, PlannerAgent, VerifierAgent

def run_pipeline(query):
    vs = load_vectorstore()

    intake = IntakeAgent()
    retriever = RetrieverAgent(vs)
    planner = PlannerAgent()
    verifier = VerifierAgent()

    profile = intake.run(query)

    context = retriever.run(query)

    if not context:
        return {"raw_output": "I don't have that information in the provided catalog."}

    result = planner.run(context, query)

    if not verifier.run(result):
        return {"raw_output": "Response failed validation."}

    return {"raw_output": result}