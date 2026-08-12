// Driver program for the Two Sum solution.
// Kept separate from solution.cpp so the displayed solution file
// stays exactly as authored, with no test/harness code appended to it.
#include <iostream>
#include "solution.cpp"

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
