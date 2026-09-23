# AGENTS.md

Instructions for AI coding agents working in this repository.

## What this repo is
Data-structures-and-algorithms solutions, organized by pattern, consumed at request time by a separate Next.js portfolio (`SHIV1804/Portfolio`, `shared/lib/dsa-sync.ts`) via the GitHub REST API. See `README.md` for the full directory/frontmatter convention.

## The contract you must not break
Each problem is `problems/<pattern-slug>/<problem-slug>/` containing `meta.md` (YAML frontmatter), `solution.cpp` (or another language), and `writeup.md`. The portfolio's `DSAProblem`/`DSATrace` TypeScript interfaces are the schema this data must satisfy — a field renamed or removed here silently breaks that site. If you change `meta.md`'s frontmatter shape or `trace.json`'s structure, the change must be mirrored in the portfolio repo's `shared/lib/dsa-sync.ts`.

## `trace.json` and the GDB pipeline
A subset of problems (currently `hash-map/two-sum`, `two-pointers/two-sum-ii-input-array-is-sorted`) have a GDB-verified `trace.json` powering an interactive step-by-step visualizer on the portfolio site. The pipeline for producing one is documented in `problems/GDB_TRACE_PIPELINE.md` — read it before creating or regenerating a trace. Traces are meant to reflect real GDB-observed program state, not hand-written/simulated data.

## CI: `.github/workflows/generate-traces.yml`
Auto-regenerates `trace.json` on a push that touches one of a **fixed, explicit list** of `solution.cpp` paths (currently the two problems above) — intentionally not every problem folder, so a new, not-yet-wired-up problem never silently triggers a GDB run against a `driver.cpp`/breakpoint setup that doesn't exist yet. To opt a new problem into auto-trace-on-push, wire it up per `GDB_TRACE_PIPELINE.md`, then add its `solution.cpp` path to both the `on.push.paths` list and the `WATCHED_SOLUTIONS` array in the workflow file — keep those two lists in sync. A `workflow_dispatch` manual run is available for problems not on the watched list.

## DO
- Follow the existing `meta.md` frontmatter shape exactly (see `README.md`'s `exampleInput` shape table, which differs by pattern).
- Keep `solution.cpp` clean and use standard naming conventions, per `README.md`.

## DO NOT
- Do not add a new pattern value to `meta.md` without also adding a corresponding case in the portfolio's `widgets/dsa/ui/PatternVisualizer.tsx` — otherwise the problem will render with "No visualizer available."
- Do not hand-author `trace.json` data as if it came from GDB — see `GDB_TRACE_PIPELINE.md`.
