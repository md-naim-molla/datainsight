from pathlib import Path

# Root project folder
project = Path("datainsight")

# Folder structure
folders = [
    project / "datainsight",
    project / "tests",
    project / "examples",
    project / "docs"
]

# Files to create
files = [
    project / "datainsight" / "__init__.py",
    project / "datainsight" / "summary.py",
    project / "datainsight" / "missing.py",
    project / "datainsight" / "outliers.py",
    project / "datainsight" / "correlation.py",
    project / "datainsight" / "leakage.py",
    project / "datainsight" / "visualization.py",
    project / "datainsight" / "report.py",

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