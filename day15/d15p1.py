filename = "day15/input.txt"
with open(filename,'r') as file:
    lines = file.read().splitlines()

split =  [i for i, s in enumerate(lines) if s == ""][0]
mapLines = lines[:split]
moves = ''.join(lines[split+1:])

map = [[ ch for ch in line] for line in mapLines ]
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

def move(step):
    global robot
    global map
    (x,y) = robot
    (xn,yn) = step(x,y)
    ch = map[yn][xn]
    if ch == '#':
        return
    if ch == '.':
        robot = (xn,yn)
        return
    if ch == 'O':
        (xi,yi) = (xn,yn)
        while map[yi][xi] == 'O':
            (xi, yi) = step(xi, yi)
        if map[yi][xi] == '.':
            map[yi][xi] = 'O'
            map[yn][xn] = '.'
            robot = (xn, yn)

def moveBy(ch):
    match ch:
        case '^':
            move(lambda x,y: (x,y-1))
        case 'v':
            move(lambda x,y: (x,y+1))
        case '<':
            move(lambda x,y: (x-1,y))
        case '>':
            move(lambda x,y: (x+1,y))
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
            if map[y][x] == 'O':
                score += y * 100 + x
    return score

print(map)
print(moves)
print(robot)

for m in moves:
    #printMap()
    #print(f"move: {m}")
    moveBy(m)


print(gpsScore())
