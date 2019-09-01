#!/usr/bin/env python
import code
rule = 30
# rule set:
# 111 110 101 100 011 010 001 000
#  x   x   x   x   x   x   x   x
rule_transitions = [int(x) for x in format(rule,'#010b')[2:][::-1]]
t = w = 10
spacetime = [[0]*w]; spacetime[-1][w//2-1] = 1

for i in range(t):
    future_space = []
    space = spacetime[-1]
    for x in range(len(space)):
        l_n = space[x-1]
        m_n = space[x]
        r_n = space[(x+1)%w]
        ix = 7 - (l_n << 2 + ((m_n << 1) + r_n))
        future_space += [rule_transitions[ix]]
        print(future_space)
        code.interact(local=globals().update(locals()) or globals())
    spacetime += [future_space]

for timestep in spacetime:
    print(timestep)
