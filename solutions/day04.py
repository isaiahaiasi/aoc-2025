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


def get_adj_count(r, c, grid):
    cnt = 0
    for r_offset, c_offset in OFFSETS:
        adj_r = r + r_offset
        adj_c = c + c_offset
        if adj_r >= 0 and adj_c >= 0 and adj_r < len(grid) and adj_c < len(grid[0]):
            if grid[adj_r][adj_c] == "@":
                cnt += 1
    return cnt


def solve_part1(raw_input: list[str]):
    result = 0
    for r in range(len(raw_input)):
        for c in range(len(raw_input[0].strip())):
            try:
                if raw_input[r][c] == "@" and get_adj_count(r, c, raw_input) < 4:
                    result += 1
            except Exception:
                print(r, c)

    return result


def solve_part2(raw_input: list[str]):
    result = 0
    grid = [list(row.strip()) for row in raw_input]

    while True:
        removable = []
        for r in range(len(grid)):
            for c in range(len(grid[r])):
                if grid[r][c] == "@" and get_adj_count(r, c, grid) < 4:
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
    with open(path) as f:
        r = solve_part2(f.readlines())
        print("solution:", r)
