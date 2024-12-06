filename = 'day6/input.txt'
with open(filename, 'r') as file:
    data = file.read()
    lines = data.splitlines()

height = len(lines)
width = len(lines[0])

matrix = [
    [ lines[y][x] for x in range(width)] 
    for y in range(height)
]

print(matrix)

i = data.replace('\n','').index('^')
x = i % width
y = i // width
dx = 0
dy = -1

def inside(x, y):
    return x >= 0 and x < width and y >= 0 and y < height

while True:
    matrix[y][x] = 'X'
    x2 = x + dx
    y2 = y + dy
    if not inside(x2,y2):
        break
    elif matrix[y2][x2] == '#':
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


result = len(
    [  1
        for x in range(width)
            for y in range(height)
                if matrix[y][x] == 'X'
            
    ]
)

print(result)