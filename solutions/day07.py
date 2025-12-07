from functools import lru_cache

from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def __init__(self, path):
        super().__init__(path)
        self.data: list[str] = [r.strip() for r in self.get_data_lines()]

    def part1(self) -> int:
        beams = [False] * len(self.data[0])
        start_idx = self.data[0].index("S")
        beams[start_idx] = True
        splits = 0
        for r in range(2, len(self.data), 2):
            tmp_beams = [b for b in beams]
            debug_line = ["|" if b else "." for b in beams]
            for c in range(len(self.data[r])):
                if beams[c] and self.data[r][c] == "^":
                    # (source data has buffer to avoid overflow)
                    splits += 1
                    tmp_beams[c] = False
                    tmp_beams[c - 1] = True
                    tmp_beams[c + 1] = True
                    if not beams[c - 1] or not beams[c + 1]:
                        debug_line[c] = "^"
                    else:
                        debug_line[c] = "X"
            beams = tmp_beams
            print("".join(debug_line))
            print("".join(["|" if b else "." for b in beams]))
        return splits

    # I really wanted to make a recursive solution work.
    # IDK why.
    def part2_lru(self) -> int:
        @lru_cache
        def recurse(r: int, c: int, timelines: int):
            if r >= len(self.data):
                return timelines

            if self.data[r][c] == "^":
                return recurse(r + 2, c - 1, timelines) + recurse(
                    r + 2, c + 1, timelines
                )
            else:
                return recurse(r + 2, c, timelines)

        start_idx = self.data[0].index("S")
        return recurse(2, start_idx, 1)

    # My part 1 actually gave me 99% of what I needed for part 2,
    # I just needed to track the number of overlapping beams.
    def part2(self) -> int:
        beams = [False] * len(self.data[0])
        start_idx = self.data[0].index("S")
        beams[start_idx] = 1
        for r in range(2, len(self.data), 2):
            tmp_beams = [b for b in beams]
            for c in range(len(self.data[r])):
                if beams[c] and self.data[r][c] == "^":
                    tmp_beams[c] = 0
                    tmp_beams[c - 1] += beams[c]
                    tmp_beams[c + 1] += beams[c]
            beams = tmp_beams
        return sum(beams)


if __name__ == "__main__":
    Solution("input/day07.txt").solve(2, benchmark=100)
