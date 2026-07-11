# Two Sum - Approach and Analysis

## Approach
The problem asks us to find two indices such that the numbers at these indices add up to a given target. 
While a brute-force approach would involve nested loops ($O(n^2)$), we can optimize this using a **Hash Map** to store the numbers we've seen so far and their corresponding indices.

For each number `nums[i]`, we calculate its `complement` ($target - nums[i]$). If the `complement` exists in our map, we've found the pair and return their indices.

## Why this Pattern?
Although this specific problem is often solved with a Hash Map, it is categorized under **two-pointers** because if the input array were sorted, we could use a classic two-pointer approach (left and right) to find the sum in $O(n)$ time with $O(1)$ space. In this repository, we use this example to demonstrate the metadata convention for two-pointer related problems.

## Complexity
- **Time Complexity**: $O(n)$ where $n$ is the number of elements in the array. We traverse the list once.
- **Space Complexity**: $O(n)$ to store the hash map.
