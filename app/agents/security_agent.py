from langchain_groq import ChatGroq

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

def generate_security_report(file_path, analysis):

    prompt = f"""
You are an advanced AI-powered cybersecurity and software architecture review agent.

Your task is to analyze static AST analysis findings from a source code repository and generate a professional security assessment report.

Repository File:
{file_path}

AST Analysis Findings:
{analysis}

Perform a detailed security-focused analysis.

Instructions:
1. Identify dangerous or suspicious coding patterns.
2. Explain why each issue is risky.
3. Classify severity as:
   - LOW
   - MEDIUM
   - HIGH
   - CRITICAL
4. Mention potential attack vectors or exploitation risks if applicable.
5. Suggest secure coding improvements and mitigation strategies.
6. Mention if no significant security issue is found.
7. Avoid hallucinating vulnerabilities that are not supported by the findings.
8. Focus on real-world software engineering and cybersecurity best practices.

Generate output in this professional format:

SECURITY FINDINGS:
- Issue:
- Severity:
- Explanation:
- Risk Impact:
- Recommendation:

Also provide:
- Overall Security Risk Score (0-10)
- Final Security Summary

Be concise but technically strong.
"""

    response = llm.invoke(prompt)

    return response.content