import sys

if len(sys.argv) != 2:
    print("Usage: python main.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()


safe_lines = 0
recovere_lines = 0
unsafe_lines = 0


def directions(x: list[int]) -> int:
    differences = sum(1 if x[i] - x[i - 1] >= 0 else -1 for i in range(1, len(x)))
    if differences < 0:
        return -1
    return 1


# Part 1
def valid_sequence(x: list[int]) -> bool:
    direction = directions(x)

    for idx in range(1, len(x)):
        diff = x[idx] * direction - x[idx - 1] * direction
        if not (1 <= diff <= 3):
            return False

    return True


# Part 2
def brute_recovery(x: list[int]) -> bool:
    if not valid_sequence(x):
        return any(valid_sequence(x[:idx] + x[idx + 1 :]) for idx in range(len(x)))


for line in lines:
    x = list(map(int, line.split()))
    if valid_sequence(x):
        safe_lines += 1
    elif brute_recovery(x):
        recovere_lines += 1
    else:
        unsafe_lines += 1
        print(f"Unsafe: {x}")


print(f"P1: {safe_lines=} {unsafe_lines=}")
print(f"P2: Total: {safe_lines + recovere_lines}, {recovere_lines=}")
