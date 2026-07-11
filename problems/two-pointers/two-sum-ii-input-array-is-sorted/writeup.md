# Two Sum II - Input Array Is Sorted

## Problem Description
Given a 1-indexed array of integers `numbers` that is already sorted in non-decreasing order, find two numbers such that they add up to a specific `target` number.

## Approach: Two Pointers
Since the array is already sorted, we can use two pointers to find the target sum in $O(n)$ time and $O(1)$ space.

1.  Initialize `left` pointer at the beginning (index 0).
2.  Initialize `right` pointer at the end (index `n-1`).
3.  Calculate the `currentSum = numbers[left] + numbers[right]`.
4.  If `currentSum == target`, we found the pair.
5.  If `currentSum < target`, we need a larger sum, so move `left` pointer forward (`left++`).
6.  If `currentSum > target`, we need a smaller sum, so move `right` pointer backward (`right--`).

## Complexity
- **Time Complexity**: $O(n)$ - We traverse the array at most once.
- **Space Complexity**: $O(1)$ - We only use two pointer variables.
