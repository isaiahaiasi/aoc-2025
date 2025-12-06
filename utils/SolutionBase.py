from pathlib import Path


class SolutionBase:
    def __init__(self, path: str):
        self.path = Path(path)
        pass

    def get_data_raw(self):
        return self.path.read_text()

    def get_data_lines(self):
        with self.path.open() as f:
            return f.readlines()

    def solve(self, part: int, benchmark=False):
        assert part > 0 and part < 3, "`part` can only be 1 or 2!"

        fn = self.part1 if part == 1 else self.part2

        if benchmark:
            import timeit

            t = timeit.Timer(fn)
            print(t.timeit(1000))
        else:
            print(fn())

    def part1(self) -> int:
        raise NotImplementedError

    def part2(self) -> int:
        raise NotImplementedError

    # TODO:
    # - testing
