#!/usr/bin/env python
import argparse
import code
import itertools
import os
import sys
import json
import os.path as op

mexit = lambda m: print(m, file=sys.stderr) or sys.exit(1)

T = lambda n: 2**n+1 # after this T amount of timesteps, the ECA loops

gen_center_array = lambda n: [1 if i == n//2 else 0 for i in range(n)]

stringify  = lambda s: ''.join([str(p) for p in s])
listify    = lambda s: [1 if p == '_' else int(p) for p in s]

gen_lattice_combo = lambda n: itertools.product([0, 1], repeat=n) # all possible configurations for n-length space

"""
get rule transitions as an array indexed by neighbor configuration, like so:

111 110 101 100 011 010 001 000
 y0  y1  y2  y3  y4  y5  y6  y7
"""
get_rule_transitions = lambda rule: [int(y) for y in format(rule,'#010b')[2:]]

"""
returns what rule should be applied for this combination of neighbors
"""
get_transition_ix = lambda ln,mn,rn: 7 - ((ln << 2) + (mn << 1) + rn)

get_neighbors = lambda x,space: [space[x-1], space[x], space[(x+1)%len(space)]]

def print_lattice(lattice, file_=sys.stdout):
    for space in lattice:
        for cell in space:
            print(cell, end='', file=file_)
        print(file=file_)

def render_image(lattice, filename):
    from PIL import Image
    w,t = len(lattice[0]), len(lattice)
    im = Image.new('RGB', (w, t))
    pixels = []
    for iy,space in enumerate([list(space) for space in lattice]):
        for ix,cell in enumerate(space):
            pixels += [(0,0,0) if cell else (255,255,255)]
    try:
        im.putdata(pixels)
    except Exception as e: 
        print(e)
        code.interact(local=globals().update(locals()) or globals())
    if op.exists(filename):
        mexit(f'{filename} already exists. Halting.')
    im.save(filename)

def run(rule, n, t, scheme, init_space):
    rule_transitions = get_rule_transitions(rule)
    space = list(init_space)
    macrospacetime = [space]
    gitr = [[tr_ix for tr_ix,rank in enumerate(scheme) if rank == i] for i in range(1,9)]
    yield macrospacetime[-1]
    for _ in range(t-1):
        macrotimestep = macrospacetime[-1]
        microspacetime = [macrotimestep]
        for pri,transition_indexes in enumerate(gitr):
            if transition_indexes:
                last_micro_timestep = microspacetime[-1]
                micro_timestep = list(last_micro_timestep)
                for ci in range(n):
                    ln,mn,rn = get_neighbors(ci, microspacetime[-1])
                    tr_ix = get_transition_ix(ln,mn,rn)
                    if tr_ix in transition_indexes:
                        micro_timestep[ci] = rule_transitions[tr_ix]
                microspacetime += [micro_timestep]
        macrospacetime += [microspacetime[-1]]
        yield macrospacetime[-1]

def validate_args(args):
    if args.help:
        print(parser.format_help())
        sys.exit(0)
    args.rule in range(0,256)                          or mexit('Rule must be in [0,255] range.')
    len(args.scheme) == 8                              or mexit("Scheme's length must be 8.")
    args.scheme = listify(args.scheme)
    args.length > 2                                    or mexit("Lattices's length must be greater than 2.")
    if not args.timesteps:
        args.timesteps = T(args.length)
    args.timesteps > 0                                 or mexit('Timestep amount must be greater than 0.')
    args.output = args.output.lower()
    args.output in ['txt', 'png']                      or mexit('Output must be one of: txt, png.')
    if args.initial_configuration:
        if args.initial_configuration == 'center':
            args.initial_configuration = gen_center_array(args.length)
        else:
            args.length == len(args.initial_configuration) or mexit('Initial configuration must match lattice length, if specified.')
            args.initial_configuration = listify(args.initial_configuration) 

def main(args):
    initial_configurations = [args.initial_configuration] if args.initial_configuration else gen_lattice_combo(args.length)
    for ic in initial_configurations:
        lattice = run(args.rule, args.length, args.timesteps, args.scheme, ic)
        filename = f'{args.length}x{args.timesteps}-{args.rule}-{stringify(args.scheme)}-{stringify(ic)}.' + args.output
        if args.output == 'txt':
            if len(initial_configurations) == 1:
                print_lattice(lattice)
            else:
                print_lattice(lattice, file_=open(filename, 'w'))
        elif args.output == 'png':
            render_image(lattice, filename)

if __name__ == '__main__':
    DESC=\
"""
Asynchronous Elementary Cellular Automata Update schedule by Neighbourhood priority

This program generates either a txt or a png file of the ECA stated above. 

The output filename format is fixed as such: <length>x<timesteps>-<rule>-<scheme>-<initial-configuration>.<png|txt>
"""
    help = '--help' in sys.argv or '-h' in sys.argv
    parser = argparse.ArgumentParser(prog='aecaudsn.py', description=DESC, formatter_class=argparse.RawTextHelpFormatter, add_help=False)
    parser.add_argument('-h' , '--help'                  , action='store_true'           , help='''Show this help message and exit.
            ''')
    parser.add_argument('-n' , '--length'                , metavar='LENGTH'              , help='''Lattice length, n.
            '''                     , type=int, required=not help)
    parser.add_argument('-t' , '--timesteps'             , metavar='TIMESTEPS'           , help='''Timesteps to run, t.
Unless specified, this program assumes timesteps=2^length+1.

'''                   , type=int)
    parser.add_argument('-r' , '--rule'                  , metavar='RULE-ID'             , help='''Wolfram-code identifier.
            ''' , type=int, required=not help)
    parser.add_argument('-s' , '--scheme'                , metavar='ASYNCHRONOUS-SCHEME' , help='''Neighborhood priority.
Example: 12345678.
This argument also supports an irrelevant priority. 
Theses cases are represented by an underscore, like in 1_1_1_1_.
            ''', required=True)
    parser.add_argument('-I' , '--initial-configuration' , metavar='CONFIG'              , help='''Initial configuration. 
Unless specified, this program generates lattices for all possible configurations. The length of CONFIG must match LENGTH parameter.
Example: 0001000

''', required=False)

    parser.add_argument('-o' , '--output', default='txt' , metavar='FORMAT'              , help='''Render to FORMAT file. Valid values are 'txt' and 'png'. Default is 'txt'. ''', required=False)
    args = parser.parse_args()
    validate_args(args)
    main(args)

# exps 2, 3:

def should_run_for_next_n(scores_n, cur_n): # {w: {rule: {scheme: score}}}
    if cur_n-2 not in scores_n:
        return True
    for rule in scores_n[cur_n-2]:
        for scheme in scores_n[cur_n-2][rule]:
            if scores_n[cur_n-2][rule][scheme] == T(cur_n-2)-1:
                return True # problem remains undecided
    return False # negative decision

def should_run_pair(scores_n, cur_n, rule, scheme):
    if cur_n-2 not in scores_n:
        return True
    if rule not in scores_n[cur_n-2]:
        return True
    if stringify(scheme) not in scores_n[cur_n-2][rule]:
        return True
    return scores_n[cur_n-2][rule][stringify(scheme)] == T(cur_n-2) - 1

def load_pairs_for_exp_2_and_3():
    uit1 = json.load(open('pairs-1.json'))
    # uit2 = json.load(open('pairs-2.json'))
    selected_pairs = {}
    for rule in uit1:
        selected_pairs[rule] = uit1[rule]
        # selected_pairs[rule] = [tuple(s) for s in uit1[rule]]
    # for rule in uit2:
    #     selected_pairs[rule] = [tuple(s) for s in uit2[rule]]
    return selected_pairs
