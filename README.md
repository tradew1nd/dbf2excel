# dbf2excel

将当前文件夹下的所有 `.dbf` 文件转换为 Excel，并输出到当前文件夹下的 `excel` 目录中，输出文件名与原始文件名保持一致。

## 功能说明

- 扫描当前目录下所有 `.dbf` 文件
- 将每个 `.dbf` 转为 `.xlsx`
- 输出到 `excel` 目录
- 支持通过 `PyInstaller` 打包为 Windows `.exe`
- 已配置 GitHub Actions，在推送到 `main` 后自动打包 exe

## 本地运行

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install .
dbf2excel
```

如果数据库文件编码特殊，也可以手动指定：

```bash
dbf2excel --encoding gbk
```

## 本地打包 EXE

在 Windows 环境下执行：

```bash
pip install -r requirements.txt
pip install .
pyinstaller --name dbf2excel --onefile --clean --paths src src/dbf2excel/cli.py
```

生成的可执行文件位于：

```text
dist/dbf2excel.exe
```

## GitHub Actions

工作流文件位于：

```text
.github/workflows/build-exe.yml
```

触发方式：

- push 到 `main`
- 手动触发 `workflow_dispatch`

构建完成后，可在 GitHub Actions 的构建产物中下载：

```text
dbf2excel-windows-exe
```
