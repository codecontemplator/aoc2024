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
    result = 0
    for (x,y) in region:
        if not (x+1,y) in region:
            result += 1
        if not (x-1,y) in region:
            result += 1
        if not (x,y+1) in region:
            result += 1
        if not (x,y-1) in region:
            result += 1
    return result

def price(region):
    return area(region) * perimeter(region)

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

print(regions)
    
print(sum([ price(r) for r in regions ]))
