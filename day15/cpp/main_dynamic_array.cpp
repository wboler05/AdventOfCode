#include <iostream>
#include <vector>

typedef size_t word;

bool check(const std::vector<word> & vec, const word & key) {
    if (key >= vec.size()) {
        return false;
    } else if (vec[key] == (word) -1) {
        return false;
    } else {
        return true;
    }
}

void set(std::vector<word> & vec, const word & key, const word & value) {
    while (2*key >= vec.size()) {
        vec.resize(2 * vec.size()+1, -1);
    }
    vec[key] = value;
}

word get(const std::vector<word> & vec, const word & key) {
    if (key >= vec.size()) {
        return (word) -1;
    } else {
        return vec[key];
    }
}

word get_nth_number(const std::vector<word> & input_vector, const word & N) {
    std::vector<word> memo;
    word cur_num = 0;
    for (word i = 0; i < N-1; ++i) {
        if (i < input_vector.size()) {
            cur_num = input_vector[i];
        }
        if (!check(memo, cur_num)) {
            set(memo, cur_num, i);
            cur_num = 0;
        } else {
            auto delta = i - get(memo, cur_num);
            set(memo, cur_num, i);
            cur_num = delta;
        }
    }
    return cur_num;
}

int main(int argc, char * argv[]) {

    std::vector<word> input_vector{18,11,9,0,5,1};
    word n = 30000000;

    auto num = get_nth_number(input_vector, n);
    std::cout << "Number: " << num << std::endl;

    return 0;
}