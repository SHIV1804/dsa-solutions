// Driver program for the Two Sum II (sorted array, two-pointer)
// solution.
//
// solution.cpp as currently committed has a stray backslash before the
// reference operator in its parameter list
// ("std::vector<int>\& numbers"), which is invalid C++ and fails to
// compile (confirmed: g++ reports "stray '\' in program" at that
// line). Rather than #include-ing the broken file, or editing
// solution.cpp itself (it's the real displayed solution elsewhere on
// the site), this duplicates the class body here with only that
// escaping artifact removed -- the algorithm/logic is otherwise
// identical, unchanged.
#include <iostream>
#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& numbers, int target) {
        int left = 0;
        int right = numbers.size() - 1;

        while (left < right) {
            int currentSum = numbers[left] + numbers[right];

            if (currentSum == target) {
                return {left + 1, right + 1}; // 1-indexed
            } else if (currentSum < target) {
                left++;
            } else {
                right--;
            }
        }

        return {};
    }
};

int main() {
    std::vector<int> numbers = {2, 7, 11, 15};
    int target = 9;

    std::vector<int> result = Solution().twoSum(numbers, target);

    std::cout << "Result: [";
    for (size_t i = 0; i < result.size(); i++) {
        std::cout << result[i];
        if (i + 1 < result.size()) std::cout << ", ";
    }
    std::cout << "]" << std::endl;

    return 0;
}
