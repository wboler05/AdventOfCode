#include <iostream>
#include <unordered_map>
#include <vector>

size_t get_nth_number(const std::vector<size_t> & input_vector, const size_t & N) {
    std::unordered_map<size_t, size_t> memo;
    size_t cur_num = 0;
    for (size_t i = 0; i < N-1; ++i) {
        if (i < input_vector.size()) {
            cur_num = input_vector[i];
        }
        auto it = memo.find(cur_num);
        if (it == memo.end()) {
            memo[cur_num] = i;
            cur_num = 0;
        } else {
            auto delta = i - memo[cur_num];
            memo[cur_num] = i;
            cur_num = delta;
        }
    }
    return cur_num;
}

int main(int argc, char * argv[]) {

    std::vector<size_t> input_vector{18,11,9,0,5,1};
    size_t n = 30000000;

    auto num = get_nth_number(input_vector, n);
    std::cout << "Number: " << num << std::endl;

    return 0;
}