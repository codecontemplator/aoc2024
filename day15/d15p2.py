filename = "day15/input.txt"
with open(filename,'r') as file:
    lines = file.read().splitlines()

split =  [i for i, s in enumerate(lines) if s == ""][0]
mapLines = lines[:split]
moves = ''.join(lines[split+1:])

def expand(ch):
    match ch:
        case '#': 
            return "##"
        case 'O': 
            return "[]"
        case '.': 
            return ".."
        case '@': 
            return "@."

map = [[ ch2 for ch in line for ch2 in expand(ch) ] for line in mapLines ]
width = len(map[0])
height = len(map)

robot = None
for y in range(height):
    for x in range(width):
        if map[y][x] == '@':
            map[y][x] = '.'
            robot = (x,y)
            break
    if robot != None:
        break

def moveVertical(y, xs, dy):
    if (len(xs) == 0):
        return

    xsNext = []
    for x in xs:
        if map[y+dy][x] == '[':
            xsNext.append(x)
            xsNext.append(x+1)
        elif map[y+dy][x] == ']':
            xsNext.append(x-1)
            xsNext.append(x)
    xsNext = list(set(xsNext))

    moveVertical(y+dy, xsNext, dy)
    for x in xs:
        map[y+dy][x] = map[y][x]
        map[y][x] = '.'

def canMoveVertical(y, xs, dy):
    if (len(xs) == 0):
        return True

    xsNext = []
    for x in xs:
        if map[y+dy][x] == '[':
            xsNext.append(x)
            xsNext.append(x+1)
        elif map[y+dy][x] == ']':
            xsNext.append(x-1)
            xsNext.append(x)
        elif map[y+dy][x] == '#':
            return False
    xsNext = list(set(xsNext))
        
    return canMoveVertical(y+dy, xsNext, dy)

def canMoveHorizontal(x, y, dx):
    xn = x + dx
    ch = map[y][xn]
    while ch in "[]":
        xn += dx
        ch = map[y][xn]

    if map[y][xn] == '#':
        return False
    else:
        return True

def moveHorizontal(x, y, dx):
    xn = x + dx
    while map[y][xn] in "[]":
        xn += dx

    for xi in range(xn, x, -dx):
        map[y][xi] = map[y][xi-dx]

def moveBy(ch):
    global robot
    (x,y) = robot
    match ch:
        case '^':
            if canMoveVertical(y, [x], -1):
                moveVertical(y, [x], -1)
                robot = (x, y-1)
        case 'v':
            if canMoveVertical(y, [x], 1):
                moveVertical(y, [x], 1)
                robot = (x, y+1)
        case '<':
            if canMoveHorizontal(x, y, -1):
                moveHorizontal(x, y, -1)
                robot = (x-1, y)
        case '>':
            if canMoveHorizontal(x, y, 1):
                moveHorizontal(x, y, 1)
                robot = (x+1, y)
        case _:
            raise "Bad"
        
def printMap():
    (rx,ry) = robot
    for y in range(height):
        row = [ map[y][x] for x in range(width) ]
        if ry == y:
            row[rx] = '@'
        l = ''.join(row)
        print(l)

def gpsScore():
    score = 0
    for y in range(height):
        for x in range(width):
            if map[y][x] == '[':
                score += y * 100 + x
    return score

#printMap()
#print(moves)
#print(robot)

for i,m in enumerate(moves):
     #printMap()
     #print(f"move: {m} ({i})")
     moveBy(m)

#printMap()

print(gpsScore())
