def unpack(data):
    arr = []
    for i,d in enumerate(data):
        size = int(d)
        val = i // 2 if i%2 == 0 else -1
        arr += [ val for _ in range(size) ] 
    return arr
    
def pack(arr):
    fi = 0
    bi = len(arr)-1
    while True:
        while fi < bi and arr[bi] < 0:
            bi -= 1
        if fi >= bi:
            break
        if arr[fi] < 0:
            arr[fi] = arr[bi]
            arr[bi] = -1
            fi += 1
        else:
            fi += 1
    return arr[:fi+1]

def checksum(arr):
    result = 0
    for i,a in enumerate(arr):
        result += i * a
    return result

filename = "day9/input.txt"
with open(filename, "r") as file:
    data = file.read()

uarr = unpack(data)
parr = pack(uarr)

print(checksum(parr))