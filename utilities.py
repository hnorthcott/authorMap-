from Bio import Entrez
import graph
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


disciplines_list = ['adverse+effects', 'analogs+and+derivatives', 'analysis', 'anatomy+and+histology', 'chemistry', 'classification', 'complications', 'cytology', 'diagnosis', 'diagnostic+imaging', 'drug+effects', 'economics', 'education', 'enzymology', 'ethics', 'etiology', 'genetics', 'history', 'immunology', 'instrumentation', 'legislation+and+jurisprudence', 'manpower', 'metabolism', 'methods', 'microbiology', 'organization+and+administration', 'pathogenicity', 'pathology', 'pharmacology', 'physiology', 'prevention+and+control', 'psychology', 'radiation+effects', 'standards', 'statistics+and+numerical+data', 'supply+and+distribution', 'surgery', 'therapeutic+use', 'therapy', 'trends', 'urine', 'utilization', 'veterinary']
broad_list = ['anatomy', 'biochemistry', 'biology', 'biophysics', 'biotechnology', 'chronobiology', 'neurosciences', 'pharmacology', 'physiology', 'toxicology']
narrow_list = ['anatomy, artistic', 'anatomy, comparative', 'anatomy, cross-sectional', 'anatomy, regional', 'anatomy, veterinary', 'cell biology, anatomy', 'embryology', 'histology', 'neuroanatomy', 'osteology', 'carbohydrate biochemistry', 'chemistry, bioinorganic', 'histocytochemistry', 'immunochemistry', 'metabolomics', 'molecular biology', 'neurochemistry', 'proteomics', 'botany', 'cell biology, biology', 'computational biology', 'cryobiology', 'developmental biology', 'ecology', 'exobiology', 'genetics', 'laboratory animal science', 'microbiology', 'natural history', 'neurobiology', 'parasitology', 'photobiology', 'radiobiology', 'sociobiology', 'synthetic biology', 'zoology', 'bionics', 'electrophysiology', 'biomimetics', 'cognitive neuroscience', 'neuroanatomy', 'neurobiology', 'neurochemistry', 'neuroendocrinology', 'neuropathology', 'neuropharmacology', 'neurophysiology', 'biopharmaceutics', 'chemistry, pharmaceutical', 'ethnopharmacology', 'neuropharmacology', 'pharmacoepidemiology', 'pharmacogenetics', 'pharmacognosy', 'pharmacology, clinical', 'psychopharmacology', 'electrophysiology', 'endocrinology', 'neurophysiology', 'physiology, comparative', 'psychophysiology', 'ecotoxicology', 'forensic toxicology', 'toxicogenetics']

def systematicApproach(l):
    for counter, option in enumerate(disciplines_list):
        SAresults = search(option)
        SA_id_list = SAresults['IdList']
        papers = fetch_details(SA_id_list)
        summary_details(SA_id_list)
        amirs_way(m_lastAuthor, m_authorList)
        graph.makeGraph(amirDict)
        graph.nodeDegree(graph.g)
