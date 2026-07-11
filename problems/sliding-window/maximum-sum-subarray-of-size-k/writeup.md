# Maximum Sum Subarray of Size K

## Problem Description
Given an array of integers and a number K, find the maximum sum of a contiguous subarray of size K.

## Approach: Sliding Window
We can use a sliding window of size K. We keep track of the current window sum. As we move the window forward, we add the new element and subtract the element that is no longer in the window.

## Complexity
- **Time Complexity**: $O(n)$ - Single pass through the array.
- **Space Complexity**: $O(1)$ - Only constant extra space.
