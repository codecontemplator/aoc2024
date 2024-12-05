filename = "day5/input.txt"

rules = []
orderings = []
with open(filename, 'r') as file:
    x = False
    for line in file.read().splitlines():
        if len(line) == 0:
            x = True
            continue

        if x:
            o = list(map(int, line.split(',')))
            orderings += [o]
        else:
            a,b = line.split('|')
            rules.append((int(a),int(b)))

print("rules")
print(rules)

print("orderings")
print(orderings)

validOrderings = []
for ordering in orderings:
    isValid = True
    for (a,b) in rules:
        if a in ordering and b in ordering:
            ai = ordering.index(a)
            bi = ordering.index(b)
            if ai > bi:
                isValid = False
                break
    if isValid:
        validOrderings += [ordering]

print("valid orderings")
print(validOrderings)

result = 0
for validOrdering in validOrderings:
    middle = validOrdering[len(validOrdering) // 2]
    result += middle

print("result")
print(result)
