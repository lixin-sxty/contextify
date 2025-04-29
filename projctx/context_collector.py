import os
import json
import datetime
import re

def collect_project_context(project_root, exts=None, exclude_dirs=None):
    if exts is None:
        exts = (".py", ".md", ".yaml", ".yml", ".toml", ".cfg", ".json",
                ".ini", ".txt", ".cpp", ".hpp", ".h", ".c", ".java", ".js",
                ".ts", ".html", ".css", ".sh")

    default_exclude_dirs = [
        r"\.git", r"__pycache__", r"venv", r"node_modules", r"\.idea", r"\.vscode",
        r"build", r"dist", r"output", r"third_party", r"logs", r"\.DS_Store", r"\.mypy_cache"
    ]

    exclude_dirs = exclude_dirs or []
    all_exclude_dirs = default_exclude_dirs + exclude_dirs

    context = {
        "project_root": os.path.abspath(project_root),
        "export_time": datetime.datetime.now().isoformat(),
        "files": [],
        "total_files": 0,
        "total_bytes": 0,
        "file_tree": {}
    }

    errors = []

    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if not any(re.fullmatch(pattern, d) for pattern in all_exclude_dirs)]
        for file in files:
            if file.endswith(exts):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    rel_path = os.path.relpath(file_path, project_root)
                    context["files"].append({"path": rel_path, "content": content})
                    context["total_files"] += 1
                    context["total_bytes"] += len(content.encode("utf-8"))
                    add_to_tree(context["file_tree"], rel_path)
                except Exception as e:
                    errors.append(f"❌ {file_path}: {e}")

    return context, errors, all_exclude_dirs

def add_to_tree(tree, file_path):
    parts = file_path.split(os.sep)
    for part in parts[:-1]:
        tree = tree.setdefault(part, {})
    tree.setdefault("files", []).append(parts[-1])

def print_tree(tree, indent=0):
    for key, value in tree.items():
        if key == "files":
            for f in value:
                print("  " * indent + f"📄 {f}")
        else:
            print("  " * indent + f"📁 {key}/")
            print_tree(value, indent + 1)
