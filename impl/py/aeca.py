#!/usr/bin/env python
import code
import argparse

def gen_spacetime(w): 
    """
    for w=3 return [0, 1, 0]
    for w=4 return [0, 1, 0, 0]
    for w=5 return [0, 0, 1, 0, 0]
    etc.
    """
    spacetime = [[0]*w]
    spacetime[0][w//2-1] = 1
    return spacetime

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

# def get_ranked_transitions(transitions, scheme):
#     """
#     returns a matrix of the transitions indexed by transition ranking
#     """
#     ranked_transitions = {}
#     for ix,rank in enumerate(scheme):
#         ranked_transitions[rank] = ix,transitions[ix]
#     code.interact(local=globals().update(locals()) or globals())
#     return ranked_transitions

def run_sync(rule, t, w):
    """
    returns spacetime after executing the rule synchronously for t steps in a w-wide space
    """
    rule_transitions = get_rule_transitions(rule)
    spacetime = gen_spacetime(w)
    for _ in range(t):
        future_space = []
        space = spacetime[-1]           # get last iteration's space
        for x in range(len(space)):         # iterate over the present space
            ln = space[x-1]                         # get neighbours
            mn = space[x]                           # <^
            rn = space[(x+1)%w]                     # <^
            ix = 7 - ((ln << 2) + ((mn << 1) + rn)) # get transition index
            y = rule_transitions[ix]                # get next cell state
            future_space += [y]                     # add to future space
        spacetime += [future_space]     # update spacetime
    return spacetime

def run_async(rule, t, w, ranks):
    rule_transitions = get_rule_transitions(rule)
    spacetime = gen_spacetime(w)
    for _ in range(t):
        future_space = [0]*w
        space = spacetime[-1]
        for rank_ix in range(8): # iterate over ranks
            i_priority_transition_indexes = [i for i,ix_rank in enumerate(ranks) if ix_rank==ranks[rank_ix]]
            for tran_ix in i_priority_transition_indexes:
                for x in range(len(space)):
                    ln = space[x-1]
                    mn = space[x]
                    rn = space[(x+1)%w]
                    ix = 7 - ((ln << 2) + ((mn << 1) + rn))
                    if ix == tran_ix:
                        y = rule_transitions[ix]
                        future_space[x] = y
            # print(future_space)
            # code.interact(local=globals().update(locals()) or globals())
        spacetime += [future_space]
    return spacetime

def main(args):
    if args.scheme:
        scheme = eval(args.scheme)
        assert len(scheme) == 8
        spacetime = run_async(args.rule, args.timesteps, args.width, scheme)
    else:
        spacetime = run_sync(args.rule, args.timesteps, args.width)
    print_spacetime(spacetime, args.zero, args.one)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='aeca', description='Asynchronous Elementary Cellular Automata')
    parser.add_argument('-s', '--scheme',    default=None,   metavar='ASYNCHRONOUS-SCHEME', help='async scheme to run (x0,x1,x2,x3,x4,x5,x6,x7) for xn in [1,7]')
    parser.add_argument('-r', '--rule',      default=30,     metavar='RULE ID',             help='rule in the Wolfram classification scheme', type=int)
    parser.add_argument('-t', '--timesteps', default=30,     metavar='TIMESTEPS',           help='timesteps to run (space height)', type=int)
    parser.add_argument('-w', '--width',     default=30,     metavar='WIDTH',               help='space width', type=int)
    parser.add_argument('-0', '--zero',      default='0',    metavar='CHAR',                help='replace zeroes by CHAR')
    parser.add_argument('-1', '--one',       default='1',    metavar='CHAR',                help='replace ones by CHAR')
    args = parser.parse_args()
    main(args)
