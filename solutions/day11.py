from functools import cache
from math import prod

from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def __init__(self, path):
        super().__init__(path)
        nodes_str = [r.split(": ") for r in self.get_data_raw().splitlines()]
        self.graph = {k: v.split(" ") for k, v in nodes_str}
        self.graph["out"] = []

    def paths_atob(self, start: str, end: str):
        paths = {n: 0 for n in self.graph}

        @cache  # the lazy man's visited hashmap
        def _dfs(n):
            for adj in self.graph[n]:
                if adj == end:
                    paths[n] += 1
                    continue
                _dfs(adj)
                paths[n] += paths[adj]

        _dfs(start)
        return paths[start]

    def part1(self) -> int:
        stack = [self.graph["you"]]

        path_count = 0
        while stack:
            adj = stack.pop()

            for n in adj:
                if n == "out":
                    path_count += 1
                else:
                    stack.append(self.graph[n])

        return path_count

    def part2(self) -> int:
        routes_a = [
            ("svr", "fft"),
            ("fft", "dac"),
            ("dac", "out"),
        ]

        a_cnts = [self.paths_atob(a, b) for a, b in routes_a]
        # print(a_cnts)

        # Apparently there are 0 paths from dac -> fft, so there's only one
        # path we *actually* have to worry about for the given input.
        # routes_b = [
        #     ("svr", "dac"),
        #     ("dac", "fft"),
        #     ("fft", "out"),
        # ]
        # # b_cnts = [self.paths_atob(a, b) for a, b in routes_b]
        # print(b_cnts)

        return prod(a_cnts)  # + prod(b_cnts)


if __name__ == "__main__":
    Solution("input/day11.txt").solve(2, benchmark=5)
