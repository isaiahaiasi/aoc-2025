from math import prod  # Just makes things a little prettier...

from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def part1(self):
        raw_input_list = [s.split() for s in self.get_data_lines()]
        num_rows = [[int(n) for n in r] for r in raw_input_list[:-1]]
        cmd_rows = raw_input_list[-1]

        result = 0
        for i in range(len(cmd_rows)):
            if cmd_rows[i] == "*":
                result += prod(num_rows[j][i] for j in range(len(num_rows)))
            else:
                result += sum(num_rows[j][i] for j in range(len(num_rows)))
        return result

    def part2(self):
        # Get each row as a raw string
        raw = [line.rstrip("\n") for line in self.get_data_lines()]
        raw_nums = raw[:-1]
        cmds = raw[-1]

        # Go through columns in reverse,
        # keeping track of the list of numbers for the current problem.
        # If the column has an operator, apply to list & add to total result.
        # If the column of numbers cannot be cast as int, it's blank,
        # which means we're moving onto the next problem & can reset nums list.
        nums = []
        result = 0
        for col in range(len(raw[0]) - 1, -1, -1):
            try:
                num = int("".join([row[col] for row in raw_nums]))
                nums.append(num)
                if cmds[col] == "*":
                    result += prod(nums)
                elif cmds[col] == "+":
                    result += sum(nums)
            except ValueError:
                nums = []

        return result


if __name__ == "__main__":
    Solution("input/day06.txt").solve(2, benchmark=1000)
