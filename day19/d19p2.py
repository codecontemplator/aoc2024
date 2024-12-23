from functools import lru_cache

filename = "day19/input.txt"

with open(filename, 'r') as file:
    lines = file.read().splitlines()

patterns = lines[0].split(", ") 
designs = lines[2:]

@lru_cache(maxsize=None)
def search(design):
    if len(design) == 0:
        return 1
    candidates = [ pattern for pattern in patterns if design.startswith(pattern) ]
    candidatesSorted = sorted(candidates, key=len, reverse=True)
    count = 0
    for candidate in candidatesSorted:
        design2 = design.removeprefix(candidate)
        count += search(design2)
    return count

designCount = [ search(design) for design in designs ]
#print(designCount)
print(sum(designCount))
