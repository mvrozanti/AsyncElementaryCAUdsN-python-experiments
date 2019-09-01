#!/usr/bin/env python
import code
rule = 30
# rule set:
# 111 110 101 100 011 010 001 000
#  y   y   y   y   y   y   y   y
rule_transitions = [int(y) for y in format(rule,'#010b')[2:]]
t = w = 10
spacetime = [[0]*w]; spacetime[-1][w//2-1] = 1

for i in range(t):
    future_space = []
    space = spacetime[-1]
    for x in range(len(space)):
        ln = space[x-1]
        mn = space[x]
        rn = space[(x+1)%w]
        ix = 7 - ((ln << 2) + ((mn << 1) + rn))
        y = rule_transitions[ix]
        future_space += [y]
    spacetime += [future_space]

for timestep in spacetime:
    print(timestep)
