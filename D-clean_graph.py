import networkx as nx;

G = nx.read_graphml("./classgraph5.graphml");

print(f"before: {len(G.edges)} {len(G.nodes)}");

remove = [node for node in G.nodes if str(node).isnumeric() or (str(str(node))[0].isnumeric() and not str(str(node)[-1]).isnumeric())];

G.remove_nodes_from(remove);

remove = [(u,v) for (u,v) in G.edges if u==v];

G.remove_edges_from(remove);

print(f"after: {len(G.edges)} {len(G.nodes)}");

nx.write_graphml(G, "./classgraphclean5.graphml");
