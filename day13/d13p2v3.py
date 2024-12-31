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

def gcd_extended(a, b):
    """
    Extended Euclidean Algorithm.
    Returns gcd, x, y such that gcd = ax + by.
    """
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = gcd_extended(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y

def solve_diophantine(a, b, c):
    """
    Solves the linear Diophantine equation ax + by = c.
    Returns a particular solution (x, y) and general solution components.
    """
    gcd, x0, y0 = gcd_extended(a, b)
    
    if c % gcd != 0:
        return None, "No solution exists because gcd(a, b) does not divide c."
    
    # Scale the solution to match c
    x0 *= c // gcd
    y0 *= c // gcd
    
    # General solution components
    general_x = b // gcd
    general_y = -a // gcd
    
    return (x0, y0), (general_x, general_y)

def costOf(machine, solution, general_solution, t):
    a = solution[0] + general_solution[0] * t
    b = solution[1] + general_solution[1] * t
    if a < 0 or b < 0:
        return 0
    s1 = machine.dxA * a + machine.dxB * b
    if s1 != machine.px:
        return 0
    s2 = machine.dyA * a + machine.dyB * b
    if s2 != machine.py:
        return 0
    
    costA = 3
    costB = 1
    costTemp = costA * a + costB * b

    return costTemp

def solveMachine(machine):
    solution, general_solution = solve_diophantine(machine.dxA, machine.dxB, machine.px)
    if solution == None:
        return None
    solution2, _ = solve_diophantine(machine.dyA, machine.dyB, machine.py)
    if solution2 == None:
        return None

    temp1 = machine.py - machine.dyA * solution[0] - machine.dyB * solution[1]
    temp2 = machine.dyA * general_solution[0] + machine.dyB * general_solution[1]
    tTest = round(temp1 / temp2)
    costTemp = costOf(machine, solution, general_solution, tTest)
    return costTemp

totalCost = 0
offset = 10000000000000
for i, machine in enumerate(machines):
    print(f"machine {i}:")
    machine.px += offset
    machine.py += offset
    cost = solveMachine(machine)
    if cost != None:
        print(cost)
        totalCost += cost

print(totalCost)        

