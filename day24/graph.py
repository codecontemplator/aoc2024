import re

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

ops = load()

with open('day24/network2.dot','w') as file:
    file.write("digraph G {\n")
    #file.write("  subgraph cluster_X {\n")
    for i in range(44):
        out = f"x{i:02}"
        file.write(f"    {out} [label=\"{out}\"];\n")
    #file.write("  }\n")
    #file.write("  subgraph cluster_Y {\n")
    for i in range(44):
        out = f"y{i:02}"
        file.write(f"    {out} [label=\"{out}\"];\n")
    #file.write("  }\n")
    #file.write("  subgraph cluster_Z {\n")
    for (out, (arg1, op, arg2)) in ops:
        file.write(f"    {out} [label=\"{out} ({op})\"];\n")
    #file.write("  }\n")

    for (out, (arg1, op, arg2)) in ops:
        file.write(f"  {arg1} -> {out};\n")
        file.write(f"  {arg2} -> {out};\n")
    file.write("}\n")
