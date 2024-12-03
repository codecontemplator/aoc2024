import re

with open("input.txt", "r") as file:
    content = file.read()

matches = re.findall("mul\((\d+),(\d+)\)|(do\(\))|(don't)", content)

enabled=True
sum=0
for (a,b,do,dont) in matches:
    if do:
        enabled=True
    elif dont:
        enabled=False
    else:
        if enabled:
            sum+=int(a)*int(b)

print(sum)
