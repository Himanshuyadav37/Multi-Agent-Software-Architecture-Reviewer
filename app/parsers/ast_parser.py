import ast

DANGEROUS_FUNCTIONS = [
    "eval",
    "exec",
    "pickle",
    "loads",
    "os.system",
    "subprocess",
    "Popen"
]

def analyze_code(code):

    try:
        tree = ast.parse(code)
    except:
        return {}

    functions = []
    classes = []
    imports = []
    dangerous_calls = []

    for node in ast.walk(tree):

        # Functions
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)

        # Classes
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        # Imports
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module)

        # Dangerous Calls
        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):

                if node.func.id in DANGEROUS_FUNCTIONS:

                    dangerous_calls.append({
                        "function": node.func.id,
                        "line": node.lineno
                    })

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "dangerous_calls": dangerous_calls
    }