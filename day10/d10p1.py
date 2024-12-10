filename = 'day10/input.txt'
with open(filename, 'r') as file:
    lines = file.read().splitlines()


width = len(lines[0])
height = len(lines)

arr = [] 
for y in range(height): 
    row = []
    for x in range(width):
        row += [int(lines[y][x])]
    arr += [row]


def track(x,y,vp):
    if x < 0 or x>=width or y < 0 or y >= height:
        return []
    
    v = arr[y][x]
    if vp + 1 != v:
        return []
    
    if v == 9:
        return [(x,y)]
    
    return track(x+1,y,v) + track(x-1,y,v) + track(x,y-1,v) + track(x,y+1,v)  

heads = [ (x,y) for y in range(height) for x in range(width) if arr[y][x] == 0 ]

result = 0
for (x,y) in heads:
    x = len(set(track(x, y, -1)))
    result += x

print(result)
