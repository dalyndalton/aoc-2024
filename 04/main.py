import sys
from itertools import product

if len(sys.argv) != 2:
    print("Usage: python main.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

PERMUTATIONS = list(product([1, 0, -1], repeat=2))
DIAG_PERMUTATIONS = list(product([1, -1], repeat=2))
TARGET = "XMAS"


def in_bounds(board_position: tuple[int, int]) -> bool:
    row, col = board_position
    return 0 <= row < len(lines) and 0 <= col < len(lines[row])


def search_XMAS(
    board_position: tuple[int, int],
) -> int:
    search_target = TARGET[1]
    row, col = board_position

    found = 0

    for direction, perm in enumerate(PERMUTATIONS):
        new_row = row + perm[0]
        new_col = col + perm[1]

        if not in_bounds((new_row, new_col)):
            continue

        if lines[new_row][new_col] == search_target and validate_XMAS(
            (new_row, new_col), 2, direction
        ):
            found += 1
    return found


def validate_XMAS(
    board_position: tuple[int, int], target_position: int, direction: int
):
    if target_position >= len(TARGET):
        return True

    row, col = board_position
    search_target = TARGET[target_position]
    new_row = row + PERMUTATIONS[direction][0]
    new_col = col + PERMUTATIONS[direction][1]

    if not in_bounds((new_row, new_col)):
        return False

    if lines[new_row][new_col] == search_target:
        return validate_XMAS((new_row, new_col), target_position + 1, direction)
    else:
        return False


def search_p2(
    board_position: tuple[int, int],
) -> int:
    row, col = board_position
    search_candidates = []

    for perm in DIAG_PERMUTATIONS:
        new_row = row + perm[0]
        new_col = col + perm[1]

        if not in_bounds((new_row, new_col)):
            return False

        search_candidates.append(lines[new_row][new_col])

    # check for x pattern
    if set(search_candidates[0] + search_candidates[3]) == {"M", "S"} and set(
        search_candidates[1] + search_candidates[2]
    ) == {"M", "S"}:
        return True
    return False


p1_total = 0
for row in range(len(lines)):
    for col in range(len(lines[row])):
        if lines[row][col] == TARGET[0]:
            p1_total += search_XMAS((row, col))


p2_total = 0
for row in range(len(lines)):
    for col in range(len(lines[row])):
        if lines[row][col] == "A" and search_p2((row, col)):
            p2_total += 1
print(f"P1 Total: {p1_total}")
print(f"P2 Total: {p2_total}")
