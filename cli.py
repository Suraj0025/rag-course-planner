from agents.orchestrator import run_pipeline

query = input("Enter your question: ")

result = run_pipeline(query)

print("\nRESULT:\n")
print(result["raw_output"])