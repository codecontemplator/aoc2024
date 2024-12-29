import re

numBits = 45

def varName(namePrefix, bitNum):
    return f"{namePrefix}{bitNum:02}"

def mkBinary(namePrefix):    
    return [ (varName(namePrefix, i), 0) for i in range(numBits)]

def isBitSet(number, bit_position):
    bitmask = 1 << bit_position
    return (number & bitmask) != 0

def setBit(binary, bitPos):
    name, _ = binary[bitPos]
    binary[bitPos] = (name, 1)

def evalOp(arg1, op, arg2):
    match op:
        case "AND":
            return arg1 and arg2
        case "OR":
            return arg1 or arg2
        case "XOR":
            return arg1 ^ arg2
        
def evalAt(var, knowns, gates):
    if var in knowns:
        return knowns[var]
    
    (arg1, op, arg2) = gates[var]
    arg1Value = evalAt(arg1, knowns, gates)
    arg2Value = evalAt(arg2, knowns, gates)
    result = evalOp(arg1Value, op, arg2Value)
    return result

def testOneBitAdder(bitPos, gates):
    for a in range(2):
        for b in range(2):            
            for cin in range(2) if bitPos > 0 else range(1):                
                x = mkBinary('x')
                y = mkBinary('y')
                if a == 1:
                    setBit(x, bitPos)
                if b == 1:
                    setBit(y, bitPos)
                if cin == 1:
                    setBit(x, bitPos-1)
                    setBit(y, bitPos-1)
                knowns = dict(x + y)
                z0 = evalAt(varName('z', bitPos), knowns, gates)
                z1 = evalAt(varName('z', bitPos+1), knowns, gates)
                s = a + b + cin
                z0Expected = 1 if isBitSet(s, 0) else 0
                z1Expected = 1 if isBitSet(s, 1) else 0
                if z0 != z0Expected or z1 != z1Expected:
                    return False
    return True
                
def load(filename):
    with open(filename,'r') as file:
        lines = file.read().splitlines()
    split = lines.index("")
    opsRaw = lines[split+1:]
    return [
        (out, (arg1, op, arg2))
        for match in (re.match(r"^(.+?) (.+?) (.+?) -> (.+)$", op) for op in opsRaw)
        if match is not None
        for arg1, op, arg2, out in [match.groups()]
    ]
def swap(a, b, dict):
    tmp = dict[a]
    dict[a] = dict[b]
    dict[b] = tmp  

gatesList = load("day24/input.txt")
gatesDict = dict(gatesList)

swap("kth", "z12", gatesDict)
swap("gsd", "z26", gatesDict)
swap("tbt", "z32", gatesDict)
swap("qnf", "vpm", gatesDict)

fails = 0
for bitPos in range(numBits):
    ok = testOneBitAdder(bitPos, gatesDict)
    print(f"{bitPos}: {ok}")
    if not ok:
        fails += 1

print(fails)

#print(",".join(sorted(["kth", "z12","gsd", "z26","tbt", "z32","qnf", "vpm"])))