# circuits

Solves a 2Nx2N lattice of resistors

`python resistor_lattice.py -n 3`

![image](https://github.com/user-attachments/assets/5b605ede-af89-44f7-bf5a-b9a623e536cf)

### how it works

general operations:
- series/parallel
- connect equipotential nodes
- wye delta

for a nxn lattice:
1. fold along line of symmetry (join two equipotential nodes)
2. collapse along line of equipotential
3. get rid of leaf nodes
4. apply series and parallel circuits
