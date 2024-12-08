from collections import defaultdict

filename = 'day8/input.txt'
with open(filename, 'r') as file:
    lines = file.read().splitlines()

height = len(lines)
width = len(lines[0])

antennas = defaultdict(list)
antennas.setdefault('missing_key', 'default value')
for h in range(height):
    for w in range(width):
        ch = lines[h][w]
        if ch != '.':
            antennas[ch].append((w, h))

def inside(x, y):
    return x >= 0 and x < width and y >= 0 and y < height

nodes = set()
for id, positions in antennas.items():
    if id == 'missing_key':
        continue
    numPositions = len(positions)
    for i in range(0,numPositions):
        for j in range(i+1,numPositions):
            (x1,y1) = positions[i]
            (x2,y2) = positions[j]
            (dx,dy) = (x2-x1, y2-y1)
            di = 0
            while True:
                (xn1,yn1) = (x1-dx*di, y1-dy*di)    
                if inside(xn1, yn1):
                    nodes.add((xn1,yn1))
                    di += 1
                else:
                    break
            di = 1
            while True:
                (xn2,yn2) = (x1+dx*di,y1+dy*di)
                if (inside(xn2,yn2)):
                    nodes.add((xn2,yn2))
                    di += 1
                else:
                    break


print(len(nodes))