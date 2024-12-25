import re

filename = "day24/input.txt"

with open(filename,'r') as file:
    lines = file.read().splitlines()

split = lines.index("")
inputsRaw = lines[:split]
opsRaw = lines[split+1:]

inputs = [ (name, int(value) == 1) for name, value in (input.split(':') for input in inputsRaw)]
ops = [ 
    (arg1, op, arg2, out)
    for match in (re.match(r"^(.+?) (.+?) (.+?) -> (.+)$", op) for op in opsRaw)
    if match is not None
    for arg1, op, arg2, out in [match.groups()]
]

knowns = dict(inputs)

variables = []
for (arg1, _, arg2, out) in ops:
    variables.append(arg1)
    variables.append(arg2)
    variables.append(out)
variables = list(set(variables) - knowns.keys())


def eval(arg1, op, arg2):
    match op:
        case "AND":
            return arg1 and arg2
        case "OR":
            return arg1 or arg2
        case "XOR":
            return arg1 ^ arg2

while len(variables) > 0:
    found = False
    for i, var in enumerate(variables):
        for arg1, op, arg2, out in ops:
            if var == out and arg1 in knowns.keys() and arg2 in knowns.keys():
                result = eval(knowns[arg1], op, knowns[arg2])
                knowns[out] = result
                del variables[i]
                found = True
                break
        if found:
            break
    if not found:
        break;

result = int(''.join(
    [
        '1' if knowns[var] else '0'
        for var in sorted([ var for var in knowns.keys() if var.startswith("z")], reverse=True)
    ]
), 2)

print(result)





