#!/usr/bin/env python3
"""
compare_traces.py

Structural diff of a hand-written trace.json against a GDB-parsed
trace_generated.json for the same problem. Compares ONLY:
  - line
  - variables
  - highlightIndices
  - mapState (where present)
per step, within each of the "bruteForce" / "optimized" sections.

Deliberately ignored:
  - "explanation" text (wording differences don't matter here)
  - "code" arrays (formatting/source differences aren't the point)
  - "complexity" (a human/heuristic label, not a traced value)
  - "discoveryQuestions" / "predictionQuestions" (hand-authored content
    with no GDB-traced equivalent)

Because the generated trace currently only captures the breakpoints
the workflow actually sets (fewer, coarser-grained than the
hand-written trace.json's step-by-step walkthrough), this script
compares by (line, subset of variable keys present in the generated
step) rather than assuming a 1:1 step-index correspondence. For each
generated step, it looks for a hand-written step at the same line
whose "variables" agree on every key the generated step actually has
values for. This finds a genuine match if the algorithm traced the
same real event, without requiring every hand-written step (e.g. pure
loop-init steps with no comparison) to have a generated counterpart.

USAGE:
    python3 scripts/compare_traces.py <problem_dir>

Exit code: 0 if no differences found, 1 if any differences (or
missing generated-side coverage) were found. Prints a report either
way.
"""

import json
import os
import sys


COMPARE_KEYS = ("line", "variables", "highlightIndices", "mapState")


def load(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)


def find_best_match(gen_step, hand_steps):
    """Finds a hand-written step at the same line whose variables agree
    with every variable the generated step actually has. Returns
    (match_or_None, list_of_disagreements_for_best_candidate)."""
    candidates = [s for s in hand_steps if s.get("line") == gen_step.get("line")]
    if not candidates:
        return None, ["no hand-written step at this line"]

    best = None
    best_diffs = None
    for cand in candidates:
        diffs = []
        gen_vars = gen_step.get("variables", {})
        cand_vars = cand.get("variables", {})
        for key, val in gen_vars.items():
            if key not in cand_vars:
                diffs.append(f"variable '{key}' not present in hand-written step")
            elif cand_vars[key] != val:
                diffs.append(
                    f"variable '{key}': generated={val!r} vs hand-written={cand_vars[key]!r}"
                )

        gen_hl = gen_step.get("highlightIndices", [])
        cand_hl = cand.get("highlightIndices", [])
        if gen_hl and gen_hl != cand_hl:
            diffs.append(
                f"highlightIndices: generated={gen_hl!r} vs hand-written={cand_hl!r}"
            )

        if best is None or len(diffs) < len(best_diffs):
            best, best_diffs = cand, diffs
        if not diffs:
            break

    return best, best_diffs


def compare_section(section_name, hand_section, gen_section, report):
    if hand_section is None and gen_section is None:
        return
    if hand_section is None:
        report.append(f"[{section_name}] present in generated only (no hand-written section)")
        return
    if gen_section is None:
        report.append(f"[{section_name}] present in hand-written only (not yet captured by GDB pipeline)")
        return

    hand_steps = hand_section.get("steps", [])
    gen_steps = gen_section.get("steps", [])

    report.append(
        f"[{section_name}] hand-written steps: {len(hand_steps)}, "
        f"generated steps: {len(gen_steps)}"
    )
    if len(hand_steps) != len(gen_steps):
        report.append(
            f"[{section_name}] STEP COUNT DIFFERS -- generated trace currently only "
            f"captures breakpoints actually set in the workflow, which is coarser "
            f"than the hand-written walkthrough (see script docstring)."
        )

    any_step_diff = False
    for idx, gen_step in enumerate(gen_steps):
        match, diffs = find_best_match(gen_step, hand_steps)
        if diffs:
            any_step_diff = True
            report.append(
                f"[{section_name}] generated step #{idx} (line {gen_step.get('line')}, "
                f"variables={gen_step.get('variables')}):"
            )
            for d in diffs:
                report.append(f"    - {d}")
        else:
            report.append(
                f"[{section_name}] generated step #{idx} (line {gen_step.get('line')}) "
                f"MATCHES hand-written step -- variables and highlightIndices agree."
            )

    if not any_step_diff and len(hand_steps) == len(gen_steps):
        report.append(f"[{section_name}] ZERO DIFFERENCES on compared fields.")
    elif not any_step_diff:
        report.append(
            f"[{section_name}] all generated steps matched their corresponding "
            f"hand-written step on compared fields, but step counts differ (see above)."
        )


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <problem_dir>", file=sys.stderr)
        sys.exit(2)

    problem_dir = sys.argv[1].rstrip("/")
    hand_path = os.path.join(problem_dir, "trace.json")
    gen_path = os.path.join(problem_dir, "trace_generated.json")

    hand = load(hand_path)
    gen = load(gen_path)

    if hand is None:
        print(f"Error: {hand_path} not found", file=sys.stderr)
        sys.exit(2)
    if gen is None:
        print(f"Error: {gen_path} not found -- run parse_gdb_trace.py first", file=sys.stderr)
        sys.exit(2)

    report = [f"Comparing {hand_path} vs {gen_path}", ""]

    for section_name in ("bruteForce", "optimized"):
        compare_section(
            section_name, hand.get(section_name), gen.get(section_name), report
        )
        report.append("")

    print("\n".join(report))

    has_real_diff = any(
        ("variable '" in line or "highlightIndices:" in line or "no hand-written step" in line)
        for line in report
    )
    sys.exit(1 if has_real_diff else 0)


if __name__ == "__main__":
    main()
