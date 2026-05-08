from typing import TypedDict

from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.parsers.ast_parser import analyze_code

from app.agents.security_agent import (
    generate_security_report
)

from app.agents.architecture_agent import (
    get_complexity,
    generate_architecture_report
)


# =========================================
# SHARED AGENT STATE
# =========================================

class AgentState(TypedDict):

    file_path: str
    content: str

    selected_agents: list

    ast_analysis: dict

    security_report: str

    complexity_data: list

    architecture_report: str


# =========================================
# AST ANALYZER NODE
# =========================================

def ast_node(state):

    analysis = analyze_code(
        state["content"]
    )

    state["ast_analysis"] = analysis

    return state


# =========================================
# SECURITY AGENT NODE
# =========================================

def security_node(state):

    report = generate_security_report(
        state["file_path"],
        state["ast_analysis"]
    )

    state["security_report"] = report

    return state


# =========================================
# ARCHITECTURE AGENT NODE
# =========================================

def architecture_node(state):

    complexity = get_complexity(
        state["content"]
    )

    state["complexity_data"] = complexity

    report = generate_architecture_report(
        state["file_path"],
        complexity,
        state["ast_analysis"]
    )

    state["architecture_report"] = report

    return state


# =========================================
# CREATE GRAPH
# =========================================

workflow = StateGraph(AgentState)


# =========================================
# ADD NODES
# =========================================

workflow.add_node(
    "AST Analyzer",
    ast_node
)

workflow.add_node(
    "Security Reviewer",
    security_node
)

workflow.add_node(
    "Architecture Reviewer",
    architecture_node
)


# =========================================
# DEFINE FLOW
# =========================================

workflow.add_edge(
    START,
    "AST Analyzer"
)

workflow.add_edge(
    "AST Analyzer",
    "Security Reviewer"
)

workflow.add_edge(
    "Security Reviewer",
    "Architecture Reviewer"
)

workflow.add_edge(
    "Architecture Reviewer",
    END
)


# =========================================
# COMPILE GRAPH
# =========================================

app = workflow.compile()