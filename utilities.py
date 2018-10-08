from Bio import Entrez

def search(query):
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='500',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'awmoulaison@wpi.edu'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


paperDict = {}


def summary_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'awmoulaison@wpi.edu'
    handle = Entrez.esummary(db = 'pubmed',
                             retmode = 'xml',
                             id= ids)
    records = Entrez.parse(handle)

    for record in records:
        if len(record['LastAuthor']) > 1:
            record['AuthorList'].pop()
            paperDict[(record['LastAuthor'])] = record['AuthorList']
            #print(record['AuthorList'])
            #print(record['LastAuthor'])

    #print(paperDict)
