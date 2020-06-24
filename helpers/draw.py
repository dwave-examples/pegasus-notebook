#    Copyright 2020 D-Wave Systems Inc.

# Imports both in modules and JN for users skipping sections
import matplotlib.pyplot as plt
import numpy as np

num_bins = 100
use_bin = 70

def histogram_energies(samplesets):
    "Plot energy histograms for both QPUs."
    
    fig = plt.figure(figsize=(8, 2))
    a = samplesets[list(samplesets.keys())[0]].record.energy
    b = samplesets[list(samplesets.keys())[1]].record.energy

    bins=np.histogram(np.hstack((a,b)), bins=num_bins)[1]

    ax = fig.add_subplot(1, 1, 1)

    ax.hist(a, bins[0:use_bin], color='b', alpha=0.4, label=list(samplesets.keys())[0])
    ax.hist(b, bins[0:use_bin], color='g', alpha=0.4, label=list(samplesets.keys())[1])

    ax.set_xlabel("Energy")
    ax.set_ylabel("Samples")
    ax.legend()
    plt.show()
