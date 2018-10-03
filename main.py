from Bio import Entrez
import graph
import utilities

Entrez.email = 'awmoulaison@wpi.edu'
Entrez.api_key = 'f513b4e2e1a0b578c9d3dd731e36f19f7f08'


def __init__(self, email):
    Entrez.email = 'awmoulaison@wpi.edu'
    Entrez.api_key = 'f513b4e2e1a0b578c9d3dd731e36f19f7f08'


if __name__ == '__main__':
    results = utilities.search('tuberculosis')
    id_list = results['IdList']
    papers = utilities.fetch_details(id_list)
    utilities.summary_details(id_list)
    graph.makeGraph(utilities.paperDict)

    # for i, paper in enumerate(papers['PubmedArticle']):
        # print("%d) %s" % (i + 1, paper['MedlineCitation']['Article']['ArticleTitle']))
