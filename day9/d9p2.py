def unpack(data):
    arr = []
    for i,d in enumerate(data):
        size = int(d)
        val = i // 2 if i%2 == 0 else None
        arr += [ (val, size) ] 
    return arr

def toStr(arr):
    result = ""
    for i in range(len(arr)):
        v = arr[i]
        if v == None:
            result += '.'
        else:
            result += str(v)
    return result

def pack(arrin):
    arr = arrin.copy()
    print(len(arr))
    i = len(arr)-1
    while i>0:
        # print(toStr(expand(arr)))
        vi, si = arr[i]
        if vi == None:
            i -= 1
            continue
        j = 0
        while j < i:
            vj, sj = arr[j]
            if vj != None:
                j += 1
                continue
            if sj < si:
                j += 1
                continue
            arr[i] = (None, si)
            arr[j] = (vj, sj - si)
            arr.insert(j, (vi, si))
            break
        i -= 1
    return arr

def expand(arr):
    result = []
    for i in range(len(arr)):
        v, s = arr[i]
        for j in range(s):
            result += [v]
    return result

def checksum(arr):
    result = 0
    for i,a in enumerate(arr):
        if a != None:
            result += i * a
    return result

filename = "day9/input.txt"
with open(filename, "r") as file:
    data = file.read()

uarr = unpack(data)
parr = pack(uarr)
earr = expand(parr)
print(checksum(earr))