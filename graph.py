import networkx as nx
import json
from IPython.display import Image
from py2cytoscape.util import from_networkx
import requests
import operator
import collections
import numpy as np
import powerlaw
import mpmath
import matplotlib.pyplot as plt
import community

server = 'http://localhost:1234/v1'


def makeGraph(d):
    global g
    g = nx.Graph(d)
    '''
    # Community showing in matplotlib 
    parts = community.best_partition(g)
    values = [parts.get(node) for node in g.nodes()]
    nx.draw(g, node_color=values, with_labels=False)
    plt.show()
    '''
    nx.write_graphml(g, 'g.xml')
    authorMap = from_networkx(g)
    authorNet = requests.post(server + '/networks',
                            data=json.dumps(authorMap),
                            headers={'Content-Type': 'application/json'})
    net_id = authorNet.json()['networkSUID']
    requests.get('%s/apply/layouts/circular/%d' % (server, net_id))
    Image('%s/networks/%d/views/first.png' % (server, net_id))

def nodeDegree(graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    np.seterr(divide='ignore', invalid='ignore')
    fitgen = powerlaw.Fit(deg, discrete=True)

    Rgen, pgen = fitgen.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print(Rgen, pgen)

    if Rgen < 0:
        print(False)
    else:
         print(True)

    # fig, ax = plt.subplots()
    # plt.bar(deg, cnt, width=0.80, color='b')
    # plt.title("Degree Histogram")
    # plt.ylabel("Count")
    # plt.xlabel("Degree")
    # ax.set_xticks([d + 0.4 for d in deg])
    # ax.set_xticklabels(deg)
    # plt.show()

def graphAnalysis(graph):
    #Calculate cluster coefficent- measure of the degree to which nodes in a graph tend to cluster together.
    print(nx.clustering(graph))
    #graph density
    print(nx.density(graph))
    # Calculate the node centrality- measure of the influence of a node in a network
    # Betweenness centrality
    global bet_cen
    bet_cen = nx.betweenness_centrality(graph)
    sorted_bet_cen = sorted(bet_cen.items(), key= operator.itemgetter(0), reverse=True)
    print(sorted_bet_cen)
    # Closeness centrality
    global clo_cen
    clo_cen = nx.closeness_centrality(graph)
    sorted_clo_cen = sorted(clo_cen.items(), key=operator.itemgetter(0), reverse=True)
    print(sorted_clo_cen)
    # Eigenvector centrality
    global eig_cen
    eig_cen = nx.eigenvector_centrality(graph)
    sorted_eig_cen = sorted(eig_cen.items(), key=operator.itemgetter(0), reverse=True)
    print(sorted_eig_cen)
    # Degree centrality
    global deg_cen
    deg_cen = nx.degree_centrality(graph)
    sorted_deg_cen = sorted(deg_cen.items(), key=operator.itemgetter(0), reverse=True)
    print(deg_cen)

