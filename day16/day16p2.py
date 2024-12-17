from collections import defaultdict
import sys

filename = 'day16/input.txt'

with open(filename, 'r') as file:
    lines = file.read().splitlines()

m = [[ch for ch in line] for line in lines ]

width = len(m[0])
height = len(m)

(initX, initY) = next( ((x,y) for y in range(height) for x in range(width) if m[y][x] == 'S'), None)
(endX, endY) = next( ((x,y) for y in range(height) for x in range(width) if m[y][x] == 'E'), None)

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

def keepOnlyMinCost(costs):
    if len(costs) == 0:
        return []

    result = sorted(costs, key=lambda x: x[0])
    minCost = result[0][0]
    return [ (c, ps) for (c, ps) in result if c == minCost ]

def search(x, y, dx, dy, cost, visited, costMap, path):

    if (x,y) in visited:
        return []

    # if (y==11 and x ==3):
    #     print("?")

    if (x,y,dx,dy) in costMap and cost > costMap[(x,y,dx,dy)]:
        return []
    else:
        costMap[(x,y,dx,dy)] = cost

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

    all = upList + downList + leftList + rightList

    # lp = len(path)    
    # costMap[(x,y,dx,dy)] = [ (c-cost,ps[lp:]) for c, ps in all]

    # costMap[(x,y,0,-1)] = [ (c-cost,ps) for c, ps in upList]
    # costMap[(x,y,0,+1)] = [ (c-cost,ps) for c, ps in downList]
    # costMap[(x,y,-1,0)] = [ (c-cost,ps) for c, ps in leftList] 
    # costMap[(x,y,+1,0)] = [ (c-cost,ps) for c, ps in rightList] 

    return all

sys.setrecursionlimit(20000)

costs = search(initX, initY, 1, 0, 0, frozenset([]), dict(), [])


result = sorted(costs, key=lambda x: x[0])
print(result)
print( [ c for (c,_) in result])

minCost = result[0][0]
minPath = set([ p for (c, ps) in costs if c == minCost for p in ps])

#minPath = set([ p for (c, ps) in costs for p in ps])
#minPath = set(costs[1][1])

for y in  range(height):
    row = [ m[y][x] for x in range(width) ]
    for x in range(width):        
        if (x,y) in minPath:
            row[x] = "O"
    print(f"{str(y).zfill(2)} {''.join(row)}")


print(len(minPath))