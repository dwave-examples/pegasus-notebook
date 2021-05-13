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
import networkx as nx
import dimod
import minorminer
import pandas as pd

def random_graph(nodes, edges, draw=True):
    "Generate a random graph."

    G = nx.random_regular_graph(n=nodes, d=edges)

    if draw:
        if  nodes*edges > 2000:
            figsize = (7, 7)
        else:
            figsize = (4, 4)
        plt.figure(figsize=figsize)
        nx.draw_networkx(G, pos=nx.spring_layout(G), with_labels=False, node_size=25)
        plt.show()

    return G

def try_embedding(source_graph, target_graphs, timeout=60, tries=2):
    "Attempt to embed a given source graph as minors of target graphs."

    max_len = {}
    for topology in target_graphs:

        embedding = minorminer.find_embedding(source_graph.edges,
                                          target_graphs[topology].edges,
                                          timeout=timeout,
                                          tries=tries)
        if not embedding:
            print("{}: failed to embed.".format(topology))
            max_len[topology] = 0
        else:
            max_len[topology] =  max(map(len, embedding.values()))
            print("{}: found embedding with longest chain of {} qubits.".format(topology, max_len[topology]))

    return max_len

def embedding_loop(nodes, edges, target_graphs, **params):
    "Loop over graph generation and embedding attempts."

    # Set configuration defaults
    problems = params.get('problems', 2)
    draw_problem = params.get('draw_problem', True)
    embedding_timeout = params.get('embedding_timeout', 60)
    embedding_tries = params.get('embedding_tries', 2)

    row = []

    for problem in range(problems):

        print("\nProblem {} of {} for {} nodes and {} edges:".format(
               problem + 1, problems, nodes, edges))

        G = random_graph(nodes, edges, draw_problem)
        row.append([nodes,
                    edges,
                    problem,
                    try_embedding(G, target_graphs, embedding_timeout, embedding_tries)])

    return row
