from Bio import Entrez
def search(query):
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='100',
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
influencerDict = {}
m_lastAuthor = []
m_authorList = []

def summary_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'awmoulaison@wpi.edu'
    handle = Entrez.esummary(db='pubmed',
                             retmode='xml',
                             id=ids)
    records = Entrez.parse(handle)

    for record in records:
        #print(record)
        m_lastAuthor.append(record['LastAuthor'])
        m_authorList.append(record['AuthorList'])
        global influencerDict
        if len(record['LastAuthor']) > 1:
            record['AuthorList'].pop()
            paperDict[(record['LastAuthor'])] = record['AuthorList']
            influencerDict[(record['LastAuthor'])] = record['Title']

            #print(record['AuthorList'])
            #print(record['LastAuthor'])

    #print(paperDict)
    #print(influencerDict)
    #print(m_authorList)
    #print(m_lastAuthor)


def amirs_way(l1, l2):
    # last author list = l1, author list = l2
    for subList in l2:
        for supAuthor in subList[:]:
            if supAuthor not in l1:
                subList.remove(supAuthor)

    #print(l1)
    #print(l2)

    global amirDict
    amirDict = dict(zip(l1, l2))
    #print(amirDict)
