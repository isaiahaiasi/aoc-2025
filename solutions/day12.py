from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def parse(self):
        sections = self.get_data_raw().split("\n\n")
        shapes = []
        for sec in sections[:-1]:
            # bool list, then get the (x, y) coords for each occupied square.
            s = [c == "#" for c in sec[3:].replace("\n", "")]
            base_shape = tuple(divmod(i, 3) for i in range(9) if s[i])
            shapes.append(self.get_variants(base_shape))

        problems = []
        for sec in sections[-1].splitlines():
            dimensions = tuple(map(int, sec[: sec.index(" ") - 1].split("x")))
            shape_indices = tuple(int(n) for n in sec[sec.index(" ") + 1 :].split())
            problems.append((dimensions, shape_indices))

        return shapes, problems

    def debug_shape(self, s):
        print(s)
        for i in range(3):
            print("".join(["#" if (i, j) in s else "." for j in range(3)]))

    def rotate(self, s):
        return tuple(sorted((2 - y, x) for x, y in s))

    def flip(self, s):
        return tuple(sorted((2 - x, y) for x, y in s))

    def get_variants(self, base_shape):
        """
        Each shape can be rotated or flipped, but depending on the shape
        there could be fewer *unique* variants.
        """
        shapes = set()
        shapes.add(base_shape)
        shapes.add(self.flip(base_shape))

        cur_shape = base_shape
        for _ in range(8):
            cur_shape = self.rotate(cur_shape)
            shapes.add(cur_shape)
            shapes.add(self.flip(cur_shape))
        return list(shapes)

    def part1(self):
        """
        Start with naive backtracking algo?
        """
        shapes, problems = self.parse()
        shape_cnt = len(shapes)

        valid_count = 0
        invalid_count = 0

        for (width, height), presents in problems:
            # Check if the boxes definitely fit.
            if sum(presents) * 9 <= width * height:
                valid_count += 1
                continue
            # Check if the boxes definitely do NOT fit.
            tot_occupied = sum(
                [len(shapes[i][0]) * presents[i] for i in range(shape_cnt)]
            )
            if tot_occupied > width * height:
                invalid_count += 1

        # Wait. Huh? Lol.
        return f"{valid_count} - {invalid_count}"

    def part2(self) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    Solution("input/day12.txt").solve(1)
    # Solution("sample-input/day12.txt").solve(1)
