#!/usr/bin/env python3
"""
parse_gdb_trace.py

Parses raw GDB batch-mode output (as produced by the "Inspect ... with
GDB" steps in .github/workflows/trace-poc.yml) into JSON shaped like
the hand-written trace.json files used elsewhere in this repo.

Every "line" and "variables" value that ends up in the output comes
directly from parsing the real GDB output for that problem -- nothing
is guessed, re-derived from unrelated sources, or copied from an
existing hand-written trace.json. Two things ARE computed rather than
printed verbatim by GDB, and both are simple arithmetic/derivation
from values GDB DID print, not guesses:
  - "sum" for brute-force steps = nums_i + nums_j (both real GDB values)
  - "highlightIndices" = the list of loop index variables (i, and j if
    present) captured at that breakpoint hit

Fields present in the hand-written trace.json schema that this script
has no real data source for (e.g. "mapState", "found") are simply
omitted from generated steps rather than fabricated. See
problems/GDB_TRACE_PIPELINE.md for what it would take to capture them
(additional GDB breakpoints/prints in the workflow).

USAGE:
    python3 scripts/parse_gdb_trace.py <problem_dir>

<problem_dir> is a path such as problems/hash-map/two-sum, expected to
contain (relative to it):
  - solution.cpp                    (optimized solution source)
  - bruteforce_driver.cpp           (brute-force driver source)
  - gdb_raw_trace.txt               (raw GDB output, optimized pass)
  - gdb_raw_trace_bruteforce.txt    (raw GDB output, brute-force pass)

Any of the four inputs may be absent; that section is simply skipped
in the output (its key is omitted from trace_generated.json).

Writes: <problem_dir>/trace_generated.json
"""

import json
import os
import re
import sys


# ---------------------------------------------------------------------------
# Breakpoint manifests
#
# GDB's batch output prints bare "$N = value" lines with no variable
# name attached -- the name is implied purely by the order of the
# "-ex print ..." commands issued in the workflow. These manifests
# record that known, fixed command order for each breakpoint line so
# real printed values can be labeled correctly. This is not a guess
# about the *value* (that always comes from the real GDB output); it
# documents the *command sequence* already committed in
# .github/workflows/trace-poc.yml.
#
# New problems need their own manifest entry here (see
# problems/GDB_TRACE_PIPELINE.md) -- this is the one part of the
# pipeline that is inherently problem-specific, since different
# algorithms have different variables.
# ---------------------------------------------------------------------------

BREAKPOINT_MANIFESTS = {
    "solution.cpp": {
        # print i / print nums[i] / print target - nums[i]
        "vars_by_hit_order": ["i", "nums_i", "complement"],
    },
    "bruteforce_driver.cpp": {
        # print i / print j / print nums[i] / print nums[j]
        "vars_by_hit_order": ["i", "j", "nums_i", "nums_j"],
    },
}

# Breakpoints hit exactly once, at the return/match line, print a
# shorter list (this repo's workflow prints fewer values there).
FINAL_BREAKPOINT_MANIFESTS = {
    "solution.cpp": ["i", "complement"],
    "bruteforce_driver.cpp": ["i", "j"],
}


BREAKPOINT_HEADER_RE = re.compile(
    r"^Breakpoint (\d+), .* at (?P<file>[^:]+):(?P<line>\d+)$"
)
GDB_VALUE_RE = re.compile(r"^\$(\d+) = (.+)$")


def parse_gdb_value(raw):
    """Best-effort conversion of a raw GDB printed value to a Python
    int/float/str. GDB prints plain integers for the int-typed
    variables this script deals with, so int() covers the real cases;
    fall back to the raw string for anything unexpected rather than
    silently coercing it."""
    raw = raw.strip()
    try:
        return int(raw)
    except ValueError:
        try:
            return float(raw)
        except ValueError:
            return raw


