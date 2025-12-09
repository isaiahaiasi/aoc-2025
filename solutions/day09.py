import heapq

from utils.SolutionBase import SolutionBase

type vec2 = tuple[int, int]


class Solution(SolutionBase):
    def __init__(self, path):
        super().__init__(path)

        self.data = [tuple(map(int, r.split(","))) for r in self.get_data_lines()]
        """List of red tiles"""
        self.size = len(self.data)
        """Number of red tiles"""
        self.width = max([x for x, _ in self.data])
        """Greatest tile x position"""
        self.height = max([y for _, y in self.data])
        """Greatest tile y position"""

    def area(self, a: vec2, b: vec2) -> int:
        """*Inclusive* area of square defined by (a, b)"""
        x1, y1 = a
        x2, y2 = b
        return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)

    def sort_vecs(self, a: vec2, b: vec2) -> tuple[vec2, vec2]:
        """
        Returns (top-left, bottom-right) expression of square described by a, b.
        """
        x1, x2 = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])
        y1, y2 = (a[1], b[1]) if a[1] < b[1] else (b[1], a[1])
        return (x1, y1), (x2, y2)

    def inside(self, a: vec2, b: vec2, v: int) -> bool:
        """
        Return if point v is inside the rect defined by (a, b)
        (Sharing an edge does not count as "inside")
        """
        return a[0] < v[0] < b[0] and a[1] < v[1] < b[1]

    def intersect_rect(self, rect1: vec2, rect2: vec2, line1: vec2, line2: vec2):
        """Return if line (line1, line2) intersects rect (rect1, rect1)"""
        # 1. either b1 or b2 is inside (a1, a2)
        if self.inside(rect1, rect2, line1) or self.inside(rect1, rect2, line2):
            return True

        # 2. vertical line intersects (without either point specifically inside)
        if line1[0] == line2[0] and rect1[0] < line1[0] < rect2[0]:
            if line1[1] <= rect1[1] and line2[1] >= rect2[1]:
                return True

        # 3. horizontal line intersects (without either point specifically inside)
        if line1[1] == line2[1] and rect1[1] < line1[1] < rect2[1]:
            if line1[0] <= rect1[0] and line2[0] >= rect2[0]:
                return True

        return False

    def no_lines_intersect_rect(self, rect1_idx: int, rect2_idx: int) -> bool:
        """
        Test given rect against all line segments.
        Return if no line segments intersect.
        """
        a1, a2 = self.sort_vecs(self.data[rect1_idx], self.data[rect2_idx])
        for i in range(self.size):
            b1, b2 = self.sort_vecs(self.data[i - 1], self.data[i])
            if self.intersect_rect(a1, a2, b1, b2):
                return False

        return True

    def part1(self) -> int:
        # naive n^2 solution because why not
        res = 0
        for v1 in self.data:
            for v2 in self.data:
                res = max(res, self.area(v1, v2))

        return res

    def part2(self) -> int:
        # Get min-heap of the negative area of all rects
        heap = []
        for i in range(self.size):
            for j in range(i + 1, self.size):
                heapq.heappush(heap, (-self.area(self.data[i], self.data[j]), i, j))

        # Go through the heap and return the first result where no line segments intersect
        for _ in range(len(heap)):
            area, a_idx, b_idx = heapq.heappop(heap)

            if self.no_lines_intersect_rect(a_idx, b_idx):
                # print(-area, self.data[a_idx], self.data[b_idx], a_idx, b_idx)
                return -area

        return -1


if __name__ == "__main__":
    Solution("input/day09.txt").solve(2, benchmark=1)
