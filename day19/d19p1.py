from functools import lru_cache

filename = "day19/input.txt"

with open(filename, 'r') as file:
    lines = file.read().splitlines()

patterns = lines[0].split(", ") 
designs = lines[2:]

@lru_cache(maxsize=None)
def search(design):
    if len(design) == 0:
        return []
    candidates = [ pattern for pattern in patterns if design.startswith(pattern) ]
    candidatesSorted = sorted(candidates, key=len, reverse=True)
    for candidate in candidatesSorted:
        design2 = design.removeprefix(candidate)
        if (result := search(design2)) != None:
            return [candidate] + result
    return None

validDesigns = [ design for design in designs if search(design) != None ]
print(len(validDesigns))