def parse_gdb_log(path):
    """Parses a raw GDB batch-log file into a list of breakpoint hits:
    [{"file": ..., "line": <source line, int>, "values": [v1, v2, ...]}, ...]
    in the order they occurred during execution.
    """
    with open(path, "r") as f:
        lines = f.read().splitlines()

    hits = []
    current = None

    for line in lines:
        header_match = BREAKPOINT_HEADER_RE.match(line)
        if header_match:
            if current is not None:
                hits.append(current)
            current = {
                "file": os.path.basename(header_match.group("file")),
                "line": int(header_match.group("line")),
                "values": [],
            }
            continue

        value_match = GDB_VALUE_RE.match(line)
        if value_match and current is not None:
            current["values"].append(parse_gdb_value(value_match.group(2)))

    if current is not None:
        hits.append(current)

    return hits


def label_hit(hit, manifests, final_manifests, final_line):
    """Attaches variable names to a hit's raw printed values, using the
    manifest for whichever source file the breakpoint was in. Returns
    a dict of {name: value}."""
    manifest = manifests.get(hit["file"])
    final_names = final_manifests.get(hit["file"])

    if hit["line"] == final_line and final_names is not None:
        names = final_names
    elif manifest is not None:
        names = manifest["vars_by_hit_order"]
    else:
        names = [f"value_{i}" for i in range(len(hit["values"]))]

    return dict(zip(names, hit["values"]))


def extract_class_block(source_path):
    """Reads a driver/solution .cpp file and returns just the
    "class Solution { ... };" block as a list of lines, matching the
    convention used in the hand-written trace.json "code" arrays.
    Returns None if the file doesn't exist or no class block is found.
    """
    if not os.path.exists(source_path):
        return None

    with open(source_path, "r") as f:
        raw_lines = f.readlines()

    start = None
    end = None
    for idx, line in enumerate(raw_lines):
        if line.strip().startswith("class Solution"):
            start = idx
            break
    if start is None:
        return None

    for idx in range(start, len(raw_lines)):
        if raw_lines[idx].strip() == "};":
            end = idx
            break
    if end is None:
        return None

    return [l.rstrip("\n") for l in raw_lines[start : end + 1]]


def estimate_complexity(code_lines):
    """Very small heuristic based on nested-loop depth in the extracted
    class block. This is NOT derived from GDB output (GDB has no
    concept of asymptotic complexity) -- it's a structural heuristic
    over the source, included only as a convenience label, same as
    the hand-written trace.json's "complexity" field is a human
    annotation rather than a measured quantity."""
    depth = 0
    max_depth = 0
    for line in code_lines:
        stripped = line.strip()
        if stripped.startswith("for") or stripped.startswith("while"):
            depth += 1
            max_depth = max(max_depth, depth)
        # crude: count closing braces as loop exits once we've seen a loop
        if stripped == "}" and depth > 0:
            depth -= 1

    if max_depth >= 2:
        return "O(n\u00b2)"
    if max_depth == 1:
        return "O(n)"
    return "O(1)"


def build_bruteforce_section(problem_dir, class_offset):
    """class_offset: number of lines between the start of the source
    file and the start of the "class Solution" block, i.e. the value
    to subtract from a GDB-reported absolute file line number to get
    the line number relative to the extracted class-only code array
    (matching trace.json's convention, where "code" starts at
    "class Solution {")."""
    driver_path = os.path.join(problem_dir, "bruteforce_driver.cpp")
    trace_path = os.path.join(problem_dir, "gdb_raw_trace_bruteforce.txt")

    code = extract_class_block(driver_path)
    if code is None or not os.path.exists(trace_path):
        return None

    hits = parse_gdb_log(trace_path)
    if not hits:
        return None

    final_line_abs = max(h["line"] for h in hits)

    steps = []
    for hit in hits:
        values = label_hit(
            hit, BREAKPOINT_MANIFESTS, FINAL_BREAKPOINT_MANIFESTS, final_line_abs
        )
        relative_line = hit["line"] - class_offset + 1  # +1: code array is 1-indexed

        highlight_indices = []
        if "i" in values:
            highlight_indices.append(values["i"])
        if "j" in values:
            highlight_indices.append(values["j"])

        # Derive "sum" only when we actually have both real operands.
        if "nums_i" in values and "nums_j" in values:
            values = dict(values)
            values["sum"] = values["nums_i"] + values["nums_j"]

        if hit["line"] == final_line_abs:
            explanation = (
                f"Match found! nums[{values.get('i')}] + "
                f"nums[{values.get('j')}] equals the target."
            )
        else:
            explanation = (
                f"Comparing nums[{values.get('i')}] + nums[{values.get('j')}] "
                f"= {values.get('sum')} against the target."
            )

        steps.append(
            {
                "line": relative_line,
                "variables": values,
                "highlightIndices": highlight_indices,
                "explanation": explanation,
            }
        )

    return {
        "code": code,
        "complexity": estimate_complexity(code),
        "steps": steps,
    }


