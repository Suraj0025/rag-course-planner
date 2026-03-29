import streamlit as st
from agents.orchestrator import run_pipeline

st.set_page_config(page_title="Course Planner AI")

st.title("RAG Course Planning Assistant")

query = st.text_input("Enter your question:")

if st.button("Get Answer"):
    if query:
        result = run_pipeline(query)
        st.success(result["raw_output"])
    else:
        st.warning("Please enter a question.")