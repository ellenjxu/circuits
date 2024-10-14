# circuits

> what better way to learn circuits than to get nerd sniped by XKCD's nerd snipe problem?

> ![image](https://github.com/user-attachments/assets/37f2ed65-71ee-4c08-8e68-6171ecd42f8e)

Solving even simple resistive lattice circuits is hard. In general, _there is no closed form formula for current through a 2Nx2N resistor lattice._

### Resistive lattice solver

Imagine a resistive lattice as a napkin which you can fold along lines of symmetry. Using symmetry arguments we can greatly simplify the circuit, then apply circuit laws.

Here we automatically simplify the circuit by applying operations on graphs.

`python solve.py -n 3`

![image](https://github.com/user-attachments/assets/5b605ede-af89-44f7-bf5a-b9a623e536cf)

Final equivalent resistance R_eq: 0.669

### How it works

general operations:

- series/parallel
- connect equipotential nodes
- wye delta

for a nxn lattice:

1. fold along line of symmetry (join two equipotential nodes)
2. collapse along line of equipotential
3. get rid of leaf nodes
4. apply series and parallel circuits

Currently only works up to N=4. For an [infinite lattice](https://arxiv.org/pdf/cond-mat/9909120) the equivalent resistance converges to 0.5.
