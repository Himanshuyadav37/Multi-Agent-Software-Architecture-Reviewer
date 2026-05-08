# =========================================
# REPOSITORY CLASSIFIER
# =========================================


def classify_repository(documents):
    tech_stack = {
        "react": False,
        "python": False,
        "docker": False
    }

    for doc in documents:

        path = doc["file_path"].lower()

        if ".jsx" in path or ".tsx" in path:
            tech_stack["react"] = True

        if ".py" in path:
            tech_stack["python"] = True

        if "dockerfile" in path:
            tech_stack["docker"] = True

    return tech_stack



# =========================================
# AGENT DECISION LOGIC
# =========================================


def decide_agents(tech_stack):

    agents = []

    if tech_stack["react"]:
        agents.append("frontend")

    if tech_stack["python"]:
        agents.append("security")
        agents.append("architecture")

    if tech_stack["docker"]:
        agents.append("devops")

    return agents