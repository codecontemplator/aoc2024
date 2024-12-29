import re
from itertools import combinations

# def swapOut(g1, g2):
#     (arg1_1, op_1, arg2_1, out_1) = g1
#     (arg1_2, op_2, arg2_2, out_2) = g2
#     return (arg1_1, op_1, arg2_1, out_2), (arg1_2, op_2, arg2_2, out_1)

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

def binaryToDecimal(knowns, prefix = 'z'):
    binary = ''.join(
        [
            '1' if knowns[var] else '0'
            for var in sorted([ var for var in knowns.keys() if var.startswith(prefix)], reverse=True)
        ])
    return int(binary, 2)

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

def backtracking_distinct_groups(lst, group_size):
    indices = range(len(lst))
    all_pairs = list(combinations(indices, 2))
    results = []

    def backtrack(group, start):
        if len(group) == group_size:
            results.append(group[:])
            return

        for i in range(start, len(all_pairs)):
            pair = all_pairs[i]
            # Ensure pair does not overlap with current group
            if not any(set(pair) & set(p) for p in group):
                group.append(pair)
                backtrack(group, i + 1)
                group.pop()

    backtrack([], 0)
    return results

def backtracking_distinct_groups2(lst, group_size):
    indices = range(len(lst))
    all_pairs = list(combinations(indices, 2))
    #results = []

    def backtrack(group, start):
        if len(group) == group_size:
            yield group[:]
            return

        for i in range(start, len(all_pairs)):
            pair = all_pairs[i]
            # Ensure pair does not overlap with current group
            if not any(set(pair) & set(p) for p in group):
                group.append(pair)
                yield from backtrack(group, i + 1)
                group.pop()

    return backtrack([], 0)

def generate_distinct_index_pair_groups(lst, group_size):
    indices = range(len(lst))  # Indices of the list
    all_pairs = list(combinations(indices, 2))  # Generate all pairs

    # Recursive function to construct groups
    def build_groups(current_group, remaining_pairs):
        if len(current_group) == group_size:  # Base case: Group is complete
            yield current_group
            return

        for i, pair in enumerate(remaining_pairs):
            # Check if the pair is compatible (no shared indices)
            if not set(pair) & set(index for p in current_group for index in p):
                # Recurse with the new pair added
                yield from build_groups(current_group + [pair], remaining_pairs[i + 1:])

    # Start building groups
    return build_groups([], all_pairs)

def generate_distinct_index_pair_groups2(lst, group_size, deps):
    indices = range(len(lst))  # Indices of the list
    all_pairs_1 = list(combinations(indices, 2))  # Generate all pairs
    all_pairs = [ (i,j) for (i,j) in all_pairs_1 if not lst[j][3] in deps[lst[i][3]] and not lst[i][3] in deps[lst[j][3]] ]

    # Recursive function to construct groups
    def build_groups(current_group, remaining_pairs):
        if len(current_group) == group_size:  # Base case: Group is complete
            yield current_group
            return

        for i, pair in enumerate(remaining_pairs):
            # Check if the pair is compatible (no shared indices)            
            if not set(pair) & set(index for p in current_group for index in p):
                # Recurse with the new pair added
                yield from build_groups(current_group + [pair], remaining_pairs[i + 1:])

    # Start building groups
    return build_groups([], all_pairs)

def solve(input, ops, numBroken, isSolution, deps):
    #print(numBroken)
    #pairs = list(combinations(range(len(ops)), 2))
    #candidateSelections = combinations(pairs, numBroken)
    candidateSelections = generate_distinct_index_pair_groups2(ops, numBroken, deps)

    for index, canditateSelection in enumerate(candidateSelections):
        selection = canditateSelection
        ops2 = ops.copy()
        # print(f"------ {index} ---------")
        if index % 100 == 0:
            print(index)
        for (i, j) in selection:
            (arg1_i, op_i, arg2_i, out_i) = ops2[i]
            (arg1_j, op_j, arg2_j, out_j) = ops2[j]
            # print(f"swap {out_i} <-> {out_j}")
            ops2[i] = (arg1_i, op_i, arg2_i, out_j)
            ops2[j] = (arg1_j, op_j, arg2_j, out_i)
        knowns = eval(input, ops2)
        if knowns == None:
            continue
        z = binaryToDecimal(knowns, 'z')
        x = binaryToDecimal(knowns, 'x')
        y = binaryToDecimal(knowns, 'y')
        # print("----------------")
        if isSolution(x, y, z):
            return [ ops2[i][3] for p in selection for i in p ]
    return None

def analyzeDeps(current, ops, prev, result):
    result[current] = prev
    for (arg1, _, arg2, out) in ops:
        if out == current:
            analyzeDeps(arg1, ops, prev + [current], result)
            analyzeDeps(arg2, ops, prev + [current], result)

#################

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

deps = dict()
for op in ops:
    out = op[3]
    if out.startswith('z'):
        analyzeDeps(out, ops, [], deps)

print(deps)    

#result = solve(inputs, ops, 2, lambda x, y, z: x & y == z)
result = solve(inputs, ops, 4, lambda x, y, z: x + y == z, deps)

#print(result)
#print(','.join(sorted(result)))




