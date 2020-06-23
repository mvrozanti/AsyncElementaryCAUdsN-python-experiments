#!/usr/bin/env python
# Problema: dentre os pares ⟨R,E⟩ selecionados, quais são candidatos para resolver o problema da maioria? 
# No caso de não haver nenhum, contar os scores para cada comprimento de reticulado. 
#
# Problem: among the selected ⟨R,E⟩ pairs, which of them are candidates to solve the density classification task? 
# In case there are none, count scores for each lattice length.

from aecaudsn import run, T, gen_lattice_combo, should_run_for_next_n, should_run_pair, stringify, load_pairs_for_exp_2_and_3
import code
import itertools
import json
from tqdm import tqdm
import pandas as pd
import sys

def lattice_solves_majority_problem(lattice):
    init_space_majority_state = max(lattice[0], key=lattice[0].count)
    for space in lattice[1:]:
        if space.count(init_space_majority_state) == len(space):
            return True
    return False

def get_majority_problem_score(rule, scheme, n):
    if not n % 2:
        print(f'Majority problem does not support n={n}')
        sys.exit(1)
    t = T(n)
    score = 0
    for ic in gen_lattice_combo(n):
        lattice = list(run(rule, n, t, scheme, ic))
        score += int(lattice_solves_majority_problem(lattice))
    return score

pairs = load_pairs_for_exp_2_and_3()
scores_n = {}
cur_n = 5

while should_run_for_next_n(scores_n, cur_n):
    for rule,schemes in pairs.items():
        rule = int(rule)
        for scheme in schemes:
            if should_run_pair(scores_n, cur_n, rule, scheme):
                score_n_rule_scheme = get_majority_problem_score(rule, scheme, cur_n)
            else:
                score_n_rule_scheme = None
            if cur_n not in scores_n:
                scores_n[cur_n] = {}
            if rule not in scores_n[cur_n]:
                scores_n[cur_n][rule] = {}
            scores_n[cur_n][rule][stringify(scheme)] = score_n_rule_scheme
    cur_n += 2
for n in scores_n:
    df = pd.DataFrame(scores_n[n]).T
    df.sort_index(inplace=True)
    df = df.T
    df.to_csv(f'scores-DCT-{n}x{T(n)}.csv')
