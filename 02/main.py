import sys

if len(sys.argv) != 2:
    print("Usage: python main.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]

with open(input_file) as f:
    lines = f.readlines()
