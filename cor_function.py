import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from corrfunc.theory import xi

data = np.load('sergio_ucm.npy')

L = 205.0

binfile = np.logspace(np.log10(0.1), np.log10(10.0), 15)

results = xi(L, 1, binfile, X, Y, Z)

np.save('results', results)