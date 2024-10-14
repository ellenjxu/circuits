# circuits

Solves a 2Nx2N lattice of resistors

`python solve.py -n 3`

![image](https://github.com/user-attachments/assets/5b605ede-af89-44f7-bf5a-b9a623e536cf)

Final equivalent resistance R_eq: 0.669

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

Currently only works up to N=4.
