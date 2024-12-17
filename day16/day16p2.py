from collections import defaultdict
import sys

filename = 'day16/sample2.txt'

with open(filename, 'r') as file:
    lines = file.read().splitlines()

m = [[ch for ch in line] for line in lines ]

width = len(m[0])
height = len(m)

(initX, initY) = next( ((x,y) for y in range(height) for x in range(width) if m[y][x] == 'S'), None)

#         (0,-1)
#   (-1,0)     (1,0)
#         (0,1)
def calculateRotationCost(dx, dy, dx2, dy2):
    if dx == dx2 and dy == dy2:
        return 0  
    if dx == 0 and dx2 == 0:
         return 2000
    if dy == 0 and dy2 == 0:
         return 2000
    return 1000

def search(x, y, dx, dy, cost, visited, costMap, path):
    if (x,y) in visited:
        return []

    # leastKnownCost = costMap[(x,y)]
    # if cost >= leastKnownCost:
    #     return []
    # else:
    #     costMap[(x,y)] = cost

    ch = m[y][x]
    if ch == '#':
        return []

    path2 = path + [(x,y)]
    if ch == 'E':
         return [(cost, path2)]
    
    visited2 = visited | frozenset([(x,y)])

    upCost = calculateRotationCost(dx, dy, 0, -1)
    downCost = calculateRotationCost(dx, dy, 0, 1)
    leftCost = calculateRotationCost(dx, dy, -1, 0)
    rightCost = calculateRotationCost(dx, dy, 1, 0)
    
    upList    = search(x,   y-1,  0, -1, cost + 1 + upCost, visited2, costMap, path2)
    downList  = search(x,   y+1,  0, +1, cost + 1 + downCost, visited2, costMap, path2)
    leftList  = search(x-1, y  , -1,  0, cost + 1 + leftCost, visited2, costMap, path2)
    rightList = search(x+1, y  , +1,  0, cost + 1 + rightCost, visited2, costMap, path2)

    return upList + downList + leftList + rightList

sys.setrecursionlimit(20000)

maxint_defaultdict = defaultdict(lambda: sys.maxsize)
costs = search(initX, initY, 1, 0, 0, frozenset([]), maxint_defaultdict, [])


result = sorted(costs, key=lambda x: x[0])
minCost = result[0][0]
minPath = set([ p for (c, ps) in result if c == minCost for p in ps])


for y in range(height):
    row = [ m[y][x] for x in range(width) ]
    for x in range(width):        
        if (x,y) in minPath:
            row[x] = "O"
    print(''.join(row))


print(len(minPath))