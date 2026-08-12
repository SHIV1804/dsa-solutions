// Driver program for the brute-force Two Sum solution.
// The Solution class below is an exact match of trace.json's
// "bruteForce.code" array, kept separate from solution.cpp (which
// holds the optimized hash-map version actually displayed as the
// solution elsewhere on the site).
#include <iostream>
#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        for (int i = 0; i < nums.size(); i++) {
            for (int j = i + 1; j < nums.size(); j++) {
                if (nums[i] + nums[j] == target) {
                    return {i, j};
                }
            }
        }
        return {};
    }
};

int main() {
    std::vector<int> nums = {3, 2, 4};
    int target = 6;

    std::vector<int> result = Solution().twoSum(nums, target);

    std::cout << "Result: [";
    for (size_t i = 0; i < result.size(); i++) {
        std::cout << result[i];
        if (i + 1 < result.size()) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    return 0;
}
