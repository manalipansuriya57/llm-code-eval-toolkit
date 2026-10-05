"""Execute submitted Python solutions against task test cases."""

from __future__ import annotations

import ast
import signal
from contextlib import contextmanager
from typing import Any


class TimeoutError(Exception):
    pass


@contextmanager
def time_limit(seconds: int):
    def handler(signum, frame):  # noqa: ARG001
        raise TimeoutError("execution timed out")

    # SIGALRM unavailable on some platforms (e.g. Windows); fall back to no timer
    if not hasattr(signal, "SIGALRM"):
        yield
        return

    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


SAFE_BUILTINS = {
    "abs": abs,
    "all": all,
    "any": any,
    "bool": bool,
    "dict": dict,
    "enumerate": enumerate,
    "float": float,
    "int": int,
    "len": len,
    "list": list,
    "max": max,
    "min": min,
    "range": range,
    "reversed": reversed,
    "set": set,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "tuple": tuple,
    "zip": zip,
}


def _extract_function_name(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            return node.name
    return None


def run_code_against_tests(code: str, tests: list[dict[str, Any]], timeout_s: int = 2) -> dict[str, Any]:
    """Compile and run `code`, invoke the first top-level function on each test."""
    fn_name = _extract_function_name(code)
    if not fn_name:
        return {
            "passed": 0,
            "total": len(tests),
            "results": [],
            "error": "No top-level function definition found",
        }

    namespace: dict[str, Any] = {"__builtins__": SAFE_BUILTINS}
    try:
        with time_limit(timeout_s):
            exec(compile(code, "<submission>", "exec"), namespace)  # noqa: S102 — demo sandbox
    except Exception as exc:  # noqa: BLE001
        return {
            "passed": 0,
            "total": len(tests),
            "results": [],
            "error": f"Compile/runtime error: {exc}",
        }

    fn = namespace.get(fn_name)
    if not callable(fn):
        return {
            "passed": 0,
            "total": len(tests),
            "results": [],
            "error": f"Function `{fn_name}` not found after exec",
        }

    results = []
    passed = 0
    for i, case in enumerate(tests):
        args = case["args"]
        expected = case["expected"]
        try:
            with time_limit(timeout_s):
                got = fn(*args)
            ok = got == expected
            if ok:
                passed += 1
            results.append(
                {
                    "index": i,
                    "passed": ok,
                    "expected": expected,
                    "got": got,
                    "error": None,
                }
            )
        except Exception as exc:  # noqa: BLE001
            results.append(
                {
                    "index": i,
                    "passed": False,
                    "expected": expected,
                    "got": None,
                    "error": str(exc),
                }
            )

    return {"passed": passed, "total": len(tests), "results": results, "error": None}
