# Longest Substring Without Repeating Characters

## Problem Description

Given a string `s`, find the length of the longest substring without repeating characters. For example, given `"abcabcbb"`, the answer is `3` because the longest substring without repeating characters is `"abc"`.

## Approach: Sliding Window with Hash Map

This is a classic sliding-window problem where we need to find the longest contiguous segment satisfying a constraint (no duplicate characters). The key insight is that we can expand a window `[left, right]` and shrink it only when we violate the constraint, rather than re-checking every possible substring.

1.  Maintain two pointers, `left` and `right`, defining the current window.
2.  Maintain a hash map `lastSeen` that records the most recent index at which each character appeared.
3.  Expand `right` one character at a time. If `s[right]` has been seen before at an index `>= left`, it is a duplicate inside the current window — shrink by moving `left` to `lastSeen[s[right]] + 1`.
4.  After resolving any duplicate, record the character's new position in `lastSeen`.
5.  Update `maxLen` with the current window length `right - left + 1`.

The hash map ensures that shrinking the window is an $O(1)$ operation rather than scanning the window contents.

## Why this pattern

A brute-force check of all substrings would be $O(n^3)$ or $O(n^2)$. The sliding window avoids re-examining valid prefixes: once we know `[left, right]` is valid, we only need to handle the single new character `s[right+1]`. The constraint "no repeating characters" is *monotone* in the sense that if `[left, right]` contains a duplicate, then `[left, right+1]` also contains a duplicate — so we only ever need to advance `left`, never reset it.

## Complexity

- **Time Complexity**: $O(n)$ — each character is visited exactly once by `right`, and `left` only advances.
- **Space Complexity**: $O(min(n, m))$ where $m$ is the character set size — the hash map stores at most one entry per distinct character.