def build_optimized_section(problem_dir):
    solution_path = os.path.join(problem_dir, "solution.cpp")
    trace_path = os.path.join(problem_dir, "gdb_raw_trace.txt")

    if not os.path.exists(solution_path) or not os.path.exists(trace_path):
        return None

    with open(solution_path, "r") as f:
        code = [l.rstrip("\n") for l in f.readlines()]
        # Drop a single fully-blank trailing line, if present, to match
        # trace.json's convention (no trailing empty-string entry).
        while code and code[-1] == "":
            code.pop()

    hits = parse_gdb_log(trace_path)
    if not hits:
        return None

    final_line_abs = max(h["line"] for h in hits)

    steps = []
    for hit in hits:
        values = label_hit(
            hit, BREAKPOINT_MANIFESTS, FINAL_BREAKPOINT_MANIFESTS, final_line_abs
        )
        # solution.cpp's own line numbers already match the "code"
        # array 1:1, since the code array is the whole file verbatim.
        relative_line = hit["line"]

        highlight_indices = []
        if "i" in values:
            highlight_indices.append(values["i"])

        if hit["line"] == final_line_abs:
            explanation = (
                f"Match found at i={values.get('i')}: complement "
                f"{values.get('complement')} was already in the map."
            )
        else:
            explanation = (
                f"At i={values.get('i')} (nums[i]={values.get('nums_i')}), "
                f"complement = {values.get('complement')}."
            )

        steps.append(
            {
                "line": relative_line,
                "variables": values,
                "highlightIndices": highlight_indices,
                "explanation": explanation,
            }
        )

    return {
        "code": code,
        "complexity": estimate_complexity(code),
        "steps": steps,
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <problem_dir>", file=sys.stderr)
        sys.exit(1)

    problem_dir = sys.argv[1].rstrip("/")
    if not os.path.isdir(problem_dir):
        print(f"Error: not a directory: {problem_dir}", file=sys.stderr)
        sys.exit(1)

    result = {}

    # class_offset for the brute-force driver: GDB reports absolute
    # file line numbers, but the "class Solution" block doesn't
    # necessarily start at line 1 of the driver file (it's preceded by
    # comments/#includes). Compute the offset by locating the class
    # start directly, rather than assuming a fixed value.
    driver_path = os.path.join(problem_dir, "bruteforce_driver.cpp")
    class_offset = 0
    if os.path.exists(driver_path):
        with open(driver_path, "r") as f:
            for idx, line in enumerate(f.readlines()):
                if line.strip().startswith("class Solution"):
                    class_offset = idx + 1  # 1-indexed line number of "class Solution {"
                    break

    bruteforce = build_bruteforce_section(problem_dir, class_offset)
    if bruteforce is not None:
        result["bruteForce"] = bruteforce

    optimized = build_optimized_section(problem_dir)
    if optimized is not None:
        result["optimized"] = optimized

    out_path = os.path.join(problem_dir, "trace_generated.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
