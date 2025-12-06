def parse(raw_input: str):
    return [p.split("-") for p in raw_input.split(",")]


def invalid_p1(n: int):
    sn = str(n)
    ln = len(sn)
    if ln % 2 == 1:
        return False
    hln = ln // 2
    return sn[:hln] == sn[hln:]


def invalid_p2(n: int):
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
        if all(c == first_char for c in sn[0::2]) and all(c == sn[1] for c in sn[1::2]):
            return True

        # All other even-length sequences invalid
        return False

    # handle 9 digit numbers
    if sn[0:3] == sn[3:6] and sn[0:3] == sn[6:9]:
        return True

    # No remaining valid cases
    return False


def solve(raw_input: str, test_invalid: callable):
    data = parse(raw_input)
    invalid_sum = 0
    for a, b in data:
        for n in range(int(a), int(b) + 1):
            if test_invalid(n):
                # print(n)
                invalid_sum += n
    return invalid_sum


def get_brute_size(raw_input: str):
    data = parse(raw_input)
    tot = 0
    for a, b in data:
        tot += b - a
    return tot


if __name__ == "__main__":
    with open("input/day02.txt") as f:
        r = solve(f.read(), invalid_p2)
        print("solution:", r)
