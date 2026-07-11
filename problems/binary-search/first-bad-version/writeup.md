# First Bad Version

## Problem Description

You are a product manager leading a team to develop a new product. Unfortunately, the latest version of your product fails the quality check. Since each version is developed based on the previous version, all the versions after a bad version are also bad. Suppose you have `n` versions `[1, 2, ..., n]` and you want to find out the first bad one, which causes all the following ones to be bad. You are given an API `bool isBadVersion(version)` which returns whether a version is bad. Implement a function to find the first bad version. You should minimize the number of calls to the API.

## Approach: Binary Search on the Answer

This problem maps directly to binary search because the versions form a monotone sequence: all versions before the first bad one are good, and all versions from the first bad one onward are bad. This creates a clear partition point that binary search can locate in $O(\log n)$ API calls.

1.  Initialize `low = 1` and `high = n`.
2.  Compute `mid = low + (high - low) / 2` (using the overflow-safe formula).
3.  If `isBadVersion(mid)` returns `true`, the first bad version is `mid` or earlier — set `high = mid`.
4.  If `isBadVersion(mid)` returns `false`, the first bad version must be after `mid` — set `low = mid + 1`.
5.  Repeat until `low == high`, at which point `low` is the first bad version.

The key invariant is that `low` always points to a candidate for the first bad version, and `high` always points to a known-bad version (or `n`). When they converge, we have the answer.

## Why this pattern

A linear scan would call `isBadVersion` up to $n$ times. Binary search reduces this to $O(\log n)$ calls by exploiting the monotonicity of the predicate. The "answer space" (version numbers) is sorted and the predicate (`isBadVersion`) is monotone — exactly the conditions binary search requires.

## Complexity

- **Time Complexity**: $O(\log n)$ — each iteration halves the search space.
- **Space Complexity**: $O(1)$ — only three integer variables are used.
