from math import prod

from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def __init__(self, path):
        super().__init__(path)
        nodes_str = [r.split(": ") for r in self.get_data_raw().splitlines()]
        self.graph = {k: v.split(" ") for k, v in nodes_str}
        self.graph["out"] = []

    def paths_atob(self, a: str, b: str):
        paths = {n: 0 for n in self.graph}
        visited = {n: False for n in self.graph}

        def _dfs(n):
            visited[n] = True
            for adj in self.graph[n]:
                if adj == b:
                    paths[n] += 1
                    continue
                if not visited[adj]:
                    _dfs(adj)
                paths[n] += paths[adj]

        _dfs(a)
        return paths[a]

    def part1(self) -> int:
        """Goal: traverse a graph. That's it?"""
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
        routes_b = [
            ("svr", "dac"),
            ("dac", "fft"),
            ("fft", "out"),
        ]

        a_cnts = [self.paths_atob(a, b) for a, b in routes_a]
        b_cnts = [self.paths_atob(a, b) for a, b in routes_b]
        print(a_cnts)
        print(b_cnts)

        return prod(a_cnts) + prod(b_cnts)


if __name__ == "__main__":
    Solution("input/day11.txt").solve(2)
