from dotenv import load_dotenv
load_dotenv()

# =========================================
# Imports
# =========================================

from app.utils.github_loader import clone_repo
from app.parsers.repo_parser import load_code_files

from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

from app.graph.workflow import app
from app.agents.router_agent import (
    classify_repository,
    decide_agents
)

from langchain_groq import ChatGroq


# =========================================
# LLM
# =========================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)


# =========================================
# GitHub Repo Input
# =========================================

repo_url = input("Enter GitHub Repo URL: ")

repo_path = clone_repo(repo_url)


# =========================================
# Load Repository Files
# =========================================

documents = load_code_files(repo_path)

# =========================================
# ROUTER AGENT
# =========================================

tech_stack = classify_repository(
    documents
)

selected_agents = decide_agents(
    tech_stack
)

print("\n===== ROUTER OUTPUT =====")
print(selected_agents)

# =========================================
# MULTI-AGENT ANALYSIS
# =========================================

print("\n===== MULTI-AGENT CODE ANALYSIS =====\n")

for doc in documents:

    file_path = doc["file_path"]

    # Analyze only Python files
    if not file_path.endswith(".py"):
        continue

    print("\n===================================")
    print("FILE:")
    print(file_path)

    try:

        # =========================================
        # INITIAL GRAPH STATE
        # =========================================

        initial_state = {
    "file_path": file_path,
    "content": doc["content"],
    "selected_agents": selected_agents
}

        # =========================================
        # RUN LANGGRAPH WORKFLOW
        # =========================================

        result = app.invoke(initial_state)

        # =========================================
        # PRINT AST ANALYSIS
        # =========================================

        print("\n===== AST ANALYSIS =====")
        print(result["ast_analysis"])

        # =========================================
        # PRINT SECURITY REPORT
        # =========================================

        print("\n===== SECURITY REPORT =====")
        print(result["security_report"])

        # =========================================
        # PRINT COMPLEXITY DATA
        # =========================================

        print("\n===== COMPLEXITY ANALYSIS =====")
        print(result["complexity_data"])

        # =========================================
        # PRINT ARCHITECTURE REPORT
        # =========================================

        print("\n===== ARCHITECTURE REPORT =====")
        print(result["architecture_report"])

    except Exception as e:

        print("\nWorkflow Error:")
        print(e)


# =========================================
# RAG PIPELINE
# =========================================

chunks = chunk_documents(documents)

create_vector_store(chunks)

retriever = get_retriever()


# =========================================
# USER QUERY
# =========================================

query = input("\nAsk Question About Codebase: ")


# =========================================
# RETRIEVE RELEVANT CHUNKS
# =========================================

results = retriever.invoke(query)

print("\n===== RETRIEVED RESULTS =====\n")


# =========================================
# CONTEXT CREATION
# =========================================

context = "\n\n".join(
    [r.page_content[:500] for r in results[:3]]
)


# =========================================
# AI PROMPT
# =========================================

prompt = f"""
You are an expert AI software architecture reviewer.

Use the repository context below to answer the question.

Repository Context:
{context}

Question:
{query}

Provide:
- technical explanation
- architecture insights
- maintainability observations
- concise professional answer
"""


# =========================================
# GENERATE AI RESPONSE
# =========================================

try:

    response = llm.invoke(prompt)

    print("\n===== AI ANSWER =====\n")
    print(response.content)

except Exception as e:

    print("\nLLM Error:")
    print(e) 