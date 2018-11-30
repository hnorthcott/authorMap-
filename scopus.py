# API key = 7dad88ebbea222d693bb348cf0b2cdb3
from pyscopus import Scopus
import utilities


def influencer_detector(d):
    key = '7dad88ebbea222d693bb348cf0b2cdb3'
    scopus = Scopus(key)

    # for author, title in d.items():
    #     basic_search = scopus.search("all(%d) AND %d" % title, author)
    #     print(basic_search)
    #     # in basic search -> extract affliation then author retrival with name and affliation

