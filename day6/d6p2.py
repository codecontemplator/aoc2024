filename = 'day6/input.txt'
with open(filename, 'r') as file:
    data = file.read()
    lines = data.splitlines()

height = len(lines)
width = len(lines[0])

i = data.replace('\n','').index('^')

def inside(x, y):
    return x >= 0 and x < width and y >= 0 and y < height

def isLoop(blockx, blocky):
    trace = [
        [ [] for x in range(width)] 
        for y in range(height)
    ]
    x = i % width
    y = i // width
    dx = 0
    dy = -1

    while True:
        if (dx,dy) in trace[y][x]:
            return True
        else:
            trace[y][x] += [(dx,dy)]
        x2 = x + dx
        y2 = y + dy
        if not inside(x2,y2):
            return False
        elif lines[y2][x2] == '#' or (x2 == blockx and y2 == blocky):
            match (dx, dy):
                case (0,-1): 
                    dx, dy = (1, 0)
                case (1, 0):
                    dx, dy = (0, 1)
                case (0, 1):
                    dx, dy = (-1,0)
                case (-1,0): 
                    dx, dy = (0,-1)
        else:
            x = x2
            y = y2

result = 0
for y in range(height):
    for x in range(width):
        if lines[y][x] == '.':
            if isLoop(x, y):
                result+=1

print(result)