from Bio import Entrez
import graph
import utilities

Entrez.email = 'awmoulaison@wpi.edu'
Entrez.api_key = 'f513b4e2e1a0b578c9d3dd731e36f19f7f08'


def __init__(self, email):
    Entrez.email = 'awmoulaison@wpi.edu'
    Entrez.api_key = 'f513b4e2e1a0b578c9d3dd731e36f19f7f08'


if __name__ == '__main__':
    results = utilities.search('etiology')
    id_list = results['IdList']
    papers = utilities.fetch_details(id_list)
    utilities.summary_details(id_list)
    utilities.systematicApproach(utilities.narrow_list)
    utilities.remove_supp_authors(utilities.m_lastAuthor, utilities.m_authorList)
    graph.makeGraph(utilities.authorDict)
    graph.nodeDegree(graph.g)
    graph.graphAnalysis(graph.g)
