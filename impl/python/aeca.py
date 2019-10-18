#!/usr/bin/env python
from curses import wrapper
import argparse
import code
import curses
import itertools
import json
import os
import random
import sys
import os.path as op
import tqdm
import time

try:
    LINES, COLS = [int(d) for d in os.popen('stty size', 'r').read().split()]
except:
    LINES, COLS = 30,30
DEBUG = True

def measure_complexity(space):
    import zlib
    return len(zlib.compress(bytes(space)))

"""
spacetime generation
"""
def gen_mid_spacetime(w): 
    spacetime = [[0]*w]
    spacetime[0][w//2] = 1
    return spacetime

read_schemes_from_file = lambda fp: json.load(open(fp))

stringify_scheme = lambda s: ''.join([str(c) for c in s])

gen_space_combo = lambda w: itertools.product([0, 1], repeat=w) # all possible configurations for w-wide space

"""
get rule transitions as an array indexed by neighbor configuration, like so:
# 111 110 101 100 011 010 001 000
#  y0  y1  y2  y3  y4  y5  y6  y7
"""
get_rule_transitions = lambda rule: [int(y) for y in format(rule,'#010b')[2:]]

"""
returns what rule should be applied for this combination of neighbors
"""
get_transition_ix = lambda ln,mn,rn: 7 - ((ln << 2) + (mn << 1) + rn)

get_neighbors = lambda x,space: [space[x-1], space[x], space[(x+1)%len(space)]]

def print_spacetime(spacetime, zero=0, one=1):
    for space in spacetime:
        [print(one if cell else zero, end='') for cell in space]
        print()

def render_image(spacetime, rule, scheme, measure_complexity=False, save_to=None):
    from PIL import Image
    w,t = len(spacetime[0]), len(spacetime)
    im = Image.new('RGB', (w, t))
    pixels = []
    for iy,space in enumerate([list(space) for space in spacetime]):
        if measure_complexity:
            compl = (10*measure_complexity(space)) % 255
        for ix,cell in enumerate(space):
            pixels += [(0,0,0) if cell else (255-compl if measure_complexity else 255, (0 if measure_complexity else 255), (0 if measure_complexity else 255))]
    try:
        im.putdata(pixels)
    except Exception as e: 
        print(e)
        code.interact(local=globals().update(locals()) or globals())
    if scheme:
        scheme = '-' + ''.join([str(r) for r in scheme])
    dirname = f'{rule:03d}-{w}x{t}'
    op.exists(dirname) or os.mkdir(dirname)
    im.save(f'{dirname}/{dirname}{scheme}.png')

def run_sync(rule, t, w, init_space=None):
    """
    returns spacetime after executing the rule synchronously for t steps in a w-wide space
    """
    rule_transitions = get_rule_transitions(rule)
    space = init_space if init_space else list(gen_mid_spacetime(w)[0])
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

def run_async(rule, w, t, ranks, init_space=None):
    rule_transitions = get_rule_transitions(args.rule)
    space = args.initial_configuration if args.initial_configuration else gen_mid_spacetime(args.width)[0] 
    macrospacetime = [space]
    yield space
    gitr = [[tr_ix for tr_ix,rank in enumerate(ranks) if rank == i] for i in range(1,9)]
    for t in range(args.timesteps-1):
        macrotimestep = macrospacetime[-1]
        microspacetime = [macrotimestep]
        for pri,transition_indexes in enumerate(gitr):
            if transition_indexes:
                last_micro_timestep = microspacetime[-1]
                micro_timestep = list(last_micro_timestep)
                for ci in range(args.width):
                    ln,mn,rn = get_neighbors(ci, microspacetime[-1])
                    tr_ix = get_transition_ix(ln,mn,rn)
                    if tr_ix in transition_indexes:
                        micro_timestep[ci] = rule_transitions[tr_ix]
                microspacetime += [micro_timestep]
        macrospacetime += [microspacetime[-1]]
        yield macrospacetime[-1]

def is_spacetime_conservative(spacetime):
    energy = next(spacetime).count(1)
    for space in spacetime:
        if space.count(1) != energy:
            return False
    return True

def run_and_check(rule, w, t, scheme, init_space):
    return is_spacetime_conservative(run_async(rule, w, t, scheme, init_space=init_space)) 

def is_rule_conservative(rule, t, w, scheme=None):
    import concurrent.futures
    from multiprocessing import Queue
    from threading import Thread
    init_spaces = gen_space_combo(w)
    scheme = scheme if scheme else [1]*8
    with concurrent.futures.ProcessPoolExecutor() as executor:
        le_tqdm = tqdm.tqdm(executor.map(run_and_check, *zip(*[[rule, w, t, scheme, init_space] for init_space in init_spaces])), leave=False, dynamic_ncols=True, total=2**w)
        for conservative in list(le_tqdm):
            le_tqdm.set_description(f'Rule {rule} is conservative: {conservative}')
            if not conservative:
                return False
        return True

def main(args):
    if args.initial_configuration:
        args.initial_configuration = [int(c) for c in args.initial_configuration]
        args.width = len(args.initial_configuration)
    if args.conservative_check:
        if args.timesteps != (2 ** args.width + 1):
            print('-c implies t=2**w+1', file=sys.stderr)
            sys.exit(1)
        if (args.png_render is not None or args.terminal_render) and args.conservative_check:
            print('-c imples not using -o or -O', file=sys.stderr)
            sys.exit(1)
    dirname = f'{args.rule:03d}-{args.width}x{args.timesteps}'
    if args.schemes:
        if all([str.isdigit(c) for scheme in args.schemes for c in scheme]):
            if len(args.schemes[0]) != 8:
                print(f'schemes must have length of 8, this scheme {args.schemes[0]} has length={len(args.schemes[0])}', file=sys.stderr)
                sys.exit(1)
            args.schemes = [[int(c) for c in scheme] for scheme in args.schemes]
        else:
            args.schemes = read_schemes_from_file(args.schemes[0])
    tqdm_schemes = tqdm.tqdm(args.schemes, dynamic_ncols=True)
    conservative_at = {} # scheme: True|False
    for scheme in tqdm_schemes:
        tqdm_schemes.set_description(f'Rendering {dirname}-{stringify_scheme(scheme)}')
        spacetime = list(run_async(args.rule, args.width, args.timesteps-1, scheme))
        if args.png_render is not None:
            render_image(spacetime, args.rule, scheme, measure_complexity=args.measure_complexity, save_to=args.png_render)
        if args.terminal_render:
            print_spacetime(spacetime, args.zero, args.one)
        if args.conservative_check:
            conservative_at[stringify_scheme(scheme)] = is_rule_conservative(args.rule, args.timesteps, args.width, scheme=scheme)
    if args.conservative_check:
        import csv
        fieldnames = ['Esquema', 'Conservabilidade']
        op.exists(dirname) or os.mkdir(dirname)
        start_time = time.time()
        with open(f'{dirname}/{dirname}.csv', 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader()
            for scheme, conservative in conservative_at.items():
                writer.writerow({'Esquema': scheme, 'Conservabilidade': conservative})
        with open(f'{dirname}/run-time.txt', 'w') as run_time_file:
            run_time_file.write(str(time.time() - start_time))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='aeca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-s', '--schemes',  nargs='+',  default=['1'*8],metavar='ASYNCHRONOUS-SCHEME', help='async scheme to run p0p1p2p3p4p5p6p7 for pn in [1,8]')
    parser.add_argument('-r', '--rule',                 default=30,     metavar='RULE-ID',             help='rule in the Wolfram classification scheme', type=int)
    parser.add_argument('-t', '--timesteps',            default=LINES,  metavar='TIMESTEPS',           help='timesteps to run', type=int)
    parser.add_argument('-w', '--width',                default=COLS,   metavar='WIDTH',               help='space width', type=int)
    parser.add_argument('-0', '--zero',                 default='0',    metavar='CHAR',                help='replace zeroes by CHAR when using -o')
    parser.add_argument('-1', '--one',                  default='1',    metavar='CHAR',                help='replace ones by CHAR when using -o')
    parser.add_argument('-c', '--conservative-check',   action='store_true',                           help='output table mapping (scheme,conservability)')
    parser.add_argument('-o', '--terminal-render',      action='store_true',                           help='render in terminal')
    parser.add_argument('-O', '--png-render',           nargs='*',      metavar='dir',                 help='render to file in an optionally chosen directory')
    parser.add_argument('-m', '--measure-complexity',   action='store_true',                           help='measure complexity')
    parser.add_argument('-I', '--initial-configuration',metavar='CONFIG',                              help='use CONFIG as initial configuration')
    # parser.add_argument('-T', '--save-run-time',        action='store_true',                           help='save run time')
    args = parser.parse_args()
    main(args)
