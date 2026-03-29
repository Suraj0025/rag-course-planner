from langchain_community.llms import HuggingFacePipeline
from transformers import pipeline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from rag.vectorstore import load_vectorstore, get_retriever

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

def build_rag_chain(prompt_template, k=6):
    vs = load_vectorstore()
    retriever = get_retriever(vs, k=k)

    pipe = pipeline(
        "text-generation",
        model="google/flan-t5-base",
        max_new_tokens=256,
        do_sample=False
    )

    llm = HuggingFacePipeline(pipeline=pipe)

    prompt = ChatPromptTemplate.from_template(prompt_template)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain