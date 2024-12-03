import re

with open("input.txt", "r") as file:
    content = file.read()

matches = re.findall("mul\((\d+),(\d+)\)", content)

print(sum([int(a)*int(b) for (a,b) in matches]))
