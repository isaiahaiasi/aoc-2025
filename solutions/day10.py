from collections import deque

from utils.SolutionBase import SolutionBase

"""
- Save goal state as a binary number: eg [.##.] = 0b0110 = 6
- Treat buttons as binary numbers too: eg (2, 3) = 0b1100 = 12
- Update state of lights by XORing button number with state number.
"""


class Solution(SolutionBase):
    def parse(self) -> list[int, list[int]]:
        rows = []
        for row in self.get_data_lines():
            goal_end = row.index(" ")
            goal_str = ["1" if c == "#" else "0" for c in row[1 : goal_end - 1]]
            goal_state = int("".join(reversed(goal_str)), 2)

            buttons = []
            i = goal_end + 1
            while True:
                if row[i] != "(":
                    break
                end = row.index(")", i + 1)
                flip_indices = [int(n) for n in row[i + 1 : end].split(",")]
                btn_str = ["0"] * 10
                for i in flip_indices:
                    btn_str[9 - i] = "1"

                buttons.append(int("".join(btn_str), 2))
                i = end + 2

            rows.append((goal_state, buttons))
        return rows

    def part1_solverow(self, goal_state: list[bool], buttons: list[list[int]]) -> int:
        """:return: fewest steps to goal"""
        # Traverse state machine with BFS, keeping visited table to kill dead ends

        visited = [False] * 1024  # max state size of input
        queue = deque([(1, btn) for btn in buttons])
        while queue:
            dist, state = queue.popleft()

            if state == goal_state:
                # print(bin(goal_state), dist)
                return dist

            for btn in buttons:
                next_state = state ^ btn
                if not visited[next_state]:
                    visited[state] = True
                    queue.append((dist + 1, next_state))

        return -1

    def part1(self) -> int:
        return sum([self.part1_solverow(g, b) for g, b in self.parse()])

    def part2(self) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    Solution("input/day10.txt").solve(1, benchmark=1)
