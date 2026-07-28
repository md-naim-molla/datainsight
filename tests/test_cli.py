import os
import pandas as pd
from dataauditkit.cli import main


def test_cli_profile_creates_html(tmp_path):
    csv_path = tmp_path / "test.csv"
    out_path = tmp_path / "report.html"
    pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]}).to_csv(csv_path, index=False)

    import sys
    sys.argv = ["dataauditkit", "profile", str(csv_path), "--output", str(out_path)]
    main()
    assert os.path.exists(out_path)
    with open(out_path) as f:
        assert "DataAuditKit Report" in f.read()


def test_cli_profile_with_target(tmp_path):
    csv_path = tmp_path / "test.csv"
    out_path = tmp_path / "report.html"
    pd.DataFrame({"A": [1, 2, 3], "target": [0, 0, 1]}).to_csv(csv_path, index=False)

    import sys
    sys.argv = ["dataauditkit", "profile", str(csv_path), "--target", "target", "--output", str(out_path)]
    main()
    assert os.path.exists(out_path)


def test_cli_compare_creates_html(tmp_path):
    csv1 = tmp_path / "d1.csv"
    csv2 = tmp_path / "d2.csv"
    out_path = tmp_path / "comparison.html"
    pd.DataFrame({"A": [1, 2, 3]}).to_csv(csv1, index=False)
    pd.DataFrame({"A": [4, 5, 6], "B": [7, 8, 9]}).to_csv(csv2, index=False)

    import sys
    sys.argv = ["dataauditkit", "compare", str(csv1), str(csv2), "--output", str(out_path)]
    main()
    assert os.path.exists(out_path)
    with open(out_path) as f:
        assert "DataAuditKit Comparison" in f.read()


def test_cli_no_args_shows_help(capsys):
    import sys
    sys.argv = ["dataauditkit"]
    try:
        main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert "usage" in captured.out.lower() or "usage" in captured.err.lower()
