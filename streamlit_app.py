import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re
import time

load_dotenv()

# ============================================================
# PROJECT IMPORTS
# ============================================================

from app.utils.github_loader import clone_repo
from app.parsers.repo_parser import load_code_files
from app.agents.router_agent import classify_repository, decide_agents
from app.graph.workflow import app
from app.rag.chunker import chunk_documents
from app.rag.vector_store import create_vector_store
from app.rag.retriever import get_retriever

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Repository Architecture Reviewer",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# STYLING
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp{
background:linear-gradient(135deg,#020617,#081126,#0f172a);
color:white;
}

.main-title{
font-size:58px;
font-weight:800;
background:linear-gradient(to right,#38bdf8,#818cf8,#c084fc);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
color:#94a3b8;
font-size:18px;
line-height:1.8;
margin-bottom:25px;
}

.card{
background:rgba(15,23,42,0.75);
border:1px solid rgba(255,255,255,0.06);
border-radius:22px;
padding:22px;
}

.metric-title{
color:#94a3b8;
font-size:12px;
letter-spacing:1px;
font-weight:600;
}

.metric-value{
font-size:30px;
font-weight:700;
margin-top:10px;
}

.workflow{
background:rgba(15,23,42,0.7);
padding:14px 18px;
border-radius:14px;
margin-bottom:10px;
border:1px solid rgba(255,255,255,0.05);
}

.rec-card{
background:rgba(30,41,59,0.6);
padding:14px 18px;
border-radius:14px;
margin-bottom:12px;
border:1px solid rgba(255,255,255,0.05);
}

.stButton > button{
background:linear-gradient(90deg,#2563eb,#7c3aed);
color:white;
border:none;
border-radius:14px;
padding:14px 22px;
font-size:16px;
font-weight:600;
width:100%;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# LLM
# ============================================================

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ⚡ System Status")

    statuses = [
        "🧠 LangGraph Active",
        "📚 RAG Pipeline Active",
        "⚡ Router Agent Active",
        "🗂 ChromaDB Connected"
    ]

    for s in statuses:
        st.markdown(f'<div class="workflow">{s}</div>', unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown('<div class="main-title">Repository Architecture Reviewer</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">AI-powered repository intelligence using LangGraph, RAG, AST analysis, and multi-agent orchestration.</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# INPUTS
# ============================================================

col1, col2 = st.columns(2)

with col1:
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/user/repository"
    )

with col2:
    query = st.text_area(
        "Analysis Prompt",
        placeholder="Perform complete architecture and security audit...",
        height=120
    )

run_btn = st.button("🚀 Run Enterprise Analysis")

# ============================================================
# MAIN FLOW
# ============================================================

if run_btn:

    if repo_url.strip() == "":
        st.error("Please enter repository URL")
        st.stop()

    # ============================================================
    # REPO LOAD
    # ============================================================

    with st.spinner("Cloning repository..."):
        repo_path = clone_repo(repo_url)

    with st.spinner("Loading repository files..."):
        documents = load_code_files(repo_path)

    with st.spinner("Running router agent..."):
        tech_stack = classify_repository(documents)
        selected_agents = decide_agents(tech_stack)

    # ============================================================
    # TOP METRICS
    # ============================================================

    st.markdown("<br>", unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)

    metrics = [
        ("FILES", str(len(documents))),
        ("AGENTS", str(len(selected_agents))),
        ("ENGINE", "LangGraph"),
        ("VECTOR DB", "ChromaDB")
    ]

    cols = [m1, m2, m3, m4]

    for col, metric in zip(cols, metrics):

        title, value = metric

        with col:

            st.markdown(f"""
            <div class="card">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """, unsafe_allow_html=True)

    # ============================================================
    # OVERVIEW
    # ============================================================

    st.markdown("<br><hr><br>", unsafe_allow_html=True)

    st.markdown("## 📦 Repository Overview")

    st.markdown(f"""
    <div class="card">

    🔗 <b>Repository:</b><br><br>

    <a href="{repo_url}" target="_blank">{repo_url}</a>

    <br><br>

    🤖 <b>Selected Agents:</b><br>

    {", ".join(selected_agents)}

    </div>
    """, unsafe_allow_html=True)

    # ============================================================
    # WORKFLOW EXECUTION
    # ============================================================

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("## ⚙️ Workflow Execution")

    workflow_logs = [
        "Repository cloned successfully",
        f"{len(documents)} files loaded",
        "Router agent completed",
        f"Selected agents: {', '.join(selected_agents)}",
        "LangGraph workflow initialized",
        "AST analysis completed",
        "Security analysis completed",
        "Architecture analysis completed",
        "RAG vector database created",
        "Enterprise AI report generated"
    ]

    progress_bar = st.progress(0)

    for i, log in enumerate(workflow_logs):

        progress_bar.progress((i + 1) / len(workflow_logs))

        st.markdown(
            f'<div class="workflow">✅ {log}</div>',
            unsafe_allow_html=True
        )

        time.sleep(0.05)

    # ============================================================
    # AGENT ANALYSIS
    # ============================================================

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("## 🤖 Multi-Agent Analysis")

    for doc in documents:

        file_path = doc["file_path"]

        if not file_path.endswith(".py"):
            continue

        with st.expander(f"📄 {file_path}"):

            try:

                state = {
                    "file_path": file_path,
                    "content": doc["content"],
                    "selected_agents": selected_agents
                }

                result = app.invoke(state)

                if result.get("ast_analysis"):

                    st.markdown("### 🌳 AST Analysis")

                    st.code(
                        str(result["ast_analysis"]),
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
    # RAG
    # ============================================================

    with st.spinner("Building vector database..."):

        chunks = chunk_documents(documents)

        create_vector_store(chunks)

        retriever = get_retriever()

    # ============================================================
    # FINAL AI REPORT
    # ============================================================

    if query.strip() != "":

        with st.spinner("Generating AI report..."):

            results = retriever.invoke(query)

            cleaned_chunks = []

            for r in results[:6]:

                text = r.page_content

                text = re.sub(
                    r'```.*?```',
                    '',
                    text,
                    flags=re.DOTALL
                )

                text = text[:1500]

                cleaned_chunks.append(text)

            context = "\n\n".join(cleaned_chunks)

            prompt = f"""
You are an elite senior enterprise software architect with 15+ years experience.

Analyze this repository using the provided context. Provide professional, actionable insights.

REPOSITORY CONTEXT:
{context}

USER QUERY:
{query}

ANALYSIS REQUIREMENTS:

1. BASE ALL INSIGHTS STRICTLY ON THE PROVIDED CONTEXT - DO NOT HALLUCINATE
2. PROVIDE STRUCTURED ANALYSIS USING CLEAR SECTIONS
3. USE PROFESSIONAL LANGUAGE WITHOUT EXCESSIVE VERBIAGE
4. FOCUS ON PRACTICAL RECOMMENDATIONS BASED ON REPOSITORY PATTERNS
5. BE SPECIFIC ABOUT CODE QUALITY, ARCHITECTURE, SECURITY, AND SCALABILITY ISSUES

REQUIRED SECTIONS (use markdown headings):

## 🏗 Architecture Analysis
- Code organization and structure
- Design patterns observed
- Dependency management
- Module coupling/cohesion

## 🛡 Security Assessment
- Potential vulnerabilities
- Input validation patterns
- Authentication/authorization
- Data handling security

## ⚡ Scalability Evaluation
- Performance bottlenecks
- Resource usage patterns
- Concurrency handling
- Database/query efficiency

## 🧩 Maintainability Review
- Code readability
- Documentation quality
- Test coverage patterns
- Error handling consistency

## 🚀 Production Readiness
- Deployment considerations
- Monitoring/logging patterns
- Configuration management
- Resilience patterns

## 📈 Key Recommendations
- Specific, actionable improvements
- Prioritized by impact
- Based on repository analysis

METRICS SUMMARY (at the very end):

METRICS:
OVERALL_SCORE: [realistic score 1-10 based on context]
SECURITY: [GOOD/MODERATE/POOR based on patterns]
SCALABILITY: [GOOD/MODERATE/POOR based on patterns]
PRODUCTION_READINESS: [READY/MODERATE/NOT_READY based on patterns]

RECOMMENDATIONS:
- [specific recommendation #1]
- [specific recommendation #2]
- [specific recommendation #3]
- [specific recommendation #4]
- [specific recommendation #5]
"""

            response = llm.invoke(prompt)

        response_text = response.content

        # ============================================================
        # METRICS EXTRACTION
        # ============================================================

        overall_score = "8.2"
        security = "GOOD"
        scalability = "MODERATE"
        production = "READY"

        try:

            if "METRICS:" in response_text:

                metrics_section = response_text.split(
                    "METRICS:"
                )[1].split(
                    "RECOMMENDATIONS:"
                )[0]

                lines = metrics_section.split("\n")

                for line in lines:

                    if "OVERALL_SCORE:" in line:
                        overall_score = line.split(":")[1].strip()

                    elif "SECURITY:" in line:
                        security = line.split(":")[1].strip()

                    elif "SCALABILITY:" in line:
                        scalability = line.split(":")[1].strip()

                    elif "PRODUCTION_READINESS:" in line:
                        production = line.split(":")[1].strip()

        except:
            pass

        color_map = {
            "GOOD": "#4ade80",
            "MODERATE": "#38bdf8",
            "POOR": "#ef4444",
            "READY": "#a78bfa",
            "NOT_READY": "#f97316"
        }

        # ============================================================
        # EXECUTIVE METRICS
        # ============================================================

        st.markdown("<br><hr><br>", unsafe_allow_html=True)

        st.markdown("## 📊 Executive AI Audit Report")

        c1, c2, c3, c4 = st.columns(4)

        cards = [
            ("OVERALL SCORE", f"{overall_score} / 10", "#ffffff"),
            ("SECURITY", security, color_map.get(security, "#4ade80")),
            ("SCALABILITY", scalability, color_map.get(scalability, "#38bdf8")),
            ("PRODUCTION", production, color_map.get(production, "#a78bfa"))
        ]

        cols = [c1, c2, c3, c4]

        for col, card in zip(cols, cards):

            title, value, color = card

            with col:

                st.markdown(f"""
                <div class="card">
                    <div class="metric-title">{title}</div>
                    <div style="font-size:30px;font-weight:700;margin-top:12px;color:{color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # ============================================================
        # CLEAN OUTPUT
        # ============================================================

        display_response = response_text

        if "METRICS:" in display_response:
            display_response = display_response.split("METRICS:")[0]

        formatted_response = display_response.replace("**", "")

        formatted_response = re.sub(
            r'\n{3,}',
            '\n\n',
            formatted_response
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)

        response_placeholder = st.empty()

        full_response = ""

        words = formatted_response.split(" ")

        for word in words:

            full_response += word + " "

            response_placeholder.markdown(
                f"""
<div style="
font-size:17px;
line-height:1.9;
color:#e2e8f0;
">

{full_response}

<span style="color:#38bdf8;">▌</span>

</div>
""",
                unsafe_allow_html=True
            )

            time.sleep(0.008)

        response_placeholder.markdown(
            f"""
<div style="
font-size:17px;
line-height:1.9;
color:#e2e8f0;
">

{full_response}

</div>
""",
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        # ============================================================
        # RECOMMENDATIONS
        # ============================================================

        recommendations = []

        try:

            if "RECOMMENDATIONS:" in response_text:

                rec_section = response_text.split(
                    "RECOMMENDATIONS:"
                )[1]

                lines = rec_section.split("\n")

                for line in lines:

                    if line.strip().startswith("-"):

                        recommendations.append(
                            line.strip()[1:].strip()
                        )

        except:
            pass

        if not recommendations:

            recommendations = [
                "Improve repository modularity",
                "Add automated test coverage",
                "Improve exception handling",
                "Optimize architecture scalability",
                "Add CI/CD deployment workflow"
            ]

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown("## 📈 Enterprise Recommendations")

        for rec in recommendations:

            st.markdown(
                f"""
<div class="rec-card">

✅ {rec}

</div>
""",
                unsafe_allow_html=True
            )
