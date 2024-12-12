def split(w):
    s = str(w)
    p = len(s) // 2
    return int(s[:p]), int(s[p:])

def processValue(v):
    if v == 0:
        return [1]
    
    sv = str(v)        
    if len(sv) % 2 == 0:
        return split(v)
    else:
        return [v*2024]

def process(arr):
    return [ v for a in arr for v in processValue(a) ]

filename = 'day11/input.txt'
with open(filename, 'r') as file:
    arr = [int(x) for x in file.read().split()]


for _ in range(25):
    arr = process(arr)

print(len(arr))