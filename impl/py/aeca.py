#!/usr/bin/env python
import code
import argparse
import json
import os
import itertools
LINES, COLS = [int(d) for d in os.popen('stty size', 'r').read().split()]
DEBUG = True

def gen_mid_spacetime(w): 
    """
    for w=3 return [0, 1, 0]
    for w=4 return [0, 1, 0, 0]
    for w=5 return [0, 0, 1, 0, 0]
    etc.
    """
    spacetime = [[0]*w]
    spacetime[0][w//2-1] = 1
    return spacetime

def gen_spacetime_combo(w):
    return list(itertools.product([0, 1], repeat=w))

def print_spacetime(spacetime, zero, one):
    for space in spacetime:
        [print(one if cell else zero, end='') for cell in space]
        print()

def get_rule_transitions(rule):
    """
    get rule transitions as an array indexed by standard neighbor configuration, like so:
    # 111 110 101 100 011 010 001 000
    #  y0  y1  y2  y3  y4  y5  y6  y7
    """
    return [int(y) for y in format(rule,'#010b')[2:]]

def is_spacetime_conservative(spacetime):
    energy = spacetime[0].count(1)
    for space in spacetime[1:]:
        if space.count(1) != energy:
            return False
    return True

def is_rule_conservative(rule, t, w, ranks):
    init_spacetimes = gen_spacetime_combo(w)
    for init_spacetime in init_spacetimes:
        final_spacetime = run_async(rule, t, w, ranks, spacetime=init_spacetime)
        if not is_spacetime_conservative(final_spacetime):
            return False
    return True

def get_neighbors(x, space):
    return space[x-1], space[x], space[(x+1)%len(space)]

def get_transition_ix(ln,mn,rn):
    return 7 - ((ln << 2) + (mn << 1) + rn)

def run_sync(rule, t, w):
    """
    returns spacetime after executing the rule synchronously for t steps in a w-wide space
    """
    rule_transitions = get_rule_transitions(rule)
    spacetime = gen_mid_spacetime(w)
    for _ in range(t):
        space = spacetime[-1]                           # get last iteration's space
        future_space = list(space)
        for ci in range(w):                             # iterate over the present space's cells
            ln,mn,rn = get_neighbors(ci, space)         # get neighborhood
            ix_transition = get_transition_ix(ln,mn,rn) # get transition ix
            y = rule_transitions[ix_transition]         # get next cell state
            future_space[ci] = y
        spacetime += [future_space]                     # update spacetime
    return spacetime

def run_async(rule, t, w, ranks, spacetime=None):
    rule_transitions = get_rule_transitions(rule)
    assert len(ranks) == 8
    spacetime = spacetime if spacetime else gen_mid_spacetime(w)
    for _ in range(t):
        space = spacetime[-1]
        giotbr = grouped_indexes_of_transitions_by_rank = [[ix for ix,rank in enumerate(ranks) if rank == i] \
                for i in range(1,8)] 
        future_space = list(space)
        for transition_indexes in giotbr:
            if transition_indexes:
                for ci in range(w):
                    ln,mn,rn = get_neighbors(ci, space)
                    ix = get_transition_ix(ln,mn,rn)
                    if ix in transition_indexes:
                        future_space[ci] = rule_transitions[ix]
                space = future_space
        spacetime += [future_space]
    return spacetime

def main(args):
    if args.scheme:
        if args.scheme[0] == '(' and args.scheme[-1] == ')':
            scheme = eval(args.scheme)
            spacetime = run_async(args.rule, args.timesteps, args.width, scheme)
            if not args.dont_render:
                print_spacetime(spacetime, args.zero, args.one)
            if args.conservative_check:
                print('Is conservative:', is_spacetime_conservative(spacetime))
        else:
            schemes = json.load(open(args.scheme))
            for scheme in schemes:
                spacetime = run_async(args.rule, args.timesteps, args.width, scheme)
                if not args.dont_render:
                    print_spacetime(spacetime, args.zero, args.one)
                if args.conservative_check:
                    print('Is conservative:', is_spacetime_conservative(spacetime))
    else:
        spacetime = run_sync(args.rule, args.timesteps, args.width)
        if not args.dont_render:
            print_spacetime(spacetime, args.zero, args.one)
        if args.conservative_check:
            print('Is conservative:', is_spacetime_conservative(spacetime))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='aeca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-s', '--scheme',               default=None,   metavar='ASYNCHRONOUS-SCHEME', help='async scheme to run (x0,x1,x2,x3,x4,x5,x6,x7) for xn in [1,7]')
    parser.add_argument('-r', '--rule',                 default=30,     metavar='RULE-ID',             help='rule in the Wolfram classification scheme', type=int)
    parser.add_argument('-t', '--timesteps',            default=LINES,  metavar='TIMESTEPS',           help='timesteps to run (space height)', type=int)
    parser.add_argument('-w', '--width',                default=COLS,   metavar='WIDTH',               help='space width', type=int)
    parser.add_argument('-0', '--zero',                 default='0',    metavar='CHAR',                help='replace zeroes by CHAR')
    parser.add_argument('-1', '--one',                  default='1',    metavar='CHAR',                help='replace ones by CHAR')
    parser.add_argument('-c', '--conservative-check',   action='store_true',                           help='at the end of execution show whether automaton is conservative')
    parser.add_argument('-R', '--dont-render',          action='store_true',                           help='toggle rendering')
    # parser.add_argument('-d', '--debug',                action='store_true',                           help='toggle debugging')
    args = parser.parse_args()
    main(args)
