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
import csv

server = 'http://localhost:1234/v1'


def makeGraph(d):
    global g
    g = nx.Graph(d)
    nx.write_graphml(g, 'g.xml')
    authorMap = from_networkx(g)
    # authorNet = requests.post(server + '/networks',
    #                         data=json.dumps(authorMap),
    #                         headers={'Content-Type': 'application/json'})
    # net_id = authorNet.json()['networkSUID']
    # requests.get('%s/apply/layouts/circular/%d' % (server, net_id))
    # Image('%s/networks/%d/views/first.png' % (server, net_id))

def nodeDegree(graph):
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())

    # # plot node degrees
    # fig, ax = plt.subplots()
    # plt.bar(deg, cnt, width=0.80, color='b')
    # plt.title("Degree Histogram")
    # plt.ylabel("Count")
    # plt.xlabel("Degree")
    # ax.set_xticks([d + 0.4 for d in deg])
    # ax.set_xticklabels(deg)
    # plt.savefig('nodeDegrees')

    np.seterr(divide='ignore', invalid='ignore')
    fitgen = powerlaw.Fit(deg, discrete=True)

    global RgenL
    global PgenL

    RgenL = []
    PgenL = []

    Rgen, pgen = fitgen.distribution_compare('power_law', 'lognormal', normalized_ratio=True)
    print(Rgen, pgen)
    RgenL.append(Rgen)
    np.log(pgen)
    PgenL.append(pgen)

    if Rgen < 0:
        print(False)
    else:
        print(True)


def graphRP(PL, RL):
    plt.scatter(PL, RL)
    plt.xlabel('log p-value')
    plt.ylabel('maximum likelihood (R)')
    plt.title('Graph Type Proof')
    plt.savefig('HypoTesting.png')

communities = []
densities = []

def graphAnalysis(graph, i):
    # Community counting
    max_value = 0
    parts = community.best_partition(g)
    max_value = max(parts.values())
    communities.append(max_value)

    # graph density
    global gDense
    gDense = 0
    gDense = nx.density(graph)
    densities.append(gDense)

    # Calculate cluster coefficent- measure of the degree to which nodes in a graph tend to cluster together.
    global clusterCo
    clusterCo = 0
    clusterCo = nx.clustering(graph)
    #print(clusterCo)
    plt.scatter(sorted(clusterCo.values()), clusterCo.keys())
    plt.xlabel('Cluster Coefficient')
    plt.ylabel('Last Authors')
    plt.title('Clustering Coefficent')
    plt.savefig(f'cluster{i}.png')

    # Eigenvector centrality
    global eig_cen
    eig_cen = 0
    eig_cen = nx.eigenvector_centrality(graph)
    plt.scatter(sorted(eig_cen.values()), eig_cen.keys())
    plt.xlabel('Eigenvector Centrality')
    plt.ylabel('Last Authors')
    plt.title('Eigenvector centrality')
    plt.savefig(f'eigenvector{i}.png')

    # Degree centrality
    global deg_cen
    deg_cen = 0
    deg_cen = nx.degree_centrality(graph)
    plt.scatter(sorted(deg_cen.values()), deg_cen.keys())
    plt.xlabel('Degree Centrality')
    plt.ylabel('Last Authors')
    plt.title('Degree Centrality')
    plt.savefig(f'degreeCenter{i}.png')


    # Calculate the node centrality- measure of the influence of a node in a network
    # Betweenness centrality
    # global bet_cen
    # bet_cen = nx.betweenness_centrality(graph)
    # sorted_bet_cen = sorted(bet_cen.items(), key= operator.itemgetter(0), reverse=True)
    # print(sorted_bet_cen)

    # Closeness centrality
    # global clo_cen
    # clo_cen = nx.closeness_centrality(graph)
    # sorted_clo_cen = sorted(clo_cen.items(), key=operator.itemgetter(0), reverse=True)
    # print(sorted_clo_cen)

def inclusiveGraphs(l1, l2):
    #create graph for communities
    plt.bar(l1, len(l1), align='center', alpha=0.5)
    plt.xlabel('Number of Communities')
    plt.title('Communities Detected')
    plt.savefig('communities.png')
    print(l1)

    # create graph for densities
    plt.bar(l2, len(l2), align='center', alpha= 0.5)
    plt.xlabel('Density of Graph')
    plt.ylabel('Graphs')
    plt.title(' Graph Densities')
    plt.savefig('densities.png')
    print(l2)

def writeToCSV(d1,d2,d3,i):

    with open(f'clusteringCsv{i}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d1.items():
            writer.writerow([key, value])

    with open(f'eigenVectorCSV{i}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d2.items():
            writer.writerow([key, value])

    with open(f'degreeCentCsv{i}.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d3.items():
            writer.writerow([key, value])
