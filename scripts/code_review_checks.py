import argparse
import ast
import logging
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, List, Optional, Sequence

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


class Severity(Enum):
    P0 = "CRITICAL"
    P1 = "ERROR"
    P2 = "WARNING"


@dataclass
class Issue:
    severity: Severity
    file_path: Path
    line: Optional[int]
    check: str
    message: str


SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}
CODE_EXTENSIONS = {".py", ".sh", ".js", ".ts", ".tsx"}
TEXT_EXTENSIONS = CODE_EXTENSIONS | {".md", ".yaml", ".yml"}
EXCLUDED_FILES = {"code_review_checks.py"}

ABSOLUTE_PATH_PATTERNS = [
    re.compile(r"/Us" + r"ers/"),
    re.compile(r"/ho" + r"me/"),
    re.compile(r"[A-Za-z]:" + r"\\\\"),
    re.compile(r"[A-Za-z]:/"),
]

RGLOB_PATTERN = re.compile(r"\.rglob\(")
GLOB_RECURSIVE_PATTERN = re.compile(r"\.glob\(\s*[\"']\*\*")
RETURN_EMPTY_PATTERN = re.compile(r"return\s+(\[\]|\{\}|set\(\))\s*(#.*)?$")
PROJECTS_ROOT_ENV_PATTERN = re.compile(
    r"os\.getenv\(\s*[\"']PROJECTS_ROOT[\"']\s*,\s*[\"'][\"']\s*\)"
)
PROJECTS_ROOT_USAGE_PATTERN = re.compile(r"\bPROJECTS_ROOT\b|\bprojects_root\b")
PROJECTS_ROOT_VALIDATION_PATTERN = re.compile(
    r"\b(PROJECTS_ROOT|projects_root)\b\.(is_dir|exists)\(\)"
)
PROJECTS_ROOT_LOG_PATTERN = re.compile(
    r"(logger|logging)\.(debug|info|warning|error|exception|critical)\(.*PROJECTS_ROOT",
    re.IGNORECASE,
)


def iter_files(root: Path) -> Iterable[Path]:
    for path in root.rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix in TEXT_EXTENSIONS:
            if path.name in EXCLUDED_FILES:
                continue
            yield path


def iter_code_files(root: Path) -> Iterable[Path]:
    for path in iter_files(root):
        if path.suffix in CODE_EXTENSIONS:
            yield path


def load_text(path: Path) -> Optional[str]:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        logger.warning("Could not read %s: %s", path, exc)
        return None


