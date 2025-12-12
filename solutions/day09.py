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

    def square_distance(self, a, b):
        x1, y1 = a
        x2, y2 = b
        return (x2 - x1) ** 2 + (y2 - y1) ** 2

    def sort_vecs(self, a: vec2, b: vec2) -> tuple[vec2, vec2]:
        """
        Returns (top-left, bottom-right) expression of square described by a, b.
        """
        x1, x2 = (a[0], b[0]) if a[0] < b[0] else (b[0], a[0])
        y1, y2 = (a[1], b[1]) if a[1] < b[1] else (b[1], a[1])
        return (x1, y1), (x2, y2)

    def aabb_intersect(self, a1, a2, b1, b2) -> bool:
        """Use AABB collision detection to see if line segment intersects rect"""
        return not (
            a1[0] >= b2[0]  # a right of b
            or a2[0] <= b1[0]  # a left of b
            or a2[1] <= b1[1]  # a above b
            or a1[1] >= b2[1]  # a below b
        )

    def intersects_any_segment(self, rect1_idx, rect2_idx, segments):
        """
        Test given rect against all line segments.
        Return if no line segments intersect.
        """
        a1, a2 = self.sort_vecs(self.data[rect1_idx], self.data[rect2_idx])
        for b1, b2 in segments:
            if self.aabb_intersect(a1, a2, b1, b2):
                return True

        return False

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
                heap.append((-self.area(self.data[i], self.data[j]), i, j))
        heapq.heapify(heap)

        # Return the first result from heap where no line segments intersect
        # Get segments, pre-"sort" the points for easier AABB, and sort by length.
        # Length optimization -> longer = more likely to intersect something.
        segments = []
        for i in range(self.size):
            segments.append(self.sort_vecs(self.data[i - 1], self.data[i]))
        segments.sort(key=lambda a: -self.square_distance(a[0], a[1]))

        for _ in range(len(heap)):
            area, a_idx, b_idx = heapq.heappop(heap)

            if not self.intersects_any_segment(a_idx, b_idx, segments):
                return -area

        return -1


if __name__ == "__main__":
    Solution("input/day09.txt").solve(2, benchmark=5)
