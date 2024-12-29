import re
from collections import defaultdict
from itertools import combinations, chain

numBits = 45

def evalOp(arg1, op, arg2):
    match op:
        case "AND":
            return arg1 and arg2
        case "OR":
            return arg1 or arg2
        case "XOR":
            return arg1 ^ arg2

def evalAt(var, knowns, ops):
    if var in knowns:
        return knowns[var]
    
    (arg1, op, arg2) = ops[var]
    arg1Value = evalAt(arg1, knowns, ops)
    arg2Value = evalAt(arg2, knowns, ops)
    result = evalOp(arg1Value, op, arg2Value)
    knowns[var] = result
    return result


def has_cycle(edges):    
    def build_graph(edges, directed=False):
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            if not directed:
                graph[v].append(u)
        return dict(graph)
    graph = build_graph(edges, True)

    def dfs(node):
        if node in recursion_stack:
            return True
        if node in visited:
            return False

        visited.add(node)
        recursion_stack.add(node)

        if node in graph:
            for neighbor in graph[node]:
                if dfs(neighbor):
                    return True

        recursion_stack.remove(node)
        return False

    visited = set()
    recursion_stack = set()

    for node in graph:
        if dfs(node):
            return True

    return False
    
def searchFromSource(input, inputToOutputMap):
    if input not in inputToOutputMap:
        return []
    
    output = inputToOutputMap[input]    
    return [output] + searchFromSource(output, inputToOutputMap)

def searchFromTarget(output, outputToInputsMap):
    if output not in outputToInputsMap:
        return []
    
    input1, input2 = outputToInputsMap[output]
    result1 = searchFromTarget(input1, outputToInputsMap)
    result2 = searchFromTarget(input2, outputToInputsMap)
    return [output] + result1 + result2

def varName(namePrefix, bitNum):
    return f"{namePrefix}{bitNum:02}"

def candidateSwaps(bitNum, opsList):
    inputToOutputMap = { input: output for (output, (input1, _, input2)) in opsList for input in (input1, input2)}
    outputToInputsMap = { output: (input1, input2) for (output, (input1, _, input2)) in opsList }

    sourceOpsX = searchFromSource(varName('x', bitNum), inputToOutputMap)
    sourceOpsY = searchFromSource(varName('y', bitNum), inputToOutputMap)
    sourceOps = set(sourceOpsX + sourceOpsY)
    destOpsZ = searchFromTarget(varName('z', bitNum), outputToInputsMap)
    destOpsCurry = searchFromTarget(varName('z', bitNum+1), outputToInputsMap)
    destOps = set(destOpsZ + destOpsCurry)

    g1 = ((s,d) for s in sourceOps for d in destOps if s != d)
    # g2 = ((s1,s2) for s1 in sourceOps for s2 in sourceOps if s1 != s2)
    g3 = ((d1,d2) for d1 in destOps for d2 in destOps if d1 != d2)
    return chain(g1, g3)

def mkBinary(namePrefix, setBits):    
    result = [ (varName(namePrefix, i), 0) for i in range(numBits)]
    for setBit in setBits:
        result[setBit] = (result[setBit][0], 1)
    return result

def isCyclic(ops):
    if has_cycle([ (inp, out) for (out, (in1, _, in2)) in ops.items() for inp in (in1, in2)] ):
        return False

def testBit(bitNum, ops):
    if has_cycle([ (inp, out) for (out, (in1, _, in2)) in ops.items() for inp in (in1, in2)] ):
        return False
    
    def testHelper(xs, ys):
        x = mkBinary("x", xs)
        y = mkBinary("y", ys)
        knowns = dict(x + y)
        z = evalAt(varName('z', bitNum), knowns, ops)
        curry = evalAt(varName('z', bitNum+1), knowns, ops)
        return z, curry
    
    if testHelper([], []) != (0,0):
        return False
    if testHelper([bitNum], []) != (1,0):
        return False
    if testHelper([], [bitNum]) != (1,0):
        return False
    if testHelper([bitNum], [bitNum]) != (0,1):
        return False

    # do we need to test prev curry?

    return True

def load():
    filename = "day24/input.txt"

    with open(filename,'r') as file:
        lines = file.read().splitlines()

    split = lines.index("")
    #inputsRaw = lines[:split]
    opsRaw = lines[split+1:]

    #inputs = [ (name, int(value) == 1) for name, value in (input.split(':') for input in inputsRaw)]
    ops = {
        (out, (arg1, op, arg2))
        for match in (re.match(r"^(.+?) (.+?) (.+?) -> (.+)$", op) for op in opsRaw)
        if match is not None
        for arg1, op, arg2, out in [match.groups()]
    }

    return ops

def swap(a, b, dict):
    tmp = dict[a]
    dict[a] = dict[b]
    dict[b] = tmp        

def fix(inputBit, opsMap):
    print(inputBit)
    if isCyclic(opsMap):
        return None
    
    if inputBit == numBits:
        return []
    
    if testBit(inputBit, opsMap):
        return fix(inputBit + 1, opsMap)
    
    print("problem detected")
    candidates = candidateSwaps(inputBit, list(opsMap.items()))
    for candidate in candidates:
        a, b = candidate
        swap(a, b, opsMap)
        if not testBit(inputBit, opsMap):
            swap(a, b, opsMap)  
            continue

        print(f"swap {a,b}")

        swaps = fix(inputBit+1, opsMap)
        if swaps != None: # and len(swaps) <= 8:
            print("found ", swaps, len(swaps))
            if len(swaps) <= 8:
                return [a,b] + swaps
        swap(a, b, opsMap)  
    
    return None

opsList = load()
opsMap = dict(opsList)
swaps = fix(0, opsMap)

print(','.join(sorted(list(set(swaps)))))

# bbb,cdq,cmf,drg,fkw,hpp,nhb,nvq,psw,tbt,vtg,z26,z32,z32,z36,z37
# dfp,kth,kth,nng,nwm,psw,qmv,rpb,skt,wkk,z26,z26,z32,z33,z33,z36
# dfp,ftq,kth,mbg,tbt,vpm,z12,z26,z32,z36
# cmf,nvq,psw,tbt,vtg,wbb,wbb,wkk,z12,z13,z13,z26,z32,z36
# mdq,nhb,psw,psw,qnf,swt,tbt,vpm,z26,z27,z27,z32


# bbb,cmf,hpp,mdq,nhb,psw,rpb,skt,z26,z32,z33,z36,z37
# gsd,hpp,mdq,nhb,nwm,psw,skt,z26,z32,z36,z37

# cdq,cmf,mdq,nhb,psw,tbt,wkk,z26,z32,z36
# cdq,gsd,nhb,psw,tbt,vpm,z26,z32,z36