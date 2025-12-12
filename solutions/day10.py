# ruff: noqa: F403
# ruff: noqa: F405
from collections import deque

from z3 import *

from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def part1_parse(self) -> list[int, list[int]]:
        """
        Parse goal state & each button as single ints.
        - eg [.##.] = 0b0110 = 6
        - eg (2, 3) = 0b1100 (2nd & 3rd indices from 0)= 12
        Then we can just XOR current state & a button to update the state.
        """
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

    def part2_parse(self):
        rows = []
        for row in self.get_data_raw().splitlines():
            jolt_idx = row.rfind(" ") + 2
            joltages = [int(n) for n in row[jolt_idx:-1].split(",")]

            buttons = []
            i = row.index(" ") + 1
            while True:
                if row[i] != "(":
                    break
                j = row.index(")", i + 1)
                buttons.append([int(n) for n in row[i + 1 : j].split(",")])
                i = j + 2

            rows.append((joltages, buttons))
        return rows

    def part1(self) -> int:
        def solve_row(goal_state: int, buttons: list[int]) -> int:
            """:return: fewest steps to goal"""
            # Traverse state machine with BFS, keeping visited table to kill dead ends.
            # (Maybe more optimal to track visited buttons in each path, since we
            # don't want to revisit buttons, but that involves a lot more lists
            # and (for me) slower total runtime.

            visited = [False] * 1024  # max state size of input

            # initial state = first pressed button
            queue = deque(buttons)
            steps = 0
            while queue:
                steps += 1
                # avoid packing steps into each queued item with sub-loop
                for _ in range(len(queue)):
                    state = queue.popleft()

                    if state == goal_state:
                        return steps

                    for btn in buttons:
                        # XOR state int with button int to flip lights.
                        next_state = state ^ btn
                        if not visited[next_state]:
                            visited[next_state] = True
                            queue.append(next_state)

            return -1

        return sum([solve_row(g, b) for g, b in self.part1_parse()])

    def part2(self) -> int:
        """
        I don't know squat about linear algebra or systems of equations,
        so I straight up cheated on this one. Sorry (not that sorry).
        """
        total = 0
        for joltages, buttons in self.part2_parse():
            solver = Solver()
            bvars = [Int(f"a{n}") for n in range(len(buttons))]
            for b in bvars:
                solver.add(b >= 0)

            for i, v in enumerate(joltages):
                vvars = [bvars[j] for j, btn in enumerate(buttons) if i in btn]
                solver.add(Sum(vvars) == v)

            while solver.check() == sat:
                model = solver.model()
                n = sum([model[d].as_long() for d in model])
                solver.add(Sum(bvars) < n)

            total += n

        return total


if __name__ == "__main__":
    Solution("input/day10.txt").solve(2)
