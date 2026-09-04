// Driver program for the brute-force Two Sum II trace.
// This deliberately checks every pair with nested loops; the displayed
// solution.cpp remains the optimized two-pointer implementation.
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
    std::vector<int> nums = {2, 7, 11, 15};
    int target = 9;

    std::vector<int> result = Solution().twoSum(nums, target);

    std::cout << "Result: [";
    for (size_t i = 0; i < result.size(); i++) {
        std::cout << result[i];
        if (i + 1 < result.size()) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    return 0;
}
