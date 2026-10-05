"""Sample coding tasks used for LLM response evaluation demos."""

from typing import Any

TASKS: list[dict[str, Any]] = [
    {
        "id": "two-sum",
        "title": "Two Sum",
        "language": "python",
        "prompt": (
            "Write a function `two_sum(nums: list[int], target: int) -> list[int]` "
            "that returns indices of two numbers that add up to target. "
            "Assume exactly one solution exists."
        ),
        "starter": "def two_sum(nums, target):\n    pass\n",
        "tests": [
            {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"args": [[3, 2, 4], 6], "expected": [1, 2]},
            {"args": [[3, 3], 6], "expected": [0, 1]},
        ],
        "sample_response": (
            "def two_sum(nums, target):\n"
            "    seen = {}\n"
            "    for i, n in enumerate(nums):\n"
            "        need = target - n\n"
            "        if need in seen:\n"
            "            return [seen[need], i]\n"
            "        seen[n] = i\n"
            "    return []\n"
        ),
    },
    {
        "id": "valid-parens",
        "title": "Valid Parentheses",
        "language": "python",
        "prompt": (
            "Write `is_valid(s: str) -> bool` that returns True if brackets "
            "`()[]{}` are balanced and correctly nested."
        ),
        "starter": "def is_valid(s):\n    pass\n",
        "tests": [
            {"args": ["()"], "expected": True},
            {"args": ["()[]{}"], "expected": True},
            {"args": ["(]"], "expected": False},
            {"args": ["([)]"], "expected": False},
            {"args": ["{[]}"], "expected": True},
        ],
        "sample_response": (
            "def is_valid(s):\n"
            "    pairs = {')': '(', ']': '[', '}': '{'}\n"
            "    stack = []\n"
            "    for ch in s:\n"
            "        if ch in '([{':\n"
            "            stack.append(ch)\n"
            "        elif ch in pairs:\n"
            "            if not stack or stack[-1] != pairs[ch]:\n"
            "                return False\n"
            "            stack.pop()\n"
            "    return not stack\n"
        ),
    },
    {
        "id": "flatten-dict",
        "title": "Flatten Nested Dict",
        "language": "python",
        "prompt": (
            "Write `flatten(d: dict, sep='.') -> dict` that flattens nested "
            "dictionaries into dot-separated keys. Values are leaves only."
        ),
        "starter": "def flatten(d, sep='.'):\n    pass\n",
        "tests": [
            {
                "args": [{"a": 1, "b": {"c": 2, "d": {"e": 3}}}],
                "expected": {"a": 1, "b.c": 2, "b.d.e": 3},
            },
            {"args": [{}], "expected": {}},
            {"args": [{"x": {"y": 0}}, "/"], "expected": {"x/y": 0}},
        ],
        "sample_response": (
            "def flatten(d, sep='.'):\n"
            "    out = {}\n"
            "    def walk(obj, prefix=''):\n"
            "        if isinstance(obj, dict):\n"
            "            for k, v in obj.items():\n"
            "                key = f'{prefix}{sep}{k}' if prefix else k\n"
            "                walk(v, key)\n"
            "        else:\n"
            "            out[prefix] = obj\n"
            "    walk(d)\n"
            "    return out\n"
        ),
    },
]
