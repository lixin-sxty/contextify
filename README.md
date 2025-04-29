# contextify

📦 项目上下文快照和差异工具。

## 打包
```bash
python -m build --wheel
```
## 安装

```bash
pip install -e .
```

## 使用

### 导出项目上下文快照

```bash
contextify export <项目目录> --output <输出文件名> --exclude-dirs "__pycache__" "venv.*"
```

### 对比两个快照差异

```bash
contextify diff old.json new.json
```

## 特性

- 支持正则排除目录
- 项目结构快照
- 跨 Python 3.7+
- 标准 `deepdiff` 差异对比
- CLI 子命令：`export` / `diff`
