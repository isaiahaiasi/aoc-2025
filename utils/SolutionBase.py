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

    def solve(self, part: int, benchmark=0):
        """
        :param part: Part 1 or 2 of the day's puzzle
        :param benchmark: Number of iterations to run benchmark (default 0: no benchmarking)
        """
        assert part > 0 and part < 3, "`part` can only be 1 or 2!"

        fn = self.part1 if part == 1 else self.part2

        print(f"solution, p{part}: {fn()}")

        if benchmark > 0:
            import timeit

            t = timeit.Timer(fn)
            print(f"avg time: {t.timeit(benchmark) / benchmark:.5f}s")

    def part1(self) -> int:
        raise NotImplementedError

    def part2(self) -> int:
        raise NotImplementedError

    # TODO:
    # - testing?
