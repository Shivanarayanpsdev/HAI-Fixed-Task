"""Verifier for dynamo/log-report.

Each test corresponds 1:1 to a numbered success criterion in instruction.md.
The expected values are computed independently from the fixed
/app/access.log that ships in the environment image (see environment/access.log),
so a stub, empty, or partially-correct report fails.
"""
import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _load_report():
    assert REPORT_PATH.exists(), "expected /app/report.json to exist"
    with REPORT_PATH.open() as f:
        return json.load(f)


def _expected():
    """Independently recompute the expected summary from the raw log."""
    total = 0
    ips = set()
    path_counts = {}
    for line in LOG_PATH.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        # The request line is the first double-quoted field, e.g.
        # "GET /index.html HTTP/1.1"
        quoted = line.split('"')[1]
        fields = quoted.split()
        if len(fields) >= 2:
            path = fields[1]
            path_counts[path] = path_counts.get(path, 0) + 1
    top_path = max(path_counts, key=path_counts.get) if path_counts else None
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": top_path,
        "top_count": path_counts.get(top_path),
        "path_counts": path_counts,
    }


def test_report_is_valid_json_object():
    """Criterion 1: /app/report.json exists and contains a valid JSON object."""
    report = _load_report()
    assert isinstance(report, dict)


def test_total_requests():
    """Criterion 2: total_requests equals the number of non-empty log lines."""
    report = _load_report()
    expected = _expected()
    assert report.get("total_requests") == expected["total_requests"]


def test_unique_ips():
    """Criterion 3: unique_ips equals the number of distinct client IPs."""
    report = _load_report()
    expected = _expected()
    assert report.get("unique_ips") == expected["unique_ips"]


def test_top_path():
    """Criterion 4: top_path equals the most frequently requested path.

    Ties are accepted: any path with the maximum count is a valid answer.
    """
    report = _load_report()
    expected = _expected()
    reported_path = report.get("top_path")
    assert reported_path in expected["path_counts"], (
        f"{reported_path!r} does not appear in the log at all"
    )
    assert expected["path_counts"][reported_path] == expected["top_count"], (
        f"{reported_path!r} was not the most frequently requested path"
    )
