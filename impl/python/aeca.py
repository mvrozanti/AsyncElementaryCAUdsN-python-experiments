#!/usr/bin/env python
import atexit
import argparse
import code
import itertools
import json
import os
import random
import pickle
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

T = lambda w: 2**w+1

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

111 110 101 100 011 010 001 000
 y0  y1  y2  y3  y4  y5  y6  y7
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

def render_image(spacetime, rule, scheme, measure_complexity=False):
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

def run_async(rule, w, t, ranks, init_space=None):
    rule_transitions = get_rule_transitions(rule)
    # space = args.initial_configuration if args.initial_configuration else gen_mid_spacetime(args.width)[0] 
    space = init_space if init_space else gen_mid_spacetime(w)[0]
    macrospacetime = [space]
    gitr = [[tr_ix for tr_ix,rank in enumerate(ranks) if rank == i] for i in range(1,9)]
    yield macrospacetime[-1]
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
    spacetime = run_async(rule, w, t, scheme, init_space=init_space)
    spacetime_is_conservative = is_spacetime_conservative(spacetime)
    return spacetime_is_conservative

def is_rule_conservative(rule, w, t, scheme=[1]*8, save_to=None):
    return all(run_and_check(rule, w, t, scheme, init_space) for init_space in gen_space_combo(w))

def normalize_args(args):
    if args.initial_configuration:
        args.initial_configuration = [int(c) for c in args.initial_configuration]
        args.width = len(args.initial_configuration)
    if not args.timesteps:
        args.timesteps = T(args.width)
    if args.pairs:
        args.pairs = json.load(open(args.pairs))
    elif args.schemes:
        prev_dirname = f'{args.rule:03d}-{args.width-1}x{T(args.width-1)}'
        schemes_json = f'{prev_dirname}/{prev_dirname}.json'
        if all([str.isdigit(c) for scheme in args.schemes for c in scheme]):
            if len(args.schemes[0]) != 8:
                print(f'schemes must have length of 8, this scheme {args.schemes[0]} has length={len(args.schemes[0])}', file=sys.stderr)
                sys.exit(1)
            args.schemes = [[int(c) for c in scheme] for scheme in args.schemes]
        elif op.exists(prev_dirname) and op.exists(schemes_json):
            args.schemes = json.load(open(schemes_json))
        else:
            args.schemes = read_schemes_from_file(args.schemes[0])

def save_json(conservative_at, dirname):
    op.exists(dirname) or os.mkdir(dirname)
    json.dump(conservative_at, open(f'{dirname}/{dirname}.json', 'w'))

def gracefully_exit(conservative_at, savepoint_file_path):
    print(f'Exiting with {len(conservative_at)} conservative schemes')
    pickle.dump(conservative_at, open(savepoint_file_path, 'wb'))
    sys.exit(0)

def listen(args):
    from synthesizer import Player, Synthesizer, Waveform
    player = Player()
    player.open_stream()
    synthesizer = Synthesizer(osc1_waveform=Waveform.sine, osc1_volume=1.0, use_osc2=False)
    maxn = 2**args.width
    from math import log
    for s in spacetime:
        out = 0
        chords = []
        for i,bit in enumerate(s):
            out = (out << 1) | bit
            if not i % 32: 
                chords += [log(out,2) if out else 0]
                out = 0
        print(chords)
        # player.play_wave(synthesizer.generate_constant_wave(out, 0.1))
        player.play_wave(synthesizer.generate_chord(chords, 0.01))

def spacetime_solves_majority_problem(spacetime):
    init_space_majority_state = max(spacetime[0], key=spacetime[0].count)
    for space in spacetime[1:]:
        if space.count(init_space_majority_state) == len(space):
            return True
    return False

def get_majority_problem_score(rule, scheme, w, render=False):
    if not w % 2:
        print(f'Majority problem does not support w={w}')
        return False
    t = T(w)
    score = 0
    for init_space in gen_space_combo(w):
        spacetime = list(run_async(rule, w, t, scheme, init_space=init_space))
        score += int(spacetime_solves_majority_problem(spacetime))
    return score

