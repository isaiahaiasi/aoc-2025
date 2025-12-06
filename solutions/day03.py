def solve_part1(raw_input: list[str]):
    result = 0
    for r in [r.strip() for r in raw_input]:
        v1 = max(r[:-1])
        i = r.index(v1)
        v2 = max(r[i + 1 :])
        print(r, v1, i, v2, v1 + v2)
        result += int(v1 + v2)

    return result


def solve_part2(raw_input: list[str]):
    result = 0

    for r in [r.strip() for r in raw_input]:
        num = ""
        cur = 0
        for i in range(0, 12):
            dig = max(r[cur : len(r) + i - 11])
            cur += r[cur:].index(dig) + 1
            num += dig
        result += int(num)
    return result


if __name__ == "__main__":
    path = "input/day03.txt"
    with open(path) as f:
        r = solve_part2(f.readlines())
        print("solution:", r)
