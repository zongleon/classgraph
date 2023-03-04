import networkx as nx
from tqdm import tqdm

base = nx.read_graphml("./graphs/classgraphLM.graphml")
other = nx.read_graphml("./graphs/classgraphclean5.graphml")

for u, v, weight in tqdm(other.edges.data("weight")):
    if base.has_node(u) and base.has_node(v):
        base.add_edge(u, v, weight=weight)

remove = [(u,v,weight) for (u,v,weight) in base.edges.data("weight") if float(weight) < 0.001];
base.remove_edges_from(remove)

nx.write_graphml(base, "./graphs/classgraphMERGE.graphml")