def main(args):
    normalize_args(args)
    if args.dct_check:
        scores = {}
        for rule,schemes in args.pairs.items():
            rule = int(rule)
            dirname = f'{rule:03d}-{args.width}x{args.timesteps}'
            op.exists(dirname) or os.mkdir(dirname)
            scores_filename = f'{dirname}/scores.json'
            if not op.exists(scores_filename):
                for scheme in schemes:
                    score_rule_scheme = get_majority_problem_score(rule, scheme, args.width, render=args.png_render)
                    scores[stringify_scheme(scheme)] = score_rule_scheme
                json.dump(scores, open(scores_filename, 'w'))
        sys.exit(0)
    savepoint_file_path = f'{dirname}/{dirname}.pkl'
    conservative_schemes = pickle.load(open(savepoint_file_path, 'rb')) if op.exists(savepoint_file_path) else []
    tqdm_schemes = tqdm.tqdm([s for s in args.schemes if (s not in conservative_schemes or not args.conservative_check)], dynamic_ncols=True)
    args.conservative_check and atexit.register(gracefully_exit, conservative_schemes, savepoint_file_path)
    for scheme in tqdm_schemes:
        stringified_scheme = stringify_scheme(scheme)
        type(tqdm_schemes) is not list and tqdm_schemes.set_description(f'Rendering {dirname}-{stringified_scheme}')
        spacetime = None
        if args.png_render is not None or args.terminal_render or args.listen:
            spacetime = list(run_async(args.rule, args.width, args.timesteps, scheme))
        if not args.conservative_check:
            args.png_render is not None and render_image(spacetime, args.rule, scheme, measure_complexity=args.measure_complexity, save_to=args.png_render)
        if args.listen:
            listen(args)
        if args.terminal_render: 
            print(f'{dirname}-{stringified_scheme}')
            print_spacetime(spacetime, args.zero, args.one)
            print()
        if args.conservative_check:
            rule_is_conservative = is_rule_conservative(args.rule, args.width, args.timesteps, scheme=scheme, save_to=args.png_render)
            if rule_is_conservative:
                # print(f'{dirname}-{stringified_scheme} is conservative: {rule_is_conservative}')
                conservative_schemes += [scheme]
    if args.conservative_check:
        save_json(conservative_schemes, dirname)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='aeca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-s', '--schemes',  nargs='+',  default=['1'*8],metavar='ASYNCHRONOUS-SCHEME', help='async scheme to run p0p1p2p3p4p5p6p7 for pn in [1,8]')
    parser.add_argument('-r', '--rules',    nargs='+',  default=30,     metavar='RULE-IDS',            help='rules in the Wolfram classification scheme')
    parser.add_argument('-t', '--timesteps',                            metavar='TIMESTEPS',           help='timesteps to run', type=int)
    parser.add_argument('-w', '--width',                                metavar='WIDTH',               help='space width', type=int)
    parser.add_argument('-0', '--zero',                 default='0',    metavar='CHAR',                help='replace zeroes by CHAR when using -o')
    parser.add_argument('-1', '--one',                  default='1',    metavar='CHAR',                help='replace ones by CHAR when using -o')
    parser.add_argument('-c', '--conservative-check',   action='store_true',                           help='output table mapping (scheme,conservability)')
    parser.add_argument('-o', '--terminal-render',      action='store_true',                           help='render in terminal')
    parser.add_argument('-l', '--listen',               action='store_true',                           help='listen to ECA')
    parser.add_argument('-O', '--png-render',           nargs='*',      metavar='dir',                 help='render to file in an optionally chosen directory')
    parser.add_argument('-m', '--measure-complexity',   action='store_true',                           help='measure complexity')
    parser.add_argument('-I', '--initial-configuration',metavar='CONFIG',                              help='use CONFIG as initial configuration')
    parser.add_argument('-p', '--pairs'                ,metavar='RULE_SCHEMES_JSON_FILE_PATH',         help='load rules/schemes json file')
    parser.add_argument('-d', '--dct-check'            ,action='store_true',                           
            help='check if majority problem is solvable by rule and defined schemes')
    args = parser.parse_args()
    main(args)
