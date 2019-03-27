import networkx as nx
import json
from IPython.display import Image
from py2cytoscape.util import from_networkx
import requests
import operator
import collections
import numpy as np
import powerlaw
import matplotlib.pyplot as plt
import community
import csv
import statistics

server = 'http://localhost:1234/v1'


def makeGraph(d):
    global g
    g = nx.Graph(d)
    nx.write_graphml(g, 'g.xml')
    authorMap = from_networkx(g)
    authorNet = requests.post(server + '/networks',
                            data=json.dumps(authorMap),
                            headers={'Content-Type': 'application/json'})
    net_id = authorNet.json()['networkSUID']
    requests.get('%s/apply/layouts/force-directed/%d' % (server, net_id))
    Image('%s/networks/%d/views/first.png' % (server, net_id))

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


def graphRP(PL, RL):
    plt.scatter(PL, RL)
    plt.xlabel('log p-value')
    plt.ylabel('maximum likelihood (R)')
    plt.title('Graph Type Proof')
    plt.savefig('HypoTesting.png')
    plt.clf()

communities = []
densities = []
degreeCentAvg = []
degreeCentMedian = []
clusterCoAvg = []
eigenVectorAvg = []
numCliques = []
largestCliqueSize = []
isConnected = []
numConnected = []
totalNodes =[]
betweennessCent = []

def graphAnalysis(graph, i):
    #number of total nodes in a graph
    global total
    total = 0
    total = nx.number_of_nodes(graph)
    totalNodes.append(total)
    print("Done with total node")

    # Community counting
    global parts
    parts = 0
    parts = community.best_partition(g)
    max_value = max(parts.values())
    if max_value > 0.00000000:
        communities.append(max_value)
    print("Done communities")

    #Degree centrality
    global deg_cen
    prunedDegreeCent = []
    deg_cen = {}
    deg_cen.clear()
    deg_cen = nx.degree_centrality(graph)

    #getting average and median degree centrality
    DCcount = 0
    DCsum = 0
    for key in deg_cen:
        if deg_cen[key] > 0:
            prunedDegreeCent.append(deg_cen[key])
            DCcount += 1
            DCsum += deg_cen[key]
    DCavg = (DCsum / DCcount)
    degreeCentAvg.append(DCavg)
    median = statistics.median(prunedDegreeCent)
    degreeCentMedian.append(median)
    print("Done with Degree Centrality")


    # Calculate cluster coefficent- measure of the degree to which nodes in a graph tend to cluster together.
    global clusterCo
    clusterCo = {}
    clusterCo.clear()
    clusterCo = nx.clustering(graph)

    # getting average of all values in dictionary
    CCcount = 0
    CCsum = 0
    for key in clusterCo:
        if clusterCo[key] > 0:
            CCcount += 1
            CCsum += clusterCo[key]
    CCavg = (CCsum / CCcount)
    clusterCoAvg.append(CCavg)
    print('Done w. ClusterCo')

    #Betweenness centrality
    global bet_cen
    bet_cen = {}
    bet_cen.clear()
    bet_cen = nx.betweenness_centrality(graph)
    betweennessCent.append(bet_cen)
    print('Done w. Betweenness Cent')

    # graph density
    # global gDense
    # gDense = 0
    # gDense = nx.density(graph)
    # if gDense > 0.00000000:
    #     densities.append(gDense)

    # Eigenvector centrality
    # global eig_cen
    # eig_cen = {}
    # eig_cen.clear()
    # eig_cen = nx.eigenvector_centrality(graph)
    #
    # # getting average eigen vector centrality
    # EVcount = 0
    # EVsum = 0
    # for key in eig_cen:
    #     EVcount += 1
    #     EVsum += eig_cen[key]
    # EVavg = (EVsum / EVcount)
    # eigenVectorAvg.append(EVavg)


    # #Number of cliques and largest clique
    # Qs = 0
    # Qs = nx.graph_number_of_cliques(graph)
    # if Qs > 0:
    #     numCliques.append(Qs)
    #
    # # Size of the largest clique
    # size = 0
    # size = nx.graph_clique_number(graph)
    # if size > 0:
    #     largestCliqueSize.append(size)
    #
    # # is the graph connected?
    # a = nx.is_connected(graph)
    # isConnected.append(a)
    #
    # # how much of the graph is connected
    # num = 0
    # num = nx.number_connected_components(graph)
    # numConnected.append(num)


    # #Calculate the node centrality- measure of the influence of a node in a network
    # Closeness centrality
    # global clo_cen
    # clo_cen = nx.closeness_centrality(graph)
    # sorted_clo_cen = sorted(clo_cen.items(), key=operator.itemgetter(0), reverse=True)
    # print(sorted_clo_cen)

def inclusiveGraphs(l1, l2):
    # Function for graphing the various lists in matplotlib
    #create graph for communities
    plt.bar(l1, len(l1), align='center', alpha=0.5)
    plt.xlabel('Number of Communities')
    plt.title('Communities Detected')
    plt.savefig('communities.png')
    plt.close()
    print(l1)

    # create graph for densities
    plt.bar(l2, len(l2), align='center', alpha= 0.5)
    plt.xlabel('Density of Graph')
    plt.ylabel('Graphs')
    plt.title(' Graph Densities')
    plt.savefig('densities.png')
    plt.close()
    print(l2)

def writeToCSV(d1,d2,d3,i):
    # function to write any list to a CSV

    with open(f'clusteringCsv{i}.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d1.items():
            writer.writerow([key, value])

    with open(f'eigenVectorCSV{i}.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d2.items():
            writer.writerow([key, value])

    with open(f'degreeCentCsv{i}.csv', 'w+') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in d3.items():
            writer.writerow([key, value])


def printGraphingLists (l1, l2, l3, l4, l5, l6 ):
    # function just to print list to the Python console
    print(l1)
    print(l2)
    print(l3)
    print(l4)
    print(l5)
    print(l6)









