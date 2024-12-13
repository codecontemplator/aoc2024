import re
import math

class Machine:
    def __init__(self, dxA, dyA, dxB, dyB, px, py):
        self.dxA = dxA 
        self.dyA = dyA
        self.dxB = dxB
        self.dyB = dyB
        self.px = px
        self.py = py

filename = "day13/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()


i = 0
machines = []
while i < len(lines):
    m = re.match(r"^Button A: X\+(\d+), Y\+(\d+)$", lines[i])
    m2 = re.match(r"^Button B: X\+(\d+), Y\+(\d+)$", lines[i+1])
    m3 = re.match(r"^Prize: X=(\d+), Y=(\d+)$", lines[i+2])
    ma = Machine(
        int(m.group(1)), 
        int(m.group(2)), 
        int(m2.group(1)), 
        int(m2.group(2)), 
        int(m3.group(1)), 
        int(m3.group(2)))
    machines.append(ma)
    i += 4

totalCost = 0
for machine in machines:
    maxA = max(math.ceil(machine.px / machine.dxA), math.ceil(machine.py / machine.dyA))
    maxB = max(math.ceil(machine.px / machine.dxB), math.ceil(machine.py / machine.dyB))
    costA = 3
    costB = 1
    minCost = None 
    for a in range(maxA):
        for b in range(maxB):
            x = a * machine.dxA + b * machine.dxB
            y = a * machine.dyA + b * machine.dyB
            if x == machine.px and y == machine.py:
                cost = a * costA + b * costB
                if minCost == None or cost < minCost:
                    minCost = cost
    if minCost != None:
        totalCost += minCost

print(totalCost)