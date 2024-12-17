import numpy as np
import re
import math

class Machine:
    def __init__(self, dxA, dyA, dxB, dyB, tx, ty):
        self.dxA = dxA 
        self.dyA = dyA
        self.dxB = dxB
        self.dyB = dyB
        self.tx = tx
        self.ty = ty

filename = "day13/sample.txt"
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

costA = 3
costB = 1

# This function checks if integral 
# solutions are possible
def isPossible(a, b, c):
    return (c % math.gcd(a, b) == 0)

def test(a, b, c):
    g = math.gcd(a,b)
    return c / a, c / b

def extended_gcd(a, b):
    """Extended Euclidean Algorithm."""
    if b == 0:
        return a, 1, 0
    gcd_, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd_, x, y

def solve_diophantine(a, b, c):
    """Solve a single linear Diophantine equation ax + by = c."""
    g, x, y = extended_gcd(a, b)
    if c % g != 0:
        return None  # No solution
    # Scale the solution
    x *= c // g
    y *= c // g
    return g, x, y

# Example usage
#a1, b1, c1 = 3, 6, 9
#a2, b2, c2 = 5, 10, 20

#solution = solve_system_of_two(a1, b1, c1, a2, b2, c2)
#print("Solution:", solution)

for m in machines:
    p1 = isPossible(m.dxA, m.dxB, m.tx) 
    p1a = test (m.dxA, m.dxB, m.tx)
    p1b = solve_diophantine(m.dxA, m.dxB, m.tx)
    p2 = isPossible(m.dyA, m.dyB, m.ty)
    print(p1, p2)
    
# cost = np.array([3, 1])
# for m in machines:
#     #A = np.array([[m.dxA, m.dyA], [m.dxB, m.dyB]])
#     #b = np.array([m.tx, m.ty])
#     #x = np.linalg.solve(A, b)
#     #print(x)


