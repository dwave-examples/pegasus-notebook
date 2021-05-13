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
import networkx as nx
import dimod

def generate_ranr(r, variables, interactions, draw=True):

    G = nx.random_regular_graph(n=variables, d=interactions)
    bqm = dimod.generators.random.ran_r(r, G)

    if draw:
        if  variables*interactions > 2000:
            figsize = (7, 7)
        else:
            figsize = (4, 4)
        plt.figure(figsize=figsize)
        nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=False, node_size=25)
        plt.show()

    return bqm


def compare_solutions(samplesets):
    "Print lowest and average energies."

    systems = samplesets.keys()

    best_energies = {system: round(samplesets[system].first.energy, 3) for
                     system in systems}
    average_energies = {system: round(np.average(samplesets[system].record.energy), 3) for
                     system in systems}

    print("Best energies found: {} (Advantage) and {} (DW-2000Q).".format(
          best_energies["Advantage"], best_energies["DW-2000Q"]))
    print("Average energies: {} (Advantage) and {} (DW-2000Q).".format(
          average_energies["Advantage"], average_energies["DW-2000Q"]))


def compare_embeddings(samplesets):
    "Print chain statistics."

    systems = samplesets.keys()

    average_chains = {system: round(np.average([len(chain) for chain in
                      samplesets[system].info['embedding_context']['embedding'].values()]), 1) for
                      system in systems}
    longest_chains = {system: round(max([len(chain) for chain in
                      samplesets[system].info['embedding_context']['embedding'].values()]), 1) for
                      system in systems}
    chain_breaks = {system: round(100*np.average(samplesets[system].record.chain_break_fraction), 1) for
                      system in systems}

    print("Average chain lengths: {} (Advantage) and {} (DW-2000Q).".format(
          average_chains["Advantage"], average_chains["DW-2000Q"]))
    print("Longest chains: {} (Advantage) and {} (DW-2000Q).".format(
          longest_chains["Advantage"], longest_chains["DW-2000Q"]))
    print("Average chain breaks percentage: {} (Advantage) and {} (DW-2000Q).".format(
          chain_breaks["Advantage"], chain_breaks["DW-2000Q"]))
