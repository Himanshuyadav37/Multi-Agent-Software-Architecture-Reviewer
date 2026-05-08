import os

def load_python_files(repo_path):
    files_data=[]

    for root, dirs, files in os.walk(repo_path):

        # ignore unnecessary folder
        dir[:] = [
            d for d in dirs
            if d not in ["myenv", "__pycache__", ".git"]
        ]

        for file in files:
            if file.endwith(".py"):

                full_path = os.path.join(root,file)

                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    files_data.append({
                        "file":full_path,
                        "content": content
                    })

                except Exception as e:
                     print(f"Error reading {full_path}: {e}")
        
    return files_data
