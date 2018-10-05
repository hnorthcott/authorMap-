import networkx as nx
import matplotlib.pyplot as plt
import main
import json
from IPython.display import Image
from py2cytoscape.util import from_networkx
import requests

server = 'http://localhost:1234/v1'


def makeGraph(d):
    g = nx.Graph(d)
    #graphvis= nx.draw_networkx(g, pos=nx.spring_layout(g), with_labels=True)
    #plt.show(graphvis)
    nx.write_graphml(g, 'g.xml')
    authorMap = from_networkx(g)
    authorNet = requests.post(server + '/networks',
                            data=json.dumps(authorMap),
                            headers={'Content-Type': 'application/json'})
    net_id = authorNet.json()['networkSUID']
    requests.get('%s/apply/layouts/circular/%d' % (server, net_id))
    Image('%s/networks/%d/views/first.png' % (server, net_id))













