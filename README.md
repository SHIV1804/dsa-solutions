# DSA Solutions Repository

This repository contains solutions to various Data Structures and Algorithms (DSA) problems, organized by patterns and problem types.

## Repository Structure

The problems are organized in the following directory structure:

```
/problems/<pattern-slug>/<problem-slug>/
  meta.md        — Metadata about the problem (frontmatter)
  solution.cpp   — The actual code solution (C++ by default)
  writeup.md     — Detailed approach, pattern reasoning, and complexity analysis
```

## Problem Convention

Each problem must include three files:

### 1. `meta.md`
Contains YAML frontmatter with the following fields:
- `title`: Problem name
- `leetcodeNumber`: The LeetCode problem number
- `leetcodeUrl`: Direct link to the problem
- `difficulty`: Easy, Medium, or Hard
- `pattern`: The algorithmic pattern (e.g., `two-pointers`, `sliding-window`, `binary-search`)
- `tags`: List of relevant tags
- `dateSolved`: The date the problem was solved
- `exampleInput`: A nested object defining a sample input for the visualizer.

#### `exampleInput` Shapes by Pattern:
| Pattern | `exampleInput` Shape |
|---|---|
| `two-pointers` | `{ array: number[], target?: number }` |
| `sliding-window` | `{ array: number[], k?: number, target?: number }` |
| `binary-search` | `{ array: number[], target: number }` |

### 2. `solution.cpp`
The implementation of the solution. Ensure the code is clean and follows standard naming conventions.

### 3. `writeup.md`
A markdown file explaining:
- **Approach**: How the problem was solved.
- **Why this pattern**: Why this specific pattern was chosen or is relevant.
- **Complexity**: Time and Space complexity analysis.

## Contribution Guidelines
When adding new solutions, ensure you follow the directory structure and provide accurate metadata in `meta.md` to ensure compatibility with the portfolio visualizer.
