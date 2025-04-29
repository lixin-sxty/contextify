import argparse
from .context_collector import collect_project_context, print_tree
from .diff_tool import diff_context_files
import json
import datetime

def main():
    parser = argparse.ArgumentParser(description="📦 项目上下文快照和差异工具 projctx")
    subparsers = parser.add_subparsers(dest="command")

    export_parser = subparsers.add_parser("export", help="导出项目上下文快照")
    export_parser.add_argument("project_dir", type=str, help="项目目录路径")
    export_parser.add_argument("--output", type=str, default=None, help="输出 JSON 文件名")
    export_parser.add_argument("--exts", nargs="+", default=None, help="要收集的文件扩展名")
    export_parser.add_argument("--exclude-dirs", nargs="+", default=None, help="排除目录正则")

    diff_parser = subparsers.add_parser("diff", help="对比两个上下文快照")
    diff_parser.add_argument("old_file", type=str, help="旧版本 JSON 文件")
    diff_parser.add_argument("new_file", type=str, help="新版本 JSON 文件")

    args = parser.parse_args()

    if args.command == "export":
        project_name = args.project_dir.rstrip("/").split("/")[-1]
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = args.output or f"{project_name}_{timestamp}.json"
        exts = tuple(args.exts) if args.exts else None

        context, errors, exclude_dirs_used = collect_project_context(
            args.project_dir, exts=exts, exclude_dirs=args.exclude_dirs)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(context, f, indent=2, ensure_ascii=False)

        print(f"\n✅ 已导出上下文: {output_file}")
        print(f"📦 导出文件: {context['total_files']} 个，累计 {context['total_bytes']} 字节")
        print(f"\n📂 排除目录正则：")
        for pattern in exclude_dirs_used:
            print(f"  - {pattern}")

        if errors:
            print("\n⚠️ 以下文件读取失败：")
            for err in errors:
                print(err)

        print("\n📂 文件结构：")
        print_tree(context["file_tree"])

    elif args.command == "diff":
        diff_context_files(args.old_file, args.new_file)

    else:
        parser.print_help()
