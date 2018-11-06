import networkx as nx
import json
from IPython.display import Image
from py2cytoscape.util import from_networkx
import requests

server = 'http://localhost:1234/v1'


def makeGraph(d):
    global g
    g = nx.Graph(d)
    #graphvis= nx.draw_networkx(g, pos=nx.spring_layout(g), with_labels=True)
    #plt.show(graphvis)
    nx.write_graphml(g, 'g.xml')
    authorMap = from_networkx(g)
    authorNet = requests.post(server + '/networks',
                            data=json.dumps(authorMap),
                            headers={'Content-Type': 'application/json'})
    net_id = authorNet.json()['networkSUID']
    requests.get('%s/apply/layouts/force-directed/%d' % (server, net_id))
    Image('%s/networks/%d/views/first.png' % (server, net_id))


def graphAnalysis(graph):
    #Calculate cluster coefficent- measure of the degree to which nodes in a graph tend to cluster together.
    print(nx.clustering(graph))
    # Calculate the node centrality- measure of the influence of a node in a network
    # Betweenness centrality
    bet_cen = nx.betweenness_centrality(graph)
    print(bet_cen)
    # Closeness centrality
    clo_cen = nx.closeness_centrality(graph)
    print(clo_cen)
    # Eigenvector centrality
    eig_cen = nx.eigenvector_centrality(graph)
    print(eig_cen)
    # Degree centrality
    deg_cen = nx.degree_centrality(graph)
    print(deg_cen)
















