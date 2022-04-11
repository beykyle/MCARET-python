Mirror of https://gitlab.umich.edu/kmc/mcaret-python
# MCArET-Py  
## Monte Carlo Aromatic-molecular Exciton Transport: Python version
This repository is the next step in the evolution of `MCArEt`. 
It evolves a specified distribution of singlet and triplet molecular excitations on a crystal latticem, in a fully analog kinetic Monte Carlo simulation, and tracks transport and light output.
It assumes fully Markovian behavior, and evolves excitons through the following processes:
 1) singlet flourescence (S_1 -> S_0 + hnu)
 2) triplet phosphorescence (T_1 -> S_0 + hnu)
 3) triplet triplet annhilation (T_1 + T_1 -> S_0 + S_1)
 4) singlet quenching (S_1 + S_1 -> S_0 + S_1)
 5) singlet transport
 6) triplet transport

## Dependencies
`MCArET-Py` depends on `beykylerandomdict`. To install:

```
pip install -i https://test.pypi.org/simple/ beykylerandomdict
```

## Installation
`MCArET-Py` will soon be distributed on pypi. For now:
```
git clone git@gitlab.umich.edu:kmc/mcaret-python.git
```

To run, from inside the mcaret-py directory:
```
python runSimulation.py <inputfile>.ini
```
