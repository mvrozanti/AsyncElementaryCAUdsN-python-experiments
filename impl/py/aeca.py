#!/usr/bin/env python
import code
import argparse

def print_spacetime(spacetime, zero):
    for timestep in spacetime:
        [print(c if c else ' ' if not zero else 0, end='') for c in timestep]
        print()

def run(rule, t, w, asyn=None):
    # rule set:
    # 111 110 101 100 011 010 001 000
    #  y   y   y   y   y   y   y   y
    rule_transitions = [int(y) for y in format(rule,'#010b')[2:]]
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
    return spacetime

def main(args):
    spacetime = run(args.rule, args.timesteps, args.width, asyn=args.asyn)
    print_spacetime(spacetime, args.zero)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='async-eca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-a', '--asyn',    default=None, metavar='ASYNCHRONOUS-SCHEME',  help='async scheme to run (x0,x1,x2,x3,x4,x5,x6,x7) for xn in [1,7]')
    parser.add_argument('-r', '--rule',      default=30,  metavar='RULE ID',       help='rule in the Wolfram classification scheme', type=int)
    parser.add_argument('-t', '--timesteps', default=10,  metavar='TIMESTEPS',     help='timesteps to run (space height)', type=int)
    parser.add_argument('-w', '--width',     default=10,  metavar='WIDTH',         help='space width', type=int)
    parser.add_argument('-0', '--zero', action='store_true', default=False,       help='replace empty space by 0')
    args = parser.parse_args()
    main(args)
