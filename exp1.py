#!/usr/bin/env python
# Problema: sob que esquemas independentes selecionados a regra 184 permanece conservativa?
# Problem: under which independent update schemes does rule 184 remain conservative?

from aecaudsn import run, T, gen_lattice_combo, stringify
import json
from tqdm import tqdm
import itertools

def is_lattice_conservative(lattice):
    energy = next(lattice).count(1)
    for space in lattice:
        if space.count(1) != energy:
            return False
    return True

schemes = [tuple(s) for s in json.load(open('independent-schemes.json'))]

MAX_N = 8
START_N = 5

for n in tqdm(itertools.count(start=START_N), initial=START_N, total=MAX_N):
    for s in list(schemes):
        for ic in gen_lattice_combo(n):
            lattice = run(184, n, T(n), s, ic)
            if not is_lattice_conservative(lattice):
                schemes.remove(s)
                break
    if n == START_N:
        print()
        for s in schemes:
            print(s)
        break
