import csv
import networkx as nx
import numpy as np
from tqdm import tqdm

G = nx.Graph();

depts = []
with open("data/coursedata.csv", "r") as csvfile1:
    reader1 = csv.reader(csvfile1, delimiter=',')
    for row in tqdm(reader1):
        dept = row[1]
        if dept not in depts:
            depts.append(dept)
            G.add_node(dept)
    
def cleanup(s):
    return s.replace("[","").replace("]","").replace("b'", "").replace("'", "")

data = []
with open("data/coursefullvectors.csv", "r") as csvfile2:
    reader2 = csv.reader(csvfile2, delimiter=',')
    for row in reader2:
        name = row[0]
        weights = np.array(cleanup(str(row[1])).split(), dtype=float)
        data.append((name, weights))
        
for name, weight in tqdm(data):    
    G.add_node(name)
    scores = []
    for other, otherweight in data:
        # print(weight, otherweight)
        if name == other:
            continue
        sim = np.dot(weight, otherweight) / (np.linalg.norm(weight) * np.linalg.norm(otherweight))
        if sim > 0.9:
            G.add_edge(name, other, weight=sim)

nx.write_graphml(G, "./classgraphLMsim.graphml");