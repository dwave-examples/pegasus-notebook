# Copyright 2021 D-Wave Systems Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

# Imports both in modules and JN for users skipping sections
import matplotlib.pyplot as plt
import numpy as np
import dwave_networkx as dnx

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

def histogram_chains_edges(results):
    "Plot chain-length histograms."

    fig, ax = plt.subplots()
    shift = 0

    for problem in results.groupby('Problem'):

        ax.bar(x=problem[1]["Edges"] + shift,
               height=problem[1]["Longest Chain"].apply(lambda x: x['Chimera']),
               width=0.3,
               color='g',
               alpha=0.3)
        ax.bar(x=problem[1]["Edges"] + shift,
               height=problem[1]["Longest Chain"].apply(lambda x: x['Pegasus']),
               width=0.3,
               color='b',
               alpha=0.3)

        shift = shift + 0.3

    ax.set_ylabel('Longest Chain')
    ax.set_xlabel('Edges')
    ax.set_title('Longest Chains for Each Topology')
    ax.legend(['Chimera', 'Pegasus'])

def draw_q16(graph, topology, nred, nblue, nwhite, line_style):
    "Plot the 16-qubit problem's node and edge embedding."

    qpu_graphs = {'Chimera': dnx.chimera_graph, 'Pegasus': dnx.pegasus_graph}
    qpu_plots = {'Chimera': dnx.draw_chimera, 'Pegasus': dnx.draw_pegasus}

    qpu_graph = qpu_graphs[topology[0]]
    qpu_plot = qpu_plots[topology[0]]

    red = qpu_graph(topology[1], node_list=nred, edge_list=[])
    blue = qpu_graph(topology[1], node_list=nblue, edge_list=[])
    white = qpu_graph(topology[1], node_list=nwhite, edge_list=[])

    fig, ax = plt.subplots(1, 1, figsize=(10,5))

    qpu_plot(graph, ax=ax, with_labels=True, node_size=500,
                     node_color='g', style=line_style)

    qpu_plot(red, ax=ax, node_size=500, node_color='r')
    qpu_plot(blue, ax=ax, node_size=500, node_color='b')
    qpu_plot(white, ax=ax, node_size=500, node_color='w')
