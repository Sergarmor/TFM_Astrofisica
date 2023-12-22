import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Corrfunc.theory import xi

data = np.load('sergio_ucm.npy')

h=0.7
L = 205.0

X = data[:, 0]
Y = data[:, 1]
Z = data[:, 2]
weights = np.ones_like(X)

binfile = np.logspace(np.log10(0.1), np.log10(20), 100)

results = xi(L, 1, binfile, X, Y, Z, weights = weights)

np.save('results', results)