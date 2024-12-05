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

invalidOrderings = []
for ordering in orderings:
    isValid = True
    for (a,b) in rules:
        if a in ordering and b in ordering:
            ai = ordering.index(a)
            bi = ordering.index(b)
            if ai > bi:
                isValid = False
                break
    if not isValid:
        invalidOrderings += [ordering]

print("invalid orderings")
print(invalidOrderings)

for invalidOrdering in invalidOrderings:
    print(invalidOrdering)
    invalid = True
    while invalid:
        invalid = False
        for (a,b) in rules:
            if a in invalidOrdering and b in invalidOrdering:
                ai = invalidOrdering.index(a)
                bi = invalidOrdering.index(b)
                if ai > bi:
                    invalidOrdering[ai] = b
                    invalidOrdering[bi] = a
                    invalid = True                    

print("fixed orderings")    
print(invalidOrderings)


result = 0
for invalidOrdering in invalidOrderings:
    middle = invalidOrdering[len(invalidOrdering) // 2]
    result += middle

print("result")
print(result)
