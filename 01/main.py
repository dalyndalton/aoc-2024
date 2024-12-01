with open("input.txt") as f:
    lines = f.readlines()

s1 = list()
s2 = list()
d2 = dict()

for line in lines:
    x, y = map(int, line.split())

    s1.append(int(x))
    s2.append(int(y))
    if y in d2:
        d2[y] += 1
    else:
        d2[y] = 1

distances = [abs(int(x) - int(y)) for x, y in zip(sorted(s1), sorted(s2))]
print("P1: ", sum(distances))

sim_score = 0

for n in s1:
    if n not in d2:
        continue
    sim_score += n * d2[n]

print("P2: ", sim_score)
