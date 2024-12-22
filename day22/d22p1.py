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

def genSecret(seed, numIter):
    secret = seed
    for _ in range(numIter):
        secret = nextSecret(secret)
    return secret

filename = "day22/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()

seeds = [int(line) for line in lines]

result = 0
for seed in seeds:
    x = genSecret(seed, 2000)
    # print(x)
    result += x

print(result)    