def find_absolute_paths(path: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    is_code = path.suffix in CODE_EXTENSIONS
    severity = Severity.P1 if is_code else Severity.P2
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in ABSOLUTE_PATH_PATTERNS:
            if pattern.search(line):
                issues.append(
                    Issue(
                        severity=severity,
                        file_path=path,
                        line=line_number,
                        check="PATH_VALIDATION",
                        message="Hardcoded absolute path detected",
                    )
                )
                break
    return issues


def find_expensive_operations(path: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if RGLOB_PATTERN.search(line) or GLOB_RECURSIVE_PATTERN.search(line):
            issues.append(
                Issue(
                    severity=Severity.P1,
                    file_path=path,
                    line=line_number,
                    check="EXPENSIVE_OPS",
                    message="Unbounded recursive glob detected",
                )
            )
    return issues


def find_sanity_checks(path: Path, lines: Sequence[str]) -> List[Issue]:
    issues: List[Issue] = []
    for idx, line in enumerate(lines):
        if RETURN_EMPTY_PATTERN.search(line):
            window = lines[max(0, idx - 5) : idx + 1]
            window_text = " ".join(window).lower()
            if "logger" not in window_text and "logging" not in window_text:
                issues.append(
                    Issue(
                        severity=Severity.P2,
                        file_path=path,
                        line=idx + 1,
                        check="SANITY_CHECKS",
                        message="Return empty value without nearby logging",
                    )
                )
    return issues


def _has_logging_call(node: ast.AST) -> bool:
    for call in [n for n in ast.walk(node) if isinstance(n, ast.Call)]:
        func = call.func
        if isinstance(func, ast.Attribute):
            if isinstance(func.value, ast.Name) and func.value.id in {"logger", "logging"}:
                return True
            if isinstance(func.value, ast.Attribute) and func.value.attr in {"logger", "logging"}:
                return True
        elif isinstance(func, ast.Name) and func.id in {"logger", "logging"}:
            return True
    return False


def _has_raise(node: ast.AST) -> bool:
    return any(isinstance(n, ast.Raise) for n in ast.walk(node))


def _is_pass_only(body: Sequence[ast.stmt]) -> bool:
    return all(isinstance(stmt, ast.Pass) for stmt in body)


def find_silent_failures(path: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return issues

    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                is_bare = handler.type is None
                is_exception = isinstance(handler.type, ast.Name) and handler.type.id == "Exception"
                line_no = handler.lineno if hasattr(handler, "lineno") else None

                if _is_pass_only(handler.body) and (is_bare or is_exception):
                    issues.append(
                        Issue(
                            severity=Severity.P0,
                            file_path=path,
                            line=line_no,
                            check="SILENT_FAILURES",
                            message="Bare except with pass",
                        )
                    )
                    continue

                if not _has_raise(handler) and not _has_logging_call(handler):
                    issues.append(
                        Issue(
                            severity=Severity.P1,
                            file_path=path,
                            line=line_no,
                            check="SILENT_FAILURES",
                            message="Exception caught without logging or re-raise",
                        )
                    )

    for line_number, line in enumerate(text.splitlines(), start=1):
        if re.search(r"except\s+Exception\s*:\s*pass", line):
            issues.append(
                Issue(
                    severity=Severity.P0,
                    file_path=path,
                    line=line_number,
                    check="SILENT_FAILURES",
                    message="except Exception with pass",
                )
            )
        if re.search(r"except\s*:\s*pass", line):
            issues.append(
                Issue(
                    severity=Severity.P0,
                    file_path=path,
                    line=line_number,
                    check="SILENT_FAILURES",
                    message="Bare except with pass",
                )
            )

    return issues


def find_projects_root_issues(path: Path, text: str) -> List[Issue]:
    issues: List[Issue] = []
    lines = text.splitlines()

    for line_number, line in enumerate(lines, start=1):
        if PROJECTS_ROOT_ENV_PATTERN.search(line):
            issues.append(
                Issue(
                    severity=Severity.P0,
                    file_path=path,
                    line=line_number,
                    check="PROJECTS_ROOT_E3A",
                    message="Empty string fallback for PROJECTS_ROOT",
                )
            )

    if not PROJECTS_ROOT_USAGE_PATTERN.search(text):
        return issues

    if not PROJECTS_ROOT_VALIDATION_PATTERN.search(text):
        issues.append(
            Issue(
                severity=Severity.P1,
                file_path=path,
                line=None,
                check="PROJECTS_ROOT_E3B",
                message="PROJECTS_ROOT used without .exists()/.is_dir() validation",
            )
        )

    if not PROJECTS_ROOT_LOG_PATTERN.search(text):
        issues.append(
            Issue(
                severity=Severity.P2,
                file_path=path,
                line=None,
                check="PROJECTS_ROOT_E3C",
                message="PROJECTS_ROOT resolved without startup logging",
            )
        )

    return issues


def collect_issues(root: Path) -> List[Issue]:
    issues: List[Issue] = []

    for file_path in iter_files(root):
        text = load_text(file_path)
        if text is None:
            continue

        issues.extend(find_absolute_paths(file_path, text))
        issues.extend(find_expensive_operations(file_path, text))
        issues.extend(find_sanity_checks(file_path, text.splitlines()))

        if file_path.suffix == ".py":
            issues.extend(find_silent_failures(file_path, text))
            issues.extend(find_projects_root_issues(file_path, text))

    return issues


def format_issue(issue: Issue) -> str:
    location = f"{issue.file_path}"
    if issue.line:
        location = f"{location}:{issue.line}"
    return f"{issue.severity.name} | {location} | {issue.check} | {issue.message}"


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Code review checks for common defects.")
    parser.add_argument("path", nargs="?", default=".", help="Root directory to scan")
    args = parser.parse_args(argv)

    root = Path(args.path).resolve()
    issues = collect_issues(root)

    p0_count = sum(1 for issue in issues if issue.severity == Severity.P0)
    p1_count = sum(1 for issue in issues if issue.severity == Severity.P1)
    p2_count = sum(1 for issue in issues if issue.severity == Severity.P2)

    for issue in issues:
        print(format_issue(issue))

    print("---")
    print(f"P0 (Critical): {p0_count}")
    print(f"P1 (Error): {p1_count}")
    print(f"P2 (Warning): {p2_count}")

    return 1 if (p0_count + p1_count) > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
