filename = 'day12/input.txt'

with open(filename, 'r') as file:
    lines = file.read().splitlines()

m = [[ ch for ch in line] for line in lines]
used = [[ False for ch in line] for line in lines]
# print(m)

width = len(m[0])
height = len(m)

def next():
    for y in range(height):
        for x in range(width):
            if not used[y][x]:
                return (x, y)
    return None

def area(region):
    return len(region)

def perimeter(region):
    result = []
    for (x,y) in region:
        if not (x+1,y) in region:
            result.append(((x,y), 0))
        if not (x-1,y) in region:
            result.append(((x,y), 1))
        if not (x,y+1) in region:
            result.append(((x,y), 2))
        if not (x,y-1) in region:
            result.append(((x,y), 3))
    return result

def canUnify(sidei, sidej):
    for ((xi,yi),si) in sidei:
        for ((xj,yj),sj) in sidej:
            if (si != sj):
                continue
            if ((abs(xi-xj) == 1 and yi == yj) or 
                (abs(yi-yj) == 1 and xi == xj)):
                return True
    return False

def unify(sides):
    for i in range(0,len(sides)):
        for j in range(i+1,len(sides)):
            sidei = sides[i]
            sidej = sides[j]
            if canUnify(sidei, sidej):
                sides.remove(sidei)
                sides.remove(sidej)
                sides.append(sidei + sidej)
                return True
    return False

def sides(region):
    per = perimeter(region)
    sides = [[p] for p in per]
    while unify(sides):
        pass
    return len(sides)

def price(region):
    return area(region) * sides(region)

def getRegion(initX, initY):
    ch = m[initY][initX]
    result = []
    stack = [(initX, initY)]
    while len(stack) > 0:
        (x,y) = stack.pop()
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if used[y][x] or m[y][x] != ch:
            continue        
        result.append((x,y))
        used[y][x] = True
        stack.append(((x+1), y))
        stack.append(((x-1), y))
        stack.append((x, (y+1)))
        stack.append((x, (y-1)))
    return result

regions = []
while True:
    init = next()
    if init == None:
        break
    region = getRegion(init[0], init[1])
    regions.append(region)

# for r in regions:
#     print("----")
#     print(m[r[0][1]][r[0][0]])
#     print(sides(r))

print(sum([ price(r) for r in regions ]))
