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

def solve_single_diophantine(a, b, c):
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

def solve_system_of_two_equations(a1, b1, c1, a2, b2, c2):
    """
    Solves a system of two linear Diophantine equations:
    a1x + b1y = c1
    a2x + b2y = c2
    """
    # Step 1: Solve the first equation
    solution1, general_solution1 = solve_single_diophantine(a1, b1, c1)
    if solution1 is None:
        return None, "No solution exists for the first equation."
    
    x1, y1 = solution1
    gx, gy = general_solution1
    
    # Step 2: Substitute x and y from the general solution of the first equation into the second equation
    # x = x1 + gx*t, y = y1 + gy*t
    # Substituting into a2x + b2y = c2:
    # a2*(x1 + gx*t) + b2*(y1 + gy*t) = c2
    # (a2*gx + b2*gy)*t = c2 - (a2*x1 + b2*y1)
    coeff_t = a2 * gx + b2 * gy
    const = c2 - (a2 * x1 + b2 * y1)
    
    # Step 3: Solve for t in coeff_t * t = const
    solution2, general_solution2 = solve_single_diophantine(coeff_t, 0, const)
    if solution2 is None:
        return None, "No solution exists after substitution into the second equation."
    
    t0 = solution2[0]
    
    # Step 4: Back-substitute t = t0 into the general solution of the first equation
    final_x = x1 + gx * t0
    final_y = y1 + gy * t0
    
    # General solution for the system
    general_x = gx * general_solution2[0]
    general_y = gy * general_solution2[0]
    
    return (final_x, final_y), (general_x, general_y)


def solveMachine(machine, offset = 0):
    solution, general_solution = (
        solve_system_of_two_equations(
            machine.dxA, machine.dxB, machine.px + offset,
            machine.dyA, machine.dyB, machine.py + offset
        )
    )

    if solution == None:
        return None
    
    tx1 = -solution[0] / general_solution[0]
    tx2 = -solution[1] / general_solution[1]    

    tmin = math.floor(min(tx1,tx2))
    tmax = math.ceil(max(tx1,tx2))

    minCost = None
    costA = 3
    costB = 1
    for t in range(tmin, tmax, 1):
        a = solution[0] + general_solution[0] * t
        b = solution[1] + general_solution[1] * t
        if a < 0 or b < 0:
            continue
        s1 = machine.dxA * a + machine.dxB * b
        if s1 != machine.px:
            continue
        s2 = machine.dyA * a + machine.dyB * b
        if s2 != machine.py:
            continue
        cost = costA * a + costB * b
        if minCost == None or cost < minCost:
            minCost = cost
    return minCost

totalCost = 0
for i, machine in enumerate(machines):
    print(f"machine {i}:")
    print(f"  {machine.dxA}*x + {machine.dxB}*y == {machine.px}")
    print(f"  {machine.dyA}*x + {machine.dyB}*y == {machine.py}")

    cost = solveMachine(machine, 0)
    if cost != None:
        print(cost)
        totalCost += cost

print(totalCost)        

# Example: Solve 12x + 15y = 21
#a, b, c = 12, 15, 21
#a,b,c = 38,11,1461
#a,b,c = 94,22,8400
#a,b,c = 34,67,5400
#solution, general_solution = solve_diophantine(a, b, c)

# machine 0:
#   38*x + 11*y == 1461
#   33*x + 47*y == 2879
# x=26, y=43. 38*26 + 11*43 == 1461
# x=26, y=43. 33*26 + 47*43 == 2879
# machine 1:
#   77*x + 15*y == 11953
#   14*x + 80*y == 16146

# if solution:
#     print(f"Particular solution: x = {solution[0]}, y = {solution[1]}")
#     print(f"General solution: x = {solution[0]} + {general_solution[0]}t, y = {solution[1]} + {general_solution[1]}t (t ∈ Z)")
# else:
#     print(general_solution)

# t1 = -solution[0] / general_solution[0]
# t2 = -solution[1] / general_solution[1]

# print(t1, t2)
# tmin = math.floor(min(t1,t2))
# tmax = math.ceil(max(t1,t2))

# for t in range(tmin, tmax, 1):
#     x = solution[0] + general_solution[0] * t
#     y = solution[1] + general_solution[1] * t
#     print(t,x,y,a*x+b*y,c)


    
