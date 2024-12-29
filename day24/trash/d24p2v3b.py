import re
from collections import defaultdict
from itertools import combinations

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

    return ((s,d) for s in sourceOps for d in destOps if s != d)

def mkBinary(namePrefix, setBits):    
    result = [ (varName(namePrefix, i), 0) for i in range(numBits)]
    for setBit in setBits:
        result[setBit] = (result[setBit][0], 1)
    return result

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

def generate_distinct_pair_groups(lst, group_size):
    #indices = range(len(lst))  # Indices of the list
    #all_pairs = list(combinations(lst, 2))  # Generate all pairs

    # Recursive function to construct groups
    def build_groups(current_group, remaining_pairs):
        if len(current_group) == group_size:  # Base case: Group is complete
            yield current_group
            return

        for i, pair in enumerate(remaining_pairs):
            # Check if the pair is compatible (no shared indices)
            if not set(pair) & set(p for p in current_group):
                # Recurse with the new pair added
                yield from build_groups(current_group + [pair], remaining_pairs[i + 1:])

    # Start building groups
    return build_groups([], lst)

def swap(a, b, dict):
    tmp = dict[a]
    dict[a] = dict[b]
    dict[b] = tmp        

opsList = load()

opsMap = dict(opsList)

numBits = 45
swaps = []
for inputBit in range(numBits):    
    print(inputBit)
    if not testBit(inputBit, opsMap):
        print(f"problem detected")
        fixed = False
        groupSize = 0
        while not fixed:            
            groupSize += 1
            print(f"   group size {groupSize}")
            candidatesRaw = list(candidateSwaps(inputBit, list(opsMap.items())))
            candidates = generate_distinct_pair_groups(candidatesRaw, groupSize)
            while (candidateList := next(candidates, None)) != None:
                for candidate in candidateList:
                    a, b = candidate
                    swap(a, b, opsMap)
                ok = testBit(inputBit, opsMap)
                if ok:
                    print(f"swapping {a,b}")
                    fixed = True
                    break
                for candidate in candidateList:
                    a, b = candidate
                    swap(a, b, opsMap)
                swap(a, b, opsMap)        
        
        if fixed:
            print("fixed!")
        else:
            print("not fixed!!!")
