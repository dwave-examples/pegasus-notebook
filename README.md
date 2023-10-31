[![Linux/Mac/Windows build status](
  https://circleci.com/gh/dwave-examples/pegasus-notebook.svg?style=shield)](
  https://circleci.com/gh/dwave-examples/pegasus-notebook)

# Exploring the Pegasus Topology

D-Wave's newest quantum computer, Advantage, introduces a quantum processing
unit (QPU) with a new architecture: the Pegasus family of topologies. This
notebook explains the Pegasus topology and how it enables superior performance
to previous generations of quantum computers.

The notebook has the following sections:

1. **The Pegasus Advantage** demonstrates and explains the performance differences
   between the previous and new QPU architectures.
2. **Navigating the Topology** describes the new topology and presents Ocean tools
   that help you use it.
3. **Example Problem: RANr** solves a hard problem on an Advantage quantum computer.

## QPU Architecture: Topologies

The layout of the D-Wave QPU is critical to formulating an objective
function in a format that a D-Wave annealing quantum computer can solve.
Although Ocean software automates the mapping from the linear and quadratic
coefficients of a quadratic model to qubit bias and coupling values set on the
QPU, you should understand it if you are using QPU solvers directly because it
has implications for the problem-graph size and solution quality.

The D-Wave QPU is a lattice of interconnected qubits.
While some qubits connect to others via couplers, the D-Wave QPU is not fully
connected. Instead, the qubits of D-Wave annealing quantum computers interconnect
in one of the following topologies:

* Chimera for D-Wave 2000Q and earlier generations of QPUs
* Pegasus for Advantage QPUs

These topologies are described in D-Wave's
[system documentation](https://docs.dwavesys.com/docs/latest/c_gs_4.html).

![comparison](images/ran7_50problems_first5.png)

## Installation

You can run this example without installation in cloud-based IDEs that support 
the [Development Containers specification](https://containers.dev/supporting)
(aka "devcontainers").

For development environments that do not support ``devcontainers``, install 
requirements:

    pip install -r requirements.txt

If you are cloning the repo to your local system, working in a 
[virtual environment](https://docs.python.org/3/library/venv.html) is 
recommended.


## Usage

Your development environment should be configured to 
[access Leap’s Solvers](https://docs.ocean.dwavesys.com/en/stable/overview/sapi.html).
You can see information about supported IDEs and authorizing access to your 
Leap account [here](https://docs.dwavesys.com/docs/latest/doc_leap_dev_env.html).  

The notebook can be opened by clicking on the 
``01-exploring-pegasus.ipynb`` file in VS Code-based IDEs. 

To run a locally installed notebook:

```bash
jupyter notebook
```

## License

See [LICENSE](LICENSE.md) file.
