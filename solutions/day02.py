from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def parse(self):
        return [p.split("-") for p in self.get_data_raw().split(",")]

    def get_brute_size(self):
        data = self.parse()
        tot = 0
        for a, b in data:
            tot += b - a
        return tot

    def solve_common(self, invalid_test: callable):
        data = self.parse()
        invalid_sum = 0
        for a, b in data:
            for n in range(int(a), int(b) + 1):
                if invalid_test(n):
                    invalid_sum += n
        return invalid_sum

    def invalid_p1(self, n: int):
        sn = str(n)
        ln = len(sn)
        if ln % 2 == 1:
            return False
        hln = ln // 2
        return sn[:hln] == sn[hln:]

    def invalid_p2(self, n: int):
        # Impossible to repeat if 10 or lower
        if n < 11:
            return False

        sn = str(n)
        ln = len(sn)

        # Test for case: 1xN
        first_char = sn[0]
        if all(c == first_char for c in sn):
            return True

        if ln < 4:
            return False

        """
        Remaining possible patterns if they aren't the same:
        2  - x
        3  - x
        4  - 2x2
        5  - x
        6  - 2x3, 3x2
        7  - x
        8  - 2x4, 4x2
        9  - 3x3
        10 - 2x5, 5x2
        (We don't have to worry abt 11-digit numbers or higher)
        """

        # For even-length numbers, we only have to worry about
        # sequences of length 2 or ln/2
        if ln % 2 == 0:
            # handle (ln/2) sequences (eg: 158158)
            hln = ln // 2
            if sn[:hln] == sn[hln:]:
                return True

            # handle 2 char sequences (eg: 6767)
            if all(c == first_char for c in sn[0::2]) and all(
                c == sn[1] for c in sn[1::2]
            ):
                return True

            # All other even-length sequences invalid
            return False

        # handle 9 digit numbers
        if sn[0:3] == sn[3:6] and sn[0:3] == sn[6:9]:
            return True

        # No remaining valid cases
        return False

    def part1(self) -> int:
        return self.solve_common(self.invalid_p1)

    def part2(self) -> int:
        return self.solve_common(self.invalid_p2)


if __name__ == "__main__":
    s = Solution("input/day02.txt")
    s.solve(2, benchmark=50)
