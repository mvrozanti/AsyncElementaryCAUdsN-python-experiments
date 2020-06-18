#!/usr/bin/env python
import code
import json
import pandas as pd
from pprint import pprint

arq_updates_independentes_traduzidos_1 = open('updates_independentes_traduzidos-1.json')
arq_updates_independentes_traduzidos_2 = open('updates_independentes_traduzidos-2.json')

uit1 = json.load(arq_updates_independentes_traduzidos_1)
uit2 = json.load(arq_updates_independentes_traduzidos_2)

def contagem_esquemas(uit):
    uit1qtds = {}
    for k in uit:
        uit1qtds[k] = len(uit[k])
    return uit1qtds

uit1qtds = contagem_esquemas(uit1)
uit2qtds = contagem_esquemas(uit2)

def latex(uitqtds):
    for k,v in uitqtds.items():
        print(f'{k} & {v} \\\\\\hline')
code.interact(banner='', local=globals().update(locals()) or globals(), exitmsg='')
