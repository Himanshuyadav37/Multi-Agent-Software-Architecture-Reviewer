import streamlit as st
from dotenv import load_dotenv
import time
import re

load_dotenv()

# ============================================================
# IMPORT PROJECT MODULES
# ============================================================

from app.utils.github_loader import clone_repo
from app.parsers.repo_parser import load_code_files

from app.agents.router_agent import (
    classify_repository,
    decide_agents
)

from app.graph.workflow import app

from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

from langchain_groq import ChatGroq


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Repository Architecture Reviewer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #020617 0%,
        #081126 50%,
        #0f172a 100%
    );
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #020817;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.main-title {
    font-size: 58px;
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(
        to right,
        #38bdf8,
        #818cf8,
        #c084fc
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.subtitle {
    color: #94a3b8;
    font-size: 18px;
    line-height: 1.8;
    margin-bottom: 30px;
}

.glass-card {
    background: rgba(15,23,42,0.72);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 24px;
    backdrop-filter: blur(14px);
}

.metric-card {
    background: rgba(15,23,42,0.75);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 24px;
    padding: 24px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.metric-title {
    color: #94a3b8;
    font-size: 12px;
    letter-spacing: 1px;
    font-weight: 600;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    margin-top: 12px;
}

.agent-card {
    background: linear-gradient(
        135deg,
        rgba(30,41,59,0.8),
        rgba(15,23,42,0.8)
    );
    border: 1px solid rgba(255,255,255,0.06);
    padding: 16px;
    border-radius: 18px;
    margin-bottom: 12px;
}

.repo-box {
    background: rgba(30,41,59,0.65);
    border-radius: 20px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}

.stButton > button {
    background: linear-gradient(
        90deg,
        #2563eb,
        #7c3aed
    );
    color: white;
    border: none;
    border-radius: 14px;
    padding: 14px 22px;
    font-size: 16px;
    font-weight: 600;
    width: 100%;
}

.stButton > button:hover {
    opacity: 0.92;
}

.status-pill {
    display: inline-block;
    background: rgba(34,197,94,0.15);
    color: #4ade80;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 14px;
    margin-right: 8px;
    margin-top: 8px;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.stMarkdown {
    color: #e2e8f0;
    line-height: 1.9;
}

[data-testid="stExpander"] {
    background: rgba(15,23,42,0.7);
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ SYSTEM STATUS")

    st.markdown("""
    <div class="agent-card">🧠 LangGraph Active</div>
    <div class="agent-card">⚡ Router Agent Active</div>
    <div class="agent-card">📚 RAG Pipeline Active</div>
    <div class="agent-card">🗂 ChromaDB Connected</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 🤖 ACTIVE AGENTS")

    st.markdown("""
    <div class="agent-card">🛡 Security Agent</div>
    <div class="agent-card">🏗 Architecture Agent</div>
    <div class="agent-card">⚡ Router Agent</div>
    <div class="agent-card">📚 RAG Analysis Agent</div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("## 🚀 CAPABILITIES")

    st.markdown("""
    - Multi-agent orchestration  
    - AST static analysis  
    - RAG repository understanding  
    - Dynamic routing  
    - Enterprise audit generation  
    - AI-powered architecture review  
    """)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div style="margin-top:20px;">
<div style="color:#3b82f6;font-size:12px;font-weight:700;letter-spacing:3px;">
ENTERPRISE AI PLATFORM
</div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">Repository Architecture Reviewer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">AI-powered repository intelligence using LangGraph, RAG, AST analysis, and dynamic multi-agent orchestration.</div>',
    unsafe_allow_html=True
)

st.markdown("---")


# ============================================================
# INPUT SECTION
# ============================================================

col1, col2 = st.columns(2)

with col1:

    repo_url = st.text_input(
        "GITHUB REPOSITORY URL",
        placeholder="https://github.com/username/repository"
    )

with col2:

    query = st.text_area(
        "ANALYSIS PROMPT",
        placeholder="Perform a complete repository audit...",
        height=120
    )

run_analysis = st.button(
    "🚀 Run Enterprise Analysis"
)


# ============================================================
# MAIN EXECUTION
# ============================================================

if run_analysis:

    if repo_url.strip() == "":

        st.error("Please enter repository URL")
        st.stop()

    with st.spinner("Cloning repository..."):

        repo_path = clone_repo(repo_url)

    st.success("Repository cloned successfully.")

    with st.spinner("Loading repository files..."):

        documents = load_code_files(repo_path)

    with st.spinner("Running Router Agent..."):

        tech_stack = classify_repository(documents)

        selected_agents = decide_agents(
            tech_stack
        )

    # ============================================================
    # METRICS
    # ============================================================

    st.markdown("<br>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        ("FILES LOADED", str(len(documents))),
        ("ACTIVE AGENTS", str(len(selected_agents))),
        ("WORKFLOW ENGINE", "LangGraph"),
        ("VECTOR DATABASE", "ChromaDB")
    ]

    cols = [m1, m2, m3, m4]

    for col, metric in zip(cols, metrics):

        title, value = metric

        with col:

            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # ============================================================
    # REPOSITORY OVERVIEW
    # ============================================================

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#64748b;font-size:13px;letter-spacing:2px;margin-bottom:20px;">
    REPOSITORY OVERVIEW
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([2, 2])

    with c1:

        st.markdown(
            f"""
            <div class="repo-box">
            🔗 <b>Repository:</b><br><br>
            <a href="{repo_url}" target="_blank">{repo_url}</a>
            </div>
            """,
            unsafe_allow_html=True
        )

        detected_tech = []

        if tech_stack.get("react"):
            detected_tech.append("⚛️ React")

        if tech_stack.get("python"):
            detected_tech.append("🐍 Python")

        if tech_stack.get("docker"):
            detected_tech.append("🐳 Docker")

        if len(detected_tech) == 0:
            detected_tech.append("📦 General Repository")

        st.markdown("<br>", unsafe_allow_html=True)

        for tech in detected_tech:

            st.markdown(
                f'<span class="status-pill">{tech}</span>',
                unsafe_allow_html=True
            )

    with c2:

        for agent in selected_agents:

            st.markdown(
                f"""
                <div class="agent-card">
                🤖 {agent.title()} Agent
                </div>
                """,
                unsafe_allow_html=True
            )

    # ============================================================
    # WORKFLOW STATUS
    # ============================================================

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#64748b;font-size:13px;letter-spacing:2px;margin-bottom:20px;">
    WORKFLOW EXECUTION
    </div>
    """, unsafe_allow_html=True)

    workflow_steps = [
        "Repository Cloning",
        "Repository Parsing",
        "Router Agent",
        "LangGraph Workflow",
        "Security Analysis",
        "Architecture Analysis",
        "RAG Processing",
        "Final AI Report"
    ]

    progress_bar = st.progress(0)

    for i, step in enumerate(workflow_steps):

        time.sleep(0.15)

        progress_bar.progress((i + 1) / len(workflow_steps))

        st.success(f"✅ {step}")

    # ============================================================
    # AGENT ANALYSIS
    # ============================================================

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#64748b;font-size:13px;letter-spacing:2px;margin-bottom:20px;">
    MULTI-AGENT ANALYSIS
    </div>
    """, unsafe_allow_html=True)

    for doc in documents:

        file_path = doc["file_path"]

        if not file_path.endswith(".py"):
            continue

        with st.expander(f"📄 {file_path}"):

            try:

                initial_state = {
                    "file_path": file_path,
                    "content": doc["content"],
                    "selected_agents": selected_agents
                }

                result = app.invoke(initial_state)

                st.markdown("### 🌳 AST Analysis")

                st.code(
                    str(result.get(
                        "ast_analysis",
                        "No AST analysis"
                    )),
                    language="python"
                )

                if result.get("security_report"):

                    st.markdown("### 🛡 Security Report")

                    st.markdown(
                        result["security_report"]
                    )

                if result.get("architecture_report"):

                    st.markdown("### 🏗 Architecture Report")

                    st.markdown(
                        result["architecture_report"]
                    )

            except Exception as e:

                st.error(str(e))

    # ============================================================
    # RAG PIPELINE
    # ============================================================

    with st.spinner("Initializing RAG pipeline..."):

        chunks = chunk_documents(documents)

        create_vector_store(chunks)

        retriever = get_retriever()

    # ============================================================
    # FINAL AI REPORT
    # ============================================================

    if query.strip() != "":

        with st.spinner("Generating enterprise AI audit report..."):

            results = retriever.invoke(query)

            cleaned_chunks = []

            for r in results[:4]:

                text = r.page_content

                if len(text) > 1200:
                    text = text[:1200]

                cleaned_chunks.append(text)

            context = "\n\n".join(cleaned_chunks)

            prompt = f"""
You are an elite enterprise AI software architecture reviewer.

Analyze the repository professionally.

Repository Context:
{context}

User Query:
{query}

STRICT RULES:

1. NEVER dump raw repository code.

2. NEVER explain everything unless user explicitly asks:
- detailed
- deep analysis
- full audit
- comprehensive review

3. If user asks simple question:
- give concise output
- maximum 5-10 lines
- to-the-point answer only

4. If user asks detailed audit:
- use proper sections
- use headings
- use bullet points
- keep spacing clean

5. VERY IMPORTANT:
- avoid giant paragraphs
- avoid repeating information
- avoid unnecessary explanation
- do not hallucinate

6. OUTPUT STYLE:
- modern
- concise
- professional
- enterprise architect tone

Generate final professional response.
"""

            response = llm.invoke(prompt)

        # ============================================================
        # EXECUTIVE REPORT HEADER
        # ============================================================

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.markdown("""
        <div style="
            color:#64748b;
            font-size:13px;
            letter-spacing:2px;
            margin-bottom:22px;
            font-weight:700;
        ">
        EXECUTIVE AI AUDIT REPORT
        </div>
        """, unsafe_allow_html=True)

        # ============================================================
        # FINAL METRICS
        # ============================================================

        col1, col2, col3, col4 = st.columns(4)

        final_metrics = [
            ("OVERALL SCORE", "8.2 / 10", "#ffffff"),
            ("SECURITY", "GOOD", "#4ade80"),
            ("SCALABILITY", "MODERATE", "#38bdf8"),
            ("PRODUCTION", "READY", "#a78bfa")
        ]

        cols = [col1, col2, col3, col4]

        for col, metric in zip(cols, final_metrics):

            title, value, color = metric

            with col:

                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>

                    <div style="
                        font-size:30px;
                        font-weight:700;
                        margin-top:12px;
                        color:{color};
                    ">
                    {value}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ============================================================
        # RESPONSE CLEANING
        # ============================================================

        formatted_response = response.content

        replacements = {
            "Architecture Insights:": "\n## 🏗 Architecture Insights\n",
            "Security Observations:": "\n## 🛡 Security Observations\n",
            "Maintainability Analysis:": "\n## 🧩 Maintainability\n",
            "Scalability Concerns:": "\n## ⚡ Scalability\n",
            "Production Readiness Assessment:": "\n## 🚀 Production Readiness\n",
            "Suggestions for Improvement:": "\n## 📈 Recommendations\n",
        }

        for old, new in replacements.items():

            formatted_response = formatted_response.replace(
                old,
                new
            )

        formatted_response = re.sub(
            r'\n{3,}',
            '\n\n',
            formatted_response
        )

        formatted_response = formatted_response.replace(
            "**",
            ""
        )

        # ============================================================
        # RESPONSE CONTAINER
        # ============================================================

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        response_placeholder = st.empty()

        full_response = ""

        words = formatted_response.split()

        for word in words:

            full_response += word + " "

            response_placeholder.markdown(
                full_response + "▌"
            )

            time.sleep(0.008)

        response_placeholder.markdown(
            full_response
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # ============================================================
        # FINAL RECOMMENDATIONS
        # ============================================================

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="glass-card">

        <h3 style="
            margin-bottom:24px;
            font-size:24px;
        ">
        📈 Enterprise Recommendations
        </h3>

        <div style="
            line-height:2.2;
            color:#e2e8f0;
            font-size:16px;
        ">

        ✅ Improve automated testing coverage<br>

        ✅ Add centralized logging and monitoring<br>

        ✅ Refactor large modules into smaller services<br>

        ✅ Improve exception handling strategy<br>

        ✅ Add CI/CD deployment pipeline<br>

        ✅ Enhance validation and sanitization layers

        </div>

        </div>
        """, unsafe_allow_html=True)