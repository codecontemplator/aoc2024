filename = "input.txt"

matrix = []
with open(filename, 'r') as file:
    for line in file:
        row = list(map(int, line.split()))
        matrix.append(row)

num_safe = 0
for row in matrix:
    diff = [ row[i] - row[i+1] for i in range(len(row) - 1) ]
    safe = (
        all( d > 0 and d <= 3 for d in diff ) 
        or
        all( d < 0 and d >= -3 for d in diff )
    )
    if safe:
        num_safe += 1

print(num_safe)

