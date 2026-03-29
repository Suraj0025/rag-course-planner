## Sample Run

Input:
What are prerequisites for CS301?

Output:
CS301 requires CS101 and MATH120.

## Architecture

1. Documents are ingested and chunked
2. Stored in FAISS vector database
3. Retriever fetches relevant chunks
4. Planner Agent generates answer using context
5. System returns final response via CLI

## Challenges Faced

- Handled LangChain breaking changes (schema, prompts, runnables)
- Resolved HuggingFace model compatibility issues
- Improved output quality with prompt engineering and post-processing
   
