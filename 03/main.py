import sys
import re

if len(sys.argv) != 2:
    print("Usage: python main.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()

pattern = re.compile(r"mul\(\d+,\d+\)")
pattern_2 = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")

total = 0
for line in lines:
    matches = pattern.findall(line)
    for match in matches:
        numbers = re.findall(r"\d+", match)
        num1, num2 = map(int, numbers)
        total += num1 * num2

print(f"P1 Total: {total}")

total_2 = 0
enabled = True

for line in lines:
    print(line)
    matches = pattern_2.findall(line)
    print(matches)
    for match in matches:
        if match == "do()":
            enabled = True
        elif match == "don't()":
            enabled = False
        else:
            numbers = re.findall(r"\d+", match)
            num1, num2 = map(int, numbers)
            if enabled:
                total_2 += num1 * num2

print(f"Total: {total_2}")
