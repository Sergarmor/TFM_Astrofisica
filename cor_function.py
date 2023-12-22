import numpy as np
import pandas as pd
from corrfunc.theory import xi

data = np.load('sergio_ucm.npy')

h=0.7
L = 205.0

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]

binfile = np.logspace(np.log10(0.1), np.log10(10.0), 15)

results = xi(L, 1, binfile, X, Y, Z, verbose=True)


np.save('results', results)