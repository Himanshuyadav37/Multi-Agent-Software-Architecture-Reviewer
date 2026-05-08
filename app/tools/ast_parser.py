import ast

DANGEROUS_FUNCTIONS = [
    "eval",
    "exec",
    "pickle",
    "os.system"
]

def analyze_code(code):

    tree = ast.parse(code)

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

        # Function Calls
        elif isinstance(node, ast.Call):

            if isinstance(node.func, ast.Name):
                func_name = node.func.id

                if func_name in DANGEROUS_FUNCTIONS:
                    dangerous_calls.append(func_name)

    return {
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "dangerous_calls": dangerous_calls
    }