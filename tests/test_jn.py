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
        self.assertIn("image/png", nb["cells"][11]["outputs"][0]["data"])

        # Section Test Case: Embedding Random Graphs, code cell 2
        self.assertIn("found", cell_text(nb, 14))

        # Section Test Case: Embedding Random Graphs, code cell 3
        self.assertIn("found", nb["cells"][16]["outputs"][2]["text"])

        # Section Performance on Sparse Graphs, code cell 1
        self.assertIn("topologies", cell_text(nb, 21))

        # Section Performance on Sparse Graphs, code cell 2 (loop code for 2 nodes)
        self.assertIn("found", nb["cells"][23]["outputs"][2]["text"])

        # Section Performance on Sparse Graphs, code cell 3 (tabulating 2 nodes)
        self.assertIn("text/plain", nb["cells"][25]["outputs"][0]["data"])

        # Section Performance on Sparse Graphs, code cell 4 (loop code for 3 nodes)
        self.assertIn("found", nb["cells"][27]["outputs"][2]["text"])

        # Section Performance on Sparse Graphs, code cell 5 (tabulating 3 nodes)
        self.assertIn("text/plain", nb["cells"][29]["outputs"][0]["data"])

        # Section Performance on Dense Graphs, code cell 1
        self.assertIn("found", nb["cells"][31]["outputs"][2]["text"])

        # Section Performance on Dense Graphs, code cell 2 (tabulating)
        self.assertIn("text/plain", nb["cells"][33]["outputs"][0]["data"])

        # Section Performance on Dense Graphs, code cell 3 (histogram)
        self.assertIn("image/png", nb["cells"][34]["outputs"][0]["data"])

        # Section Embedding in a Single Unit Cell, code cell 1 (draw chimera)
        self.assertIn("image/png", nb["cells"][39]["outputs"][1]["data"])

        # Section Embedding in a Single Unit Cell, code cell 2 (chain lengths)
        self.assertIn("embedded", cell_text(nb, 40))

        # Section Solver Availability, code cell 1
        self.assertIn("Connected", cell_text(nb, 45))

        # Section Solver Availability, code cell 2
        self.assertIn("yield", cell_text(nb, 47))

        # Section Embed Random Graphs, code cell 2 (chain length for clique)
        self.assertIn("embedded", cell_text(nb, 51))

        # Section Embed Random Graphs, code cell 2 (chain for random graph)
        self.assertIn("image/png", nb["cells"][52]["outputs"][1]["data"])

        # Section Chimera Topology, code cell 1 (draw_chimera(chimera_2))
        self.assertIn("image/png", nb["cells"][57]["outputs"][0]["data"])

        # Section Chimera Topology, code cell 2 (linear_to_chimera)
        self.assertIn("coordinates", nb["cells"][59]["source"])

        # Section Chimera Topology, code cell 3 (translate)
        self.assertIn("Qubit 13", cell_text(nb, 61))

        # Section Pegasus Topology, code cell 1 (draw_pegasus(pegasus_2))
        self.assertIn("image/png", nb["cells"][64]["outputs"][0]["data"])
