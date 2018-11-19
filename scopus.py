# API key = 7dad88ebbea222d693bb348cf0b2cdb3
from pyscopus import Scopus
import utilities


def influencer_detector(d):
    key = '7dad88ebbea222d693bb348cf0b2cdb3'
    scopus = Scopus(key)

    search = scopus.search("KEY(The rise of concurrent care for veterans with advanced cancer at the end of life) AND (Shreve)")
    print(search)

    #for author,title in d.items():




    author_result_df = scopus.search_author("AUTHLAST(Korkin) and AUTHFIRST(Dmitry)")
    print(author_result_df)

    retrieve_author_info = scopus.retrieve_author('8779137600')
    print(retrieve_author_info)
