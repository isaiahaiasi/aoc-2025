import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2 or not sys.argv[1].isdigit():
        print("Provide the day! Example usage: python3 newday.py 3")

    day = "day" + sys.argv[1].zfill(2)

    root = Path(__file__).parent

    paths = [
        root / "input" / (day + ".txt"),
        root / "sample-input" / (day + ".txt"),
    ]

    for p in paths:
        p.parent.mkdir(exist_ok=True)
        if not p.exists():
            p.write_text("", encoding="utf-8")
        else:
            print(f"skipping {p.name} - already exists!")

    py_path = root / "solutions" / (day + ".py")
    if not py_path.exists():
        py_path.write_text(
            f"""from utils.SolutionBase import SolutionBase


class Solution(SolutionBase):
    def part1(self) -> int:
        raise NotImplementedError

    def part2(self) -> int:
        raise NotImplementedError


if __name__ == "__main__":
    Solution("sample-input/{day}.txt").solve(1)
"""
        )
    else:
        print(f"skipping {p.name} - already exists!")


if __name__ == "__main__":
    main()
