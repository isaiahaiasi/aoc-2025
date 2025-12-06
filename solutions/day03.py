from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        result = 0
        for r in [r.strip() for r in self.get_data_lines()]:
            v1 = max(r[:-1])
            i = r.index(v1)
            v2 = max(r[i + 1 :])
            print(r, v1, i, v2, v1 + v2)
            result += int(v1 + v2)

        return result

    def part2(self):
        result = 0

        for r in [r.strip() for r in self.get_data_lines()]:
            num = ""
            cur = 0
            for i in range(0, 12):
                dig = max(r[cur : len(r) + i - 11])
                cur += r[cur:].index(dig) + 1
                num += dig
            result += int(num)
        return result


if __name__ == "__main__":
    path = "input/day03.txt"
    Solution(path).solve(2)
