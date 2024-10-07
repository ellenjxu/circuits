"""solving an NxN resistive network lattice"""

import networkx as nx
import matplotlib.pyplot as plt

def create_lattice(N):
  G = nx.grid_2d_graph(2*N, 2*N)
  for (u, v) in G.edges():
    G[u][v]['weight'] = 1
  G.add_edge((N-1,N-1),(N,N)) # battery
  return G

def simplify_weights(G):
  '''replace parallel weights after contraction'''
  for u, v, data in G.edges(data=True):
    if 'contraction' in data:
      total_weight = 1/data['weight']
      for contracted_edge in data['contraction'].values():
        total_weight += 1/contracted_edge.get('weight', 0)
      G[u][v]['weight'] = 1/total_weight # parallel resistors
      del G[u][v]['contraction']
  return G

def fold(G,N):
  '''fold along diagonal (line of symmetry)'''
  pairs = [((x,y), (y,x)) for x in range(2*N) for y in range(2*N)]

  for (n1,n2) in pairs:
    if n1 in G and n2 in G:
      G = nx.contracted_nodes(G, n1, n2)
  return simplify_weights(G)

def fold2(G,N):
  '''contract along other diagonal, only diag elements'''
  pairs = [((x,2*N-x-1), (x+1,2*N-x-2)) for x in range(2*N-1)] # starts on bottom left

  for (n1,n2) in pairs:
    if n1 in G and n2 in G:
      G = nx.contracted_nodes(G, n1, n2)
  return simplify_weights(G)

def remove_leaf(G):
  G = G.copy()
  leaf_nodes = [node for node, degree in dict(G.degree()).items() if degree == 1]
  G.remove_nodes_from(leaf_nodes)
  return G

def simplify_parallel(G, n1, n2, w_new):
  '''if adding a new edge, combine in parallel with previous'''
  if G.has_edge(n1,n2):
    if 'weight' in G[n1][n2]:
      w_old = G[n1][n2]['weight']
      w_new = (w_new * w_old) / (w_new + w_old) # parallel
  return w_new

def simplify_series(G):
  '''find all nodes with 2 neighbors (series = share exclusive node)'''
  G = G.copy()
  for node in list(G.nodes()):
    neighbors = list(G.neighbors(node))
    if len(neighbors) == 2:
      n1, n2 = neighbors
      if 'weight' in G[node][n1] and 'weight' in G[node][n2]:
        w1 = G[node][n1]['weight']
        w2 = G[node][n2]['weight']
        w_new = w1 + w2
        G.remove_node(node)
        w_new = simplify_parallel(G, n1, n2, w_new)
        G.add_edge(n1, n2, weight=w_new)
        print(f"Removed node {node} and connected {n1} and {n2} with weight {w_new}")
  return G

def delta_y_transform(G):
  '''Turns Y->delta network'''
  G = G.copy()
  for node in list(G.nodes()):
    neighbors = list(G.neighbors(node))
    if len(neighbors) == 3:
      n1, n2, n3 = neighbors
      if 'weight' in G[node][n1] and 'weight' in G[node][n2] and 'weight' in G[node][n3]:
        R_a = G[node][n1]['weight']
        R_b = G[node][n2]['weight']
        R_c = G[node][n3]['weight']
        R = R_a*R_b + R_b*R_c + R_c*R_a
        R_ab = R/R_c
        R_bc = R/R_a
        R_ca = R/R_b
        G.remove_node(node) # remove center node
        R_ab = simplify_parallel(G, n1, n2, R_ab)
        G.add_edge(n1, n2, weight=R_ab)
        R_bc = simplify_parallel(G, n2, n3, R_bc)
        G.add_edge(n2, n3, weight=R_bc)
        R_ca = simplify_parallel(G, n3, n1, R_ca)
        G.add_edge(n3, n1, weight=R_ca)
  return G

def display_graph(G, title):
  pos = {node: node for node in G.nodes()}
  plt.figure(figsize=(5, 5))
  nx.draw(G, pos, with_labels=True, node_size=500, font_size=8)
  edge_labels = nx.get_edge_attributes(G, 'weight')
  nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
  plt.title(title)
  plt.axis('off')
  plt.show()

def solve(G):
  display_graph(G, "original")
  # 1. fold along line of symmetry
  G = fold(G,N)
  display_graph(G, "folded graph")
  # 2. contract along other diagonal
  G = fold2(G,N)
  display_graph(G, "contracted graph")
  # 3. get rid of leaf nodes, simplify series and parallel resistors
  G_prev = G
  while True:
    G = simplify_series(remove_leaf(G))
    if nx.is_isomorphic(G, G_prev) or G.number_of_edges() == 1:
      break
    G_prev = G
  # 4. delta-y transforms
  G_prev = G
  while True:
    G = simplify_series(delta_y_transform(G))
    if nx.is_isomorphic(G, G_prev) or G.number_of_edges() == 1:
      break
    G_prev = G
  
  if G.number_of_edges() == 1:
    for u, v in G.edges:
      print(f'Final equivalent resistance R_eq: {G[u][v]['weight']:.3f}')
  else:
    print('solution not found')
  display_graph(G, "final R_eq")

if __name__ == "__main__":
  N = 2 # 5/7
  # N = 3
  G = create_lattice(N)
  solve(G)