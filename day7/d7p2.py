def calc(l):
    if len(l) == 1:
        return [l[0]]
    else:
        a = l[0]
        b = l[1]
        l2 = l[2:]
        x = [a * b] + l2
        y = [a + b] + l2
        z = [int(str(a)+str(b))] + l2
        r1 = calc(x)
        r2 = calc(y)
        r3 = calc(z)
        return r1 + r2 + r3

def isValid(re, l):
    r = calc(l)
    return re in r


filename = 'day7/input.txt'
with open(filename, 'r') as file:
    lines = file.read().splitlines()
    data = []
    for line in lines:
       r, rest = line.split(':')
       data += [(int(r), list(map(int, rest.split())))]


result = 0
for (r,l) in data:
    if isValid(r,l):
        result += r

print(result)
