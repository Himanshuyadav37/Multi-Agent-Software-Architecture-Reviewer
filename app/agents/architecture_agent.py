from langchain_groq import ChatGroq
from radon.complexity import cc_visit


# LLM Initialization
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)


# Complexity Analyzer
def get_complexity(code):

    try:

        results = cc_visit(code)

        complexity_data = []

        for item in results:

            complexity_data.append({
                "name": item.name,
                "complexity": item.complexity,
                "line": item.lineno
            })

        return complexity_data

    except:
        return []


# AI Architecture Review
def generate_architecture_report(
    file_path,
    complexity_data,
    ast_analysis
):

    prompt = f"""
You are an expert software architect and code quality reviewer.

Analyze the following software architecture and static analysis findings.

File:
{file_path}

Cyclomatic Complexity:
{complexity_data}

AST Analysis:
{ast_analysis}

Your tasks:
1. Identify architecture or maintainability issues.
2. Detect overly complex functions or components.
3. Identify code smells or bad design patterns.
4. Evaluate modularity and separation of concerns.
5. Suggest scalability improvements.
6. Recommend refactoring opportunities.
7. Mention maintainability risks.

Classify findings as:
- LOW
- MEDIUM
- HIGH

Generate output in this format:

ARCHITECTURE FINDINGS:
- Issue:
- Severity:
- Explanation:
- Recommendation:

Also provide:
- Overall Maintainability Score (0-10)
- Final Architecture Summary
"""

    response = llm.invoke(prompt)

    return response.content