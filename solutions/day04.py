from utils.SolutionBase import SolutionBase

OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Solution(SolutionBase):
    def get_adj_count(self, r, c, grid):
        cnt = 0
        for r_offset, c_offset in OFFSETS:
            adj_r = r + r_offset
            adj_c = c + c_offset
            if adj_r >= 0 and adj_c >= 0 and adj_r < len(grid) and adj_c < len(grid[0]):
                if grid[adj_r][adj_c] == "@":
                    cnt += 1
        return cnt

    def part1(self):
        data = self.get_data_lines()
        result = 0
        for r in range(len(data)):
            for c in range(len(data[0].strip())):
                try:
                    if data[r][c] == "@" and self.get_adj_count(r, c, data) < 4:
                        result += 1
                except Exception:
                    print(r, c)

        return result

    def part2(self):
        result = 0
        grid = [list(row.strip()) for row in self.get_data_lines()]

        while True:
            removable = []
            for r in range(len(grid)):
                for c in range(len(grid[r])):
                    if grid[r][c] == "@" and self.get_adj_count(r, c, grid) < 4:
                        removable.append((r, c))

            if not removable:
                break

            for r, c in removable:
                grid[r][c] = "."

            removed = len(removable)
            result += removed

        return result


if __name__ == "__main__":
    path = "input/day04.txt"
    Solution(path).solve(2)
