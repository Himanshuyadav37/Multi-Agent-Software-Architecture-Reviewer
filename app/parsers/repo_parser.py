import os
from langchain_core.documents import Document


IGNORE_DIRS = {
    "myenv",
    "venv",
    "__pycache__",
    "node_modules",
    ".git",
    "dist",
    "build",
    "site-packages"
}


ALLOWED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx"
}


def load_code_files(repo_path):

    documents = []

    for root, dirs, files in os.walk(repo_path):

        # Ignore unnecessary folders
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
        ]

        for file in files:

            ext = os.path.splitext(file)[1]

            if ext in ALLOWED_EXTENSIONS:

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:

                        content = f.read()

                        documents.append({
                            "file_path": file_path,
                            "content": content
                        })

                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return documents