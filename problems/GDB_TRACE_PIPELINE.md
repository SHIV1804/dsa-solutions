# GDB Trace Pipeline

This documents how the `Trace POC` GitHub Actions workflow
(`.github/workflows/trace-poc.yml`) and the two scripts under
`scripts/` work together, and what's involved in running this for a
problem other than `problems/hash-map/two-sum` (the only problem
currently wired up end to end).

**As of this writing, none of the steps below have actually been run
for a second problem.** The tooling has been made *capable* of it
(the problem path is a workflow input / script argument rather than a
hardcoded string), but running it for real against a new problem is a
deliberate future step, not something this document triggers on its
own.

## What exists today

- `.github/workflows/trace-poc.yml` — compiles a problem's optimized
  and brute-force drivers, runs each under GDB in batch mode, and
  commits the raw GDB output back to the repo as `github-actions[bot]`.
- `scripts/parse_gdb_trace.py <problem_dir>` — parses a problem's raw
  GDB output files into `<problem_dir>/trace_generated.json`.
- `scripts/compare_traces.py <problem_dir>` — structurally diffs
  `trace.json` (hand-written) against `trace_generated.json`
  (GDB-parsed) for a problem, ignoring explanation-text wording.

## What's parameterized vs. still problem-specific

**Parameterized (safe to reuse as-is):**
- The problem directory path — the workflow accepts it via a
  `workflow_dispatch` input (`problem_path`, defaults to
  `problems/hash-map/two-sum` so ordinary `push` events keep working
  unchanged), and both scripts take it as a positional CLI argument.

**Still specific to Two Sum (needs manual edits for a new problem):**
- The GDB breakpoint line numbers (`solution.cpp:9`, `solution.cpp:11`,
  `bruteforce_driver.cpp:14`, `bruteforce_driver.cpp:15`) — these are
  literal source line numbers for *this* problem's code and will be
  wrong for any other problem's source.
- The `-ex "print ..."` variable lists in each GDB step — different
  algorithms have different variables (Two Sum has `i`, `j`,
  `nums[i]`, `complement`; a different problem will have different
  ones).
- `scripts/parse_gdb_trace.py`'s `BREAKPOINT_MANIFESTS` /
  `FINAL_BREAKPOINT_MANIFESTS` dicts — these record, per source
  filename, the order in which variables were printed at each
  breakpoint (GDB's output has no variable names, only `$N = value`,
  so the parser needs to know the order to label them correctly).

## Steps to add a new problem later

1. Write `<problem_dir>/driver.cpp` (optimized) and
   `<problem_dir>/bruteforce_driver.cpp` (brute-force, if applicable),
   each with a real `main()` using the problem's actual example input
   — same pattern as `problems/hash-map/two-sum/driver.cpp` and
   `bruteforce_driver.cpp`.
2. Compile locally and use `gdb -batch -ex "break <file>:<line>" ...`
   to confirm the exact breakpoint line numbers resolve, the same way
   this was verified for Two Sum before committing anything (view the
   file, count lines — don't guess).
3. Edit `.github/workflows/trace-poc.yml`'s GDB steps for the new
   problem's breakpoint lines and print-variable lists (or duplicate
   the job/steps under a differently-named job if you want both
   problems traced independently).
4. Add a corresponding entry to `BREAKPOINT_MANIFESTS` /
   `FINAL_BREAKPOINT_MANIFESTS` in `scripts/parse_gdb_trace.py`,
   matching the exact `-ex "print ..."` order used in step 3.
5. Trigger the workflow manually (Actions tab → Trace POC → Run
   workflow → set `problem_path` to the new problem's directory), wait
   for it to complete, then `git pull` and confirm the raw trace
   file(s) landed.
6. Run `python3 scripts/parse_gdb_trace.py <problem_dir>` locally
   (or as an additional workflow step) to produce that problem's
   `trace_generated.json`.
7. If the problem already has a hand-written `trace.json`, run
   `python3 scripts/compare_traces.py <problem_dir>` and review the
   output before touching anything else. Never overwrite an existing
   `trace.json` based on this without explicit review — that decision
   belongs to a human, not this pipeline.
