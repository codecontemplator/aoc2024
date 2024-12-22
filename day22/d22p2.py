import itertools as iter

def mix(a, b):
    return a ^ b

def prune(x):
    return x % 16777216

def nextSecret(secret):
    t0 = secret
    t1 = prune(mix(t0*64, t0))
    t2 = prune(mix(t1//32, t1))
    t3 = prune(mix(t2*2048, t2))
    return t3

def price(secret):
    return secret % 10

def secrets(seed):
    secret = seed
    while True:
        yield secret
        secret = nextSecret(secret)

def seqToPriceMap(seed, numIter):
    gen = iter.pairwise(secrets(seed))
    curSeq = []
    result = dict()
    for _ in range(numIter):
        a, b = next(gen)
        pa, pb = price(a), price(b)
        dp = pb - pa
        if len(curSeq) > 3:
            curSeq = curSeq[1:] + [dp]
        else:
            curSeq.append(dp)

        if len(curSeq) == 4:
            key = tuple(curSeq)
            if not key in result:
                result[key] = pb

    return result
        
filename = "day22/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()

seeds = [int(line) for line in lines]
seqMaps = [seqToPriceMap(seed, 2000) for seed in seeds]
keys = set([ key for seqMap in seqMaps for key in seqMap.keys() ])

maxPrice = -1
maxKey = None
for index, key in enumerate(keys):
    priceTotal = 0
    for seqMap in seqMaps:
        if key in seqMap:
            priceTotal += seqMap[key]
    if priceTotal > maxPrice:
        maxPrice = priceTotal
        maxKey = key
        
print(maxKey, maxPrice)        
