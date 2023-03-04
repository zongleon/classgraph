import csv
import networkx as nx
from tqdm import tqdm

G = nx.Graph();

depts = []
with open("coursedata.csv", "r") as csvfile1:
    reader1 = csv.reader(csvfile1, delimiter=',')
    for row in tqdm(reader1):
        dept = row[1]
        if dept not in depts:
            depts.append(dept)
            G.add_node(dept)
    
def cleanup(s):
    return s.replace("[","").replace("]","").replace("b'", "").replace("'", "")

with open("coursepreds.csv", "r") as csvfile2:
    reader2 = csv.reader(csvfile2, delimiter=',')
    for row in tqdm(reader2):
        name = row[0]
        associations = cleanup(str(row[1])).split()
        weights = cleanup(str(row[2])).split()
        G.add_node(name)
        for a, w in tqdm(zip(associations, weights)):
            G.add_edge(name, a, weight=w)

nx.write_graphml(G, "./classgraphLM.graphml");