#!/usr/bin/env python
rule = 40
# rule set:
# 111 110 101 100 011 010 001 000
#  x   x   x   x   x   x   x   x
rule_set = {int(x) for x in bin(rule)[2:][::-1]}

w = 5
t = 30
space = [[0,0,1,0,0]]

print(rule_set)

for i in range(t):
    new_space = []
    for x in range(len(space[-1])):
        for rule in rule_set:
            pass
