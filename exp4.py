#!/usr/bin/env python
from aecaudsn import run, T, gen_lattice_combo, stringify, gen_center_array
import numpy as np
import code
import re
import signal
import sys
import os
from time import sleep
from matplotlib import pyplot as plt

chords = ['A0','A#0','B0','C1','C#1','D1','D#1','E1','F1','F#1','G1','G#1','A1','A#1','B1','C2','C#2','D2','D#2','E2','F2','F#2','G2','G#2','A2','A#2','B2','C3','C#3','D3','D#3','E3','F3','F#3','G3','G#3','A3','A#3','B3','C4','C#4','D4','D#4','E4','F4','F#4','G4','G#4','A4','A#4','B4','C5','C#5','D5','D#5','E5','F5','F#5','G5','G#5','A5','A#5','B5','C6','C#6','D6','D#6','E6','F6','F#6','G6','G#6','A6','A#6','B6','C7','C#7','D7','D#7','E7','F7','F#7','G7','G#7','A7','A#7','B7','C8']
n = len(chords)*2
ic = gen_center_array(n)
# notes = [f'{t} {chord}' for chord in chords for t in types]
def signal_handler(sig, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
# lattice = list(run(51, n, 200, [1,3,1,3,3,2,3,2], ic))
# lattice = list(run(19, n, 200, [2,3,1,3,3,2,3,1], ic))
# lattice = list(run(99, n, 200, [2,3,3,3,3,2,3,1], ic))
# lattice = list(run(55, n, 200, [2,1,2,1,1,1,1,2], ic))
# lattice = list(run(55, n, 200, [2,1,2,1,1,1,1,2], ic))
# lattice = list(run(27, n, 200, [3,2,1,3,2,3,3,1], ic))
# lattice = list(run(19, n, 200, [3,2,1,3,2,3,3,1], ic))
# lattice = list(run(123, n, 200, [2,1,2,1,1,1,1,2], ic))
# lattice = list(run(51, n, 200, [3,2,3,2,2,1,2,1], ic))
# lattice = list(run(33, n, 200, [1,2,2,1,2,1,1,1], ic))
# lattice = list(run(55, n, 200, [2,1,3,1,1,1,1,3], ic))
# lattice = list(run(51, n, 200, [2,1,2,1,1,3,1,3], ic))
# lattice = list(run(51, n, 200, [1,3,2,4,3,2,4,2], ic))
lattice = list(run(55, n, 200, [2,1,1,3,1,1,3,1], ic))

# plt.rcParams["figure.figsize"] = (20,3)
# os.system('amixer sset Master 20%')
fig,ax = plt.subplots(figsize=(15,15))
fig.set_figheight(500)
image = [[0]*len(chords)]*88
im = ax.imshow(image, cmap=plt.get_cmap('gray').reversed(), vmin=0, vmax=1)
ax.autoscale_view(True, True, True)
ax.relim()
ax.set_aspect('equal')
image = []
types = ['sine', 'square', 'triangle', 'sawtooth', 'trapezium', 'exp', 'whitenoise', 'noise', 'tpdfnoise', 'pinknoise', 'brownnoise', 'pluck']
for i,l in enumerate(lattice):
    # plt.plot(l[n//2:n//2+len(chords)//2])
    # plt.show()
    # update_line(hl, l[n//2-len(chords)//2:n//2+len(chords)//2])
    for j,c in enumerate(l[n//2:n//2+len(chords)//2]):
        if c:
            os.system(f'play -qn synth 0.1 exp {chords[j]} fade h 0 0 0 &')
    for j,c in enumerate(l[n//2-len(chords)//2:n//2]):
        if c:
            os.system(f'play -qn synth 0.1 triangle {chords[j]} fade h 0 0 0 &')
    # code.interact(banner='', local=globals().update(locals()) or globals(), exitmsg='')
    image += [l[n//2-len(chords)//2:n//2+len(chords)//2]]
    im.set_data(image[-len(chords):])
    fig.canvas.draw()
    plt.pause(0.1)
