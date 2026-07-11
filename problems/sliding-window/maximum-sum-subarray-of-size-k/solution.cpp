#include <vector>
#include <algorithm>

class Solution {
public:
    long maximumSumSubarray(int K, std::vector<int>& Arr) {
        long maxSum = 0;
        long windowSum = 0;
        int start = 0;
        
        for (int end = 0; end < Arr.size(); end++) {
            windowSum += Arr[end];
            
            if (end >= K - 1) {
                maxSum = std::max(maxSum, windowSum);
                windowSum -= Arr[start];
                start++;
            }
        }
        
        return maxSum;
    }
};
