import re

def evalOp(arg1, op, arg2):
    match op:
        case "AND":
            return arg1 and arg2
        case "OR":
            return arg1 or arg2
        case "XOR":
            return arg1 ^ arg2
        
def getVars(ops):
    variables = []
    for (arg1, _, arg2, out) in ops:
        variables.append(arg1)
        variables.append(arg2)
        variables.append(out)
    return set(variables)
        
def eval(inputs, ops):
    knowns = dict(inputs)
    variables = list(getVars(ops) - knowns.keys())
    while len(variables) > 0:
        found = False
        for i, var in enumerate(variables):
            for arg1, op, arg2, out in ops:
                if var == out and arg1 in knowns.keys() and arg2 in knowns.keys():
                    result = evalOp(knowns[arg1], op, knowns[arg2])
                    knowns[out] = result
                    del variables[i]
                    found = True
                    break
            if found:
                break
        if not found:
            return None
    return knowns

def load():
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

    return inputs, ops

def formatBinary(knowns, prefix = 'z'):
    return ''.join(
        [
            '1' if knowns[var] else '0'
            for var in sorted([ var for var in knowns.keys() if var.startswith(prefix)], reverse=True)
        ])
    

_, ops = load()

numBits = 45
for inputBit in range(numBits):    
    x0 = [ (f"x{i:02}", 0) for i in range(numBits)]
    y0 = [ (f"y{i:02}", 0) for i in range(numBits)]
    x1 = [ (f"x{i:02}", 0) for i in range(numBits)]
    x1[inputBit] = (x1[inputBit][0], 1)
    y1 = [ (f"y{i:02}", 0) for i in range(numBits)]
    y1[inputBit] = (y1[inputBit][0], 1)

    z0 = eval(x0 + y0, ops)
    z1 = eval(x1 + y0, ops)
    z2 = eval(x0 + y1, ops)
    z3 = eval(x1 + y1, ops)

    print(f"========{inputBit}============")
    print(formatBinary(z0))
    print(formatBinary(z1))
    print(formatBinary(z2))
    print(formatBinary(z3))
    print("======================")
