<p align="center">
  <img src="assets/contextify_logo.png" alt="Contextify logo" width="300"/>
</p>

# Contextify

📦 **Contextify** 是一个将代码工程目录转化为 LLM（大语言模型）可理解上下文的工具。
它能提取项目结构、核心文件内容、环境信息，生成结构化 JSON 快照，方便大模型分析、代码补全、依赖排查和文档生成。

---

## 📌 功能特性

- 📖 **项目结构快照**：递归扫描项目目录，记录文件结构与内容
- 🔍 **智能目录排除**：自动识别 `.gitignore` 和常见目录（如 `__pycache__`、`venv` 等）
- 📊 **上下文差异对比**：支持对比任意两个快照，输出标准 diff 结果
- 🎛️ **可自定义扩展名、排除目录、包含目录**
- 🤖 **为 LLM 优化的上下文格式**，专为 AI 编码助手 / 文档生成场景设计

---

## 📦 编译与安装

```bash
# 开发者安装
python -m pip install -e .

# 打包为wheel文件
python -m build --wheel

# 安装wheel
python -m pip install contextify.whl
```

## 📖 使用方法

### 📤 导出项目上下文快照

```bash
contextify export <项目目录> --output <输出文件名> --exclude-dirs "__pycache__" "venv.*"

# 示例：
contextify export . --output snapshot.json
```

### 📊 对比两个快照差异

```bash
contextify diff old_snapshot.json new_snapshot.json
```

## 📂 快照 JSON 样例

```json
{
  "project_root": "/home/user/myproject",
  "export_time": "2025-04-29T12:00:00",
  "files": [
    { "path": "README.md", "content": "# My Project" },
    ...
  ],
  "total_files": 23,
  "total_bytes": 54012,
  "file_tree": {
    "files": ["README.md"],
    "src": {
      "files": ["main.py"]
    }
  }
}
```

## 📚 原理简介

Contextify 会：

1. 递归遍历项目目录，过滤 .gitignore 和常见无用目录
2. 根据指定扩展名收集核心文件内容
3. 构建文件树结构 + 文件内容上下文
4. 输出为 LLM 可用的结构化 JSON 快照
5. 对比功能基于 deepdiff，生成标准化差异报告
