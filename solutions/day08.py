from collections import Counter
from math import prod

from utils.SolutionBase import SolutionBase

IS_SAMPLE = False


class UnionFind:
    def __init__(self, size: int):
        self.parents = [i for i in range(size)]  # Each points to itself at first
        self.sizes = [1] * size  # The size of each union is 1 to start

    def find(self, i: int) -> int:
        """
        Find the parent of vertex i
        (Also flattens the tree as an optimization - "Path Compression")
        """
        if i != self.parents[i]:
            self.parents[i] = self.find(self.parents[i])
        return self.parents[i]

    def union(self, i: int, j: int) -> bool:
        """
        Joins vertex i & j into a single Union.
        Returns if i & j were NOT already a Union.
        """
        pi, pj = self.find(i), self.find(j)
        if pi == pj:
            return False

        # Merge the smaller tree into the larger one.
        if self.sizes[i] < self.sizes[pj]:
            self.parents[pi] = self.find(self.parents[pj])
            self.sizes[pj] += self.sizes[pi]
        else:
            self.parents[pj] = self.find(self.parents[pi])
            self.sizes[pi] += self.sizes[pj]

        return True

    def has_disjoint(self):
        v = self.parents[0]
        return not all(n == v for n in self.parents)


class Solution(SolutionBase):
    def __init__(self, path):
        super().__init__(path)
        self.data = [list(map(int, d.split(","))) for d in self.get_data_lines()]
        self.size = len(self.data)

    def square_distance(self, vi1: int, vi2: int):
        x1, y1, z1 = self.data[vi1]
        x2, y2, z2 = self.data[vi2]
        return (x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2

    def get_distances(self) -> list[tuple[int, int, int]]:
        """Returns a sorted (ascend.) list of (distance, node_idx, node_idx)"""
        distances = []  # (d, v1_idx, v2_idx)
        for i_idx in range(self.size):
            for j_idx in range(i_idx + 1, self.size):
                if j_idx == i_idx:
                    continue
                d = self.square_distance(i_idx, j_idx)
                distances.append((d, i_idx, j_idx))
        distances.sort()
        return distances

    def part1(self) -> int:
        # 1. Get sorted distances.
        # 2. Build graph of connections using Union-Find to easily get disjoint set.
        # 3. Get size of all unions, sort, RETURN prod([top 3])
        distances = self.get_distances()

        unionfind = UnionFind(self.size)
        x = 0
        while x < (10 if IS_SAMPLE else 1000):
            _, i_idx, j_idx = distances[x]
            unionfind.union(i_idx, j_idx)
            x += 1

        counts = Counter([unionfind.find(i) for i in range(self.size)])
        return prod([c for _, c in counts.most_common(3)])

    def part2(self) -> int:
        # 1. Get sorted distances.
        # 2. Add edges to unionfind.
        # 3. Return answer whenever number of disjoint sets in unionfind is 1.
        distances = self.get_distances()
        unionfind = UnionFind(self.size)
        while distances:
            _, i_idx, j_idx = distances.pop(0)
            unionfind.union(i_idx, j_idx)

            # unionfind.parents is not perfectly flat,
            # so we still have to find() each parent
            for i in range(i_idx + 1, j_idx):
                unionfind.find(i)

            # We know all vertices are in the same circuit if they all have the same parent.
            if not unionfind.has_disjoint():
                return self.data[i_idx][0] * self.data[j_idx][0]
        return -1


if __name__ == "__main__":
    path = "sample-input/day08.txt" if IS_SAMPLE else "input/day08.txt"
    Solution(path).solve(1, benchmark=1)
    Solution(path).solve(2, benchmark=1)
