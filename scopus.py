# API key = 7dad88ebbea222d693bb348cf0b2cdb3
from pyscopus import Scopus

key = '7dad88ebbea222d693bb348cf0b2cdb3'
scopus = Scopus(key)

author_result_df = scopus.search_author("AUTHLAST(Korkin) and AUTHFIRST(Dmitry)")
print(author_result_df)

retrieve_author_info = scopus.retrieve_author('8779137600')
print(retrieve_author_info)
