def get_parsed_input(path: str) -> tuple[list[tuple[int, int]], list[int]]:
    with open(path) as f:
        raw = f.read().strip().splitlines()
    split_idx = raw.index("")
    ranges = [(int(a), int(b)) for a, b in (r.split("-") for r in raw[:split_idx])]
    values = [int(n) for n in raw[split_idx + 1 :]]
    return ranges, values


def solve_part1(path: str):
    result = 0
    ranges, values = get_parsed_input(path)
    for v in values:
        for a, b in ranges:
            if v >= a and v <= b:
                result += 1
                break  # don't double-count
    return result


def solve_part2(path: str):
    ranges, _ = get_parsed_input(path)
    ranges.sort()

    merged = [ranges[0]]

    for i in range(1, len(ranges)):
        a, b = merged[-1]
        c, d = ranges[i]
        if a <= c and c <= b and b <= d:
            merged[-1] = (a, d)
        elif b < c:
            merged.append(ranges[i])

    return sum([b - a + 1 for a, b in merged])


if __name__ == "__main__":
    path = "input/day05.txt"
    print(solve_part2(path))
