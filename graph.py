import networkx as nx
import matplotlib.pyplot as plt
import main


def makeGraph(d):
    g = nx.Graph(d)
    graphvis= nx.draw_networkx(g, pos=nx.spring_layout(g), with_labels=True)
    plt.show(graphvis)
    #nx.write_graphml(g, 'g.xml')













