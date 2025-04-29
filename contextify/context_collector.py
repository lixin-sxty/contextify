import os
import json
import datetime
import re


def collect_project_context(project_root,
                            exts=None,
                            exclude_dirs=None,
                            include_dirs=None):
    if exts is None:
        exts = (".py", ".md", ".yaml", ".yml", ".toml", ".cfg", ".json",
                ".ini", ".txt", ".cpp", ".hpp", ".h", ".c", ".java", ".js",
                ".ts", ".html", ".css", ".sh")

    default_exclude_dirs = []

    # 读取 .gitignore 里的目录项，加入 exclude_dirs
    gitignore_path = os.path.join(project_root, ".gitignore")
    gitignore_dirs = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if line.endswith("/") or ("/" not in line and "*" not in line
                                          and "." not in line):
                    pattern = re.escape(line.rstrip("/"))
                    gitignore_dirs.append(pattern)

    exclude_dirs = exclude_dirs or []
    include_dirs = include_dirs or []
    all_exclude_dirs = default_exclude_dirs + gitignore_dirs + exclude_dirs

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
        if include_dirs:
            dirs[:] = [
                d for d in dirs if any(
                    re.fullmatch(p, d) for p in include_dirs)
            ]
        dirs[:] = [
            d for d in dirs if not any(
                re.fullmatch(pattern, d) for pattern in all_exclude_dirs)
        ]

        for file in files:
            if file.endswith(exts):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    rel_path = os.path.relpath(file_path, project_root)
                    context["files"].append({
                        "path": rel_path,
                        "content": content
                    })
                    context["total_files"] += 1
                    context["total_bytes"] += len(content.encode("utf-8"))
                    add_to_tree(context["file_tree"], rel_path)
                except Exception as e:
                    errors.append(f"❌ {file_path}: {e}")

    return context, errors, all_exclude_dirs, include_dirs


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
