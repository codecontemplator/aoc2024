filename = "input.txt"

matrix = []
with open(filename, 'r') as file:
    for line in file:
        row = list(map(int, line.split()))
        matrix.append(row)

def is_safe(row):
    diff = [ row[i] - row[i+1] for i in range(len(row) - 1) ]
    safe = (
        all( d > 0 and d <= 3 for d in diff ) 
        or
        all( d < 0 and d >= -3 for d in diff )
    )
    return safe

num_safe = 0
for row in matrix:
    if is_safe(row):
        num_safe += 1
    else:
        for i in range(len(row)):
            row2 = row[:i] + row[i+1:]
            if is_safe(row2):
                num_safe += 1
                break



print(num_safe)

