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
