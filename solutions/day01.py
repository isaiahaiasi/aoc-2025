class Solution:
    def __init__(self, path: str):
        with open(path) as f:
            self.raw_data = f.read()

    def solve1(self):
        instructions = self.raw_data.splitlines()
        cur_pos = 50
        zero_count = 0
        for instr in instructions:
            direction = -1 if instr[0] == "L" else 1
            size = int(instr[1:])
            cur_pos += direction * size
            cur_pos %= 100
            if cur_pos == 0:
                zero_count += 1
        return zero_count

    def solve2(self):
        instructions = self.raw_data.splitlines()
        cur_pos = 50
        clicks = 0
        for instr in instructions:
            direction = -1 if instr[0] == "L" else 1
            distance = int(instr[1:])
            # This isn't QUITE right in itself
            zeros, pos = divmod(cur_pos + (distance * direction), 100)
            # ...So here's some arbitrary off-by-one fixes:
            zeros = abs(zeros)
            if pos == 0 and direction == -1:
                zeros += 1
            if cur_pos == 0 and direction == -1:
                zeros -= 1
            cur_pos = pos

            clicks += abs(zeros)

        return clicks


if __name__ == "__main__":
    s = Solution("input/day01.txt")
    print(s.solve1(), s.solve2())
