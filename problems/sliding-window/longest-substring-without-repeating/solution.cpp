/*
 * Longest Substring Without Repeating Characters
 * LeetCode 3 — Medium
 *
 * We maintain a sliding window [left, right] over the input string.
 * A hash map tracks the last index where each character was seen.
 * When we encounter a duplicate inside the current window, we shrink
 * the window by moving `left` to one past the previous occurrence.
 * At each step we record the window length and keep the maximum.
 */

#include <string>
#include <unordered_map>
#include <algorithm>

using namespace std;

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        unordered_map<char, int> lastSeen;
        int left = 0;
        int maxLen = 0;

        for (int right = 0; right < (int)s.size(); right++) {
            char c = s[right];

            // If the character was seen inside the current window,
            // move left past it.
            if (lastSeen.count(c) && lastSeen[c] >= left) {
                left = lastSeen[c] + 1;
            }

            // Record the current character's position.
            lastSeen[c] = right;

            // Update the maximum window length.
            maxLen = max(maxLen, right - left + 1);
        }

        return maxLen;
    }
};
