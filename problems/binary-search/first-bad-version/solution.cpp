/*
 * First Bad Version
 * LeetCode 278 — Easy
 *
 * Versions are numbered 1..n. Starting from some version, every version
 * from that point onward is "bad". We must find the first bad version
 * using the fewest calls to the `isBadVersion` API.
 *
 * This is a textbook binary-search problem on the answer space.
 * If version `mid` is bad, the first bad version is at `mid` or earlier
 * (move `high = mid`). If `mid` is good, it must be after `mid`
 * (move `low = mid + 1`). The loop converges on the boundary.
 *
 * Note: The solution uses `long long` for `mid` computation to avoid
 * integer overflow when `n` is large.
 */

// Forward declaration.
bool isBadVersion(int version);

class Solution {
public:
    int firstBadVersion(int n) {
        long long low = 1;
        long long high = n;

        while (low < high) {
            long long mid = low + (high - low) / 2;

            if (isBadVersion((int)mid)) {
                // First bad version is mid or earlier.
                high = mid;
            } else {
                // First bad version must be after mid.
                low = mid + 1;
            }
        }

        return (int)low;
    }
};
