from pathlib import Path

# Root project folder
project = Path("dataauditkit")

# Folder structure
folders = [
    project / "dataauditkit",
    project / "tests",
    project / "examples",
    project / "docs"
]

# Files to create
files = [
    project / "dataauditkit" / "__init__.py",
    project / "dataauditkit" / "summary.py",
    project / "dataauditkit" / "missing.py",
    project / "dataauditkit" / "outliers.py",
    project / "dataauditkit" / "correlation.py",
    project / "dataauditkit" / "leakage.py",
    project / "dataauditkit" / "visualization.py",
    project / "dataauditkit" / "report.py",

    project / "tests" / "test_summary.py",
    project / "tests" / "test_missing.py",

    project / "examples" / "demo.ipynb",

    project / "pyproject.toml"
]

# Create folders
for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

# Create files
for file in files:
    file.touch(exist_ok=True)