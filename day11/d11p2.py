from collections import defaultdict

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

def dedup(arr):
    grouped = defaultdict(int)
    for key, value in arr:
        grouped[key] += value
    return grouped.items()

def process(arr):
    return dedup([ (v,c) for (a,c) in arr for v in processValue(a) ])


filename = 'day11/input.txt'
with open(filename, 'r') as file:
    arr = [(int(x), 1) for x in file.read().split()]


for _ in range(75):
    arr = process(arr)

print(sum([ c for (_,c) in arr]))
