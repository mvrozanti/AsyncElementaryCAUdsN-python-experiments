#!/usr/bin/env python
import argparse
import code
import itertools
import json
import os
try:
    LINES, COLS = [int(d) for d in os.popen('stty size', 'r').read().split()]
except:
    LINES, COLS = 30,30
DEBUG = True

"""
spacetime generation
"""
def gen_mid_spacetime(w): 
    spacetime = [[0]*w]
    spacetime[0][w//2-1] = 1
    return spacetime

read_schemes_from_file = lambda fp: json.load(open(fp))

gen_space_combo = lambda w: list(itertools.product([0, 1], repeat=w))       # all possible configurations for w-wide space

"""
get rule transitions as an array indexed by neighbor configuration, like so:
# 111 110 101 100 011 010 001 000
#  y0  y1  y2  y3  y4  y5  y6  y7
"""
get_rule_transitions = lambda r: [int(y) for y in format(r,'#010b')[2:]]

"""
returns what rule should be applied for this combination of neighbors
"""
get_transition_ix = lambda ln,mn,rn: 7 - ((ln << 2) + (mn << 1) + rn)

get_neighbors = lambda x,space: [space[x-1], space[x], space[(x+1)%len(space)]]

def print_spacetime(spacetime, zero=0, one=1):
    for space in spacetime:
        [print(one if cell else zero, end='') for cell in space]
        print()

def run_sync(rule, t, w):
    """
    returns spacetime after executing the rule synchronously for t steps in a w-wide space
    """
    rule_transitions = get_rule_transitions(rule)
    space = list(gen_mid_spacetime(w)[0])
    yield space
    for _ in range(t):
        future_space = list(space)
        for ci in range(w):                             # iterate over the present space's cells
            ln,mn,rn = get_neighbors(ci, space)         # get neighborhood
            ix_transition = get_transition_ix(ln,mn,rn) # get transition ix
            y = rule_transitions[ix_transition]         # get next cell state
            future_space[ci] = y                        # update cell
        space = list(future_space)                      # update space
        yield future_space

def run_async(rule, t, w, ranks, init_space=None):
    rule_transitions = get_rule_transitions(rule)
    assert len(ranks) == 8
    space = init_space if init_space else list(gen_mid_spacetime(w)[0])
    yield space
    giotbr = grouped_indexes_of_transitions_by_rank = [[ix for ix,rank in enumerate(ranks) if rank == i] \
            for i in range(1,8)] 
    for _ in range(t):
        future_space = list(space)
        for transition_indexes in giotbr:
            if transition_indexes:
                for ci in range(w):
                    ln,mn,rn = get_neighbors(ci, space)
                    ix = get_transition_ix(ln,mn,rn)
                    if ix in transition_indexes:
                        future_space[ci] = rule_transitions[ix]
                space = future_space
        yield future_space

def is_spacetime_conservative(spacetime):
    energy = next(spacetime).count(1)
    for space in spacetime:
        if space.count(1) != energy:
            return False
    return True

def is_rule_conservative(rule, t, w, ranks=None):
    init_spaces = gen_space_combo(w)
    ranks = ranks if ranks else [1]*8
    for init_space in init_spaces:
        final_spacetime = run_async(rule, t, w, ranks, init_space=init_space)
        if not is_spacetime_conservative(final_spacetime):
            return False
    return True

def main(args):
    if args.scheme:
        if args.scheme[0] == '(' and args.scheme[-1] == ')':
            scheme = eval(args.scheme)
            spacetime = run_async(args.rule, args.timesteps - 1, args.width, scheme)
            if not args.dont_render:
                print_spacetime(spacetime, args.zero, args.one)
            if args.conservative_check:
                print('Is conservative:', is_spacetime_conservative(spacetime))
        else:
            schemes = read_schemes_from_file(args.scheme)
            for scheme in schemes:
                spacetime = run_async(args.rule, args.timesteps - 1, args.width, scheme)
                if not args.dont_render:
                    print_spacetime(spacetime, args.zero, args.one)
                if args.conservative_check:
                    print('Is conservative:', is_spacetime_conservative(spacetime))
    else:
        spacetime = run_sync(args.rule, args.timesteps - 1, args.width)
        if not args.dont_render:
            print_spacetime(spacetime, args.zero, args.one)
        if args.conservative_check:
            print('Is conservative:', is_spacetime_conservative(spacetime))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='aeca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-s', '--scheme',               default=None,   metavar='ASYNCHRONOUS-SCHEME', help='async scheme to run (x0,x1,x2,x3,x4,x5,x6,x7) for xn in [1,7]')
    parser.add_argument('-r', '--rule',                 default=30,     metavar='RULE-ID',             help='rule in the Wolfram classification scheme', type=int)
    parser.add_argument('-t', '--timesteps',            default=LINES,  metavar='TIMESTEPS',           help='timesteps to run', type=int)
    parser.add_argument('-w', '--width',                default=COLS,   metavar='WIDTH',               help='space width', type=int)
    parser.add_argument('-0', '--zero',                 default='0',    metavar='CHAR',                help='replace zeroes by CHAR')
    parser.add_argument('-1', '--one',                  default='1',    metavar='CHAR',                help='replace ones by CHAR')
    parser.add_argument('-c', '--conservative-check',   action='store_true',                           help='show whether automata generated are conservative')
    parser.add_argument('-R', '--dont-render',          action='store_true',                           help='toggle rendering')
    args = parser.parse_args()
    main(args)
