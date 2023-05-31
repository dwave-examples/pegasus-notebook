# Copyright 2021 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import unittest

def run_jn(jn, timeout):

    open_jn = open(jn, "r", encoding='utf-8')
    notebook = nbformat.read(open_jn, nbformat.current_nbformat)
    open_jn.close()

    preprocessor = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    preprocessor.allow_errors = True
    preprocessor.preprocess(notebook, {'metadata': {'path': os.path.dirname(jn)}})

    return notebook

def collect_jn_errors(nb):

    errors = []
    for cell in nb.cells:
        if 'outputs' in cell:
            for output in cell['outputs']:
                if output.output_type == 'error':
                    errors.append(output)

    return errors

def embedding_fail(error_list):
    return error_list and error_list[0].evalue == 'no embedding found'

def robust_run_jn(jn, timeout, retries):

    run_num = 1
    notebook = run_jn(jn, timeout)
    errors = collect_jn_errors(notebook)

    while embedding_fail(errors) and run_num < retries:
        run_num += 1
        notebook = run_jn(jn, timeout)
        errors = collect_jn_errors(notebook)

    return notebook, errors

def cell_text(nb, cell):
    return nb["cells"][cell]["outputs"][0]["text"]

def cell_output(nb, cell, part, data_type):
    return nb["cells"][cell]["outputs"][part][data_type]

jn_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
jn_file = os.path.join(jn_dir, '01-exploring-pegasus.ipynb')

class TestJupyterNotebook(unittest.TestCase):

    def test_jn(self):
        # Smoketest
        MAX_EMBEDDING_RETRIES = 3
        MAX_RUN_TIME = 500                 # Ran on my laptop in < 300 secs

        nb, errors = robust_run_jn(jn_file, MAX_RUN_TIME, MAX_EMBEDDING_RETRIES)

        self.assertEqual(errors, [])

        # Test cell outputs:
        # Section More Qubits and Denser Connectivity, code cell 1
        self.assertIn("2048", cell_text(nb, 7))

        # Section Test Case: Embedding Random Graphs, code cell 1
        self.assertIn("image/png", cell_output(nb, 11, 0, "data"))

        # Section Test Case: Embedding Random Graphs, code cell 2
        self.assertIn("found", cell_text(nb, 14))

        # Section Test Case: Embedding Random Graphs, code cell 3
        self.assertIn("found", cell_output(nb, 16, 2, "text"))

        # Section Performance on Sparse Graphs, code cell 1
        self.assertIn("topologies", cell_text(nb, 21))

        # Section Performance on Sparse Graphs, code cell 2 (loop code for 2 nodes)
        self.assertIn("found", cell_output(nb, 23, 2, "text"))

        # Section Performance on Sparse Graphs, code cell 3 (tabulating 2 nodes)
        self.assertIn("text/plain", cell_output(nb, 25, 0, "data"))

        # Section Performance on Sparse Graphs, code cell 4 (loop code for 3 nodes)
        self.assertIn("found", cell_output(nb, 27, 2, "text"))

        # Section Performance on Sparse Graphs, code cell 5 (tabulating 3 nodes)
        self.assertIn("text/plain", cell_output(nb, 29, 0, "data"))

        # Section Performance on Dense Graphs, code cell 1
        self.assertIn("found", cell_output(nb, 31, 2, "text"))

        # Section Performance on Dense Graphs, code cell 2 (tabulating)
        self.assertIn("text/plain", cell_output(nb, 33, 0, "data"))

        # Section Performance on Dense Graphs, code cell 3 (histogram)
        self.assertIn("image/png", cell_output(nb, 34, 0, "data"))

        # Section Embedding in a Single Unit Cell, code cell 1 (draw chimera)
        self.assertIn("image/png", cell_output(nb, 39, 1, "data"))

        # Section Embedding in a Single Unit Cell, code cell 2 (chain lengths)
        self.assertIn("embedded", cell_text(nb, 40))

        # Section Solver Yield, code cell 1
        self.assertIn("Connected", cell_text(nb, 45))

        # Section Solver Yield, code cell 2
        self.assertIn("yield", cell_text(nb, 47))

        # Section Embed Random Graphs, code cell 2 (chain length for clique)
        self.assertIn("Embedded", cell_text(nb, 51))

        # Section Embed Random Graphs, code cell 3 (chain for random graph)
        self.assertIn("image/png", cell_output(nb, 52, 1, "data"))

        # Section Chimera Topology, code cell 1 (draw_chimera(chimera_2))
        self.assertIn("image/png", cell_output(nb, 57, 0, "data"))

        # Section Chimera Topology, code cell 2 (linear_to_chimera)
        self.assertIn("coordinates", nb["cells"][59]["source"])

        # Section Chimera Topology, code cell 3 (translate)
        self.assertIn("Qubit 13", cell_text(nb, 61))

        # Section Pegasus Topology - Qubit Indices, code cell 1
        self.assertIn("image/png", cell_output(nb, 64, 0, "data"))

        # Section Pegasus Topology - Qubit Indices, code cell 2
        self.assertIn("Qubit 36", cell_text(nb, 66))

        # Section Pegasus Topology - Qubit Indices, code cell 3 (draw qubit 36 etc)
        self.assertIn("image/png", cell_output(nb, 68, 0, "data"))

        # Section Pegasus Coordinates, code cell 1
        self.assertIn("Pegasus coordinates", cell_text(nb, 70))

        # Section Pegasus Coordinates, code cell 2
        self.assertIn("Pegasus coordinates", cell_text(nb, 72))

        # Section Nice Coordinates, code cell 1
        self.assertIn("nice coordinates", cell_text(nb, 74))

        # Section Nice Coordinates, code cell 2
        self.assertIn("nice coordinates", cell_text(nb, 76))

        # Section Chimera Embedding, code cell 1
        self.assertIn("image/png", cell_output(nb, 79, 0, "data"))

        # Section Chimera Embedding, exercise 1 cell 2 (test solution)
        self.assertIn("image/png", cell_output(nb, 83, 0, "data"))

        # Section Chimera Embedding, exercise 2 cell 2 (test solution)
        self.assertIn("image/png", cell_output(nb, 87, 0, "data"))

        # Section Pegasus Embedding, code cell 1
        self.assertIn("image/png", cell_output(nb, 90, 0, "data"))

        # Section Pegasus Embedding, exercise 1 cell 2 (test solution: nodes)
        self.assertIn("image/png", cell_output(nb, 94, 0, "data"))

        # Section Pegasus Embedding, exercise 2 cell 2 (test solution: edges)
        self.assertIn("image/png", cell_output(nb, 98, 0, "data"))

        # Section Pegasus Embedding, exercise 3 cell 2 (test solution: problem)
        self.assertIn("image/png", cell_output(nb, 103, 0, "data"))

        # Section Example Problem: RANr, code cell 1
        self.assertIn("image/png", cell_output(nb, 106, 0, "data"))

        # Section Submit a Problem to an Advantage System, code cell 1
        self.assertIn("image/png", cell_output(nb, 110, 0, "data"))

        # Section Submit a Problem to an Advantage System, code cell 2 (Compare the solutions)
        self.assertIn("Best energy found", cell_text(nb, 112))

        # Section Submit a Problem to an Advantage System, code cell 3 (analyze)
        self.assertIn("Average chain length", cell_text(nb, 114))

        # Section Submit a Problem to an Advantage System, code cell 4 (histogram)
        self.assertIn("image/png", cell_output(nb, 116, 0, "data"))
