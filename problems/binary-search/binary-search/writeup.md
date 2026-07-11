# Binary Search

## Problem Description
Given a sorted array of integers `nums` and a `target`, return the index of the target if it exists, otherwise return -1.

## Approach: Binary Search
Since the array is sorted, we can use binary search to find the target in logarithmic time. We maintain a range `[low, high]` and check the middle element.

## Complexity
- **Time Complexity**: $O(\log n)$ - We halve the search space at each step.
- **Space Complexity**: $O(1)$ - Constant extra space.
