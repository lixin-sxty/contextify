import json
from deepdiff import DeepDiff


def diff_context_files(old_file, new_file):
    with open(old_file, "r", encoding="utf-8") as f:
        old_ctx = json.load(f)
    with open(new_file, "r", encoding="utf-8") as f:
        new_ctx = json.load(f)

    diff = DeepDiff(old_ctx, new_ctx, ignore_order=True)

    if not diff:
        print("✅ 两个上下文完全一致。")
        return

    print(f"--- {old_file}")
    print(f"+++ {new_file}\n")

    for change_type, changes in diff.items():
        print(f"@@ {change_type} @@")
        for path, detail in (changes.items() if isinstance(changes, dict) else
                             enumerate(changes)):
            print(f"{change_type}: {path} -> {detail}")
        print()
