#!/usr/bin/env python
from glob import glob
import code
import sys
import json

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd

def plot_dim(dim):
   dirnames = glob(f'[0-9][0-9][0-9]-{dim}*')
   global_scores = {}
   for d in dirnames:
      global_scores[d[:3]] = json.load(open(f'./{d}/scores.json')) 

   df = pd.DataFrame(global_scores).transpose()
   # code.interact(local=globals().update(locals()) or globals())
   df.sort_index(inplace=True)
   df = df.transpose()
   df.to_csv(f'scores-DCT-{dim}.csv')
   df = df.transpose()
   # return

   fig = plt.figure(figsize=(200,20))
   ax = plt.subplot(111)
   plt.margins(0,0)

   plt.xlabel('Esquema')
   plt.ylabel('Regra')
   ax.set_xticks(np.arange(len(df.columns)))
   ax.set_yticks(np.arange(len(df.index)))
   ax.set_xticklabels(df.columns)
   ax.set_yticklabels(df.index)
   plt.setp(ax.get_xticklabels(), rotation=90, ha='center')
# plt.subplots_adjust(hspace=0.5)

   plt.title(dim)
   cmap = plt.cm.viridis 
   cmap.set_bad(color='black')
   plt.imshow(df, aspect='auto', cmap=cmap)
   plt.colorbar()

# plt.show()
   plt.savefig(f'{dim}.png', bbox_inches='tight')

plot_dim('5x33')
plot_dim('7x129')
plot_dim('9x513')
