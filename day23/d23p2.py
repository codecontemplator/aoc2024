import networkx as nx
    
def largest_clique(graph):
    """
    Finds the largest clique in an undirected graph.

    :param graph: A networkx Graph object.
    :return: A list of nodes representing the largest clique.
    """
    cliques = list(nx.find_cliques(graph))  # Find all maximal cliques
    largest = max(cliques, key=len)        # Find the largest clique by size
    return largest


filename = "day23/input.txt"
with open(filename, 'r') as file:
    lines = file.read().splitlines()

def opposite(node, edge):
    n1, n2 = edge
    return n2 if node == n1 else n1

edges = [ tuple(line.split('-')) for line in lines ]

G = nx.Graph()
G.add_edges_from(edges)

largest = largest_clique(G)
print("Largest Clique:", largest)

result = ','.join(sorted(largest))
print(result)