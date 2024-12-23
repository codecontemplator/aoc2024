from itertools import combinations

filename = "day23/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()

def opposite(node, edge):
    n1, n2 = edge
    return n2 if node == n1 else n1

nodes = list(set(n for line in lines for n in line.split('-')))
edges = [ tuple(line.split('-')) for line in lines ]

edgeMap = dict()
for node in nodes:    
    edgeMap[node] = set(opposite(node,edge) for edge in edges if node in edge)
    edgeMap[node].add(node)

def find_cliques_of_size(graph, size):
    """
    Finds all cliques of a given size in an undirected graph.

    :param graph: A dictionary representing the graph. Keys are nodes, and values are sets of neighbors.
    :param size: The size of the cliques to find.
    :return: A list of cliques, where each clique is a tuple of nodes.
    """
    if size < 2:
        raise ValueError("The size of a clique must be at least 2.")
    
    nodes = list(graph.keys())
    cliques = []

    for potential_clique in combinations(nodes, size):
        if all(graph[u].issuperset(potential_clique) for u in potential_clique):
            cliques.append(potential_clique)

    return cliques


cliques = find_cliques_of_size(edgeMap, 3)
result = [clique for clique in cliques if any(node.startswith('t') for node in clique)]

print(len(result))