import networkx as nx
import main


def makeGraph(d):
    g = nx.Graph(d)
    nx.write_graphml(g, 'g.xml')













