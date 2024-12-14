import re
from collections import Counter
from functools import reduce
from operator import mul

filename = "day14/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()

#width = 11
#height = 7

width = 101
height = 103

def parse(line):
    m = re.match(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$", line)
    x = int(m.group(1))
    y = int(m.group(2))
    vx = int(m.group(3))
    vy = int(m.group(4))
    return ((x,y),(vx,vy))

def move(robot):
    ((x,y),(vx,vy)) = robot
    xNew = x + vx
    if xNew < 0:
        xNew += width
    elif xNew >= width:
        xNew -= width
    yNew = y + vy
    if yNew < 0:
        yNew += height
    elif yNew >= height:
        yNew -= height
    return ((xNew, yNew),(vx,vy))

def step(robots):
    return [ move(robot) for robot in robots ]

def quad(robot):
    midX = width // 2
    midY = height // 2
    ((x,y),_) = robot
    q = None
    if x < midX:
        if y < midY:
            q = 0
        elif y > midY:
            q = 2
    elif x > midX:
        if y < midY:
            q = 1
        elif y > midY:
            q = 3
    return q

def display(robots, f):
    m = [[ '.' for _ in range(width) ] for _ in range(height)]
    for ((x,y),_) in robots:
        m[y][x] = 'X'
    for y in range(height):
        s = ''.join(m[y])
        print(s, file=f)

robots = [ parse(line) for line in lines ]
with open('day14/tmp2.txt', 'w') as f:
    simLen = 10000
    for i in range(simLen):
        print(f"{i}:", file=f)
        robots = step(robots)
        display(robots, f)
        print('--', file=f)
