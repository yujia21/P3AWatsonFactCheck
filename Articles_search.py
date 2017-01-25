
# coding: utf-8

# In[10]:

get_ipython().system('jupyter nbconvert --to script Articles_search.ipynb')

from watson_developer_cloud import AlchemyDataNewsV1
import json


# In[8]:

from API_Key import *
alchemy_data_news = AlchemyDataNewsV1(api_key = api_key_chosen)


# In[8]:

def search_from_keywords(keywords):
    
    tts='A['
    for keyword in keywords:
        tts += keyword+'^'
    tts = tts[:-1]+']'
    
    print(tts)

    results = alchemy_data_news.get_news_documents(
                                                   start='now-1d',
                                                   end='now',
                                                   return_fields=['enriched.url.title',
                                                                  'enriched.url.url',
                                                                  'enriched.url.author',
                                                                  'enriched.url.publicationDate'],
                                                   query_fields={'q.enriched.url.text': tts})
    print(json.dumps(results, indent=2))


# In[9]:

''' # Comment if using from Interface, decomment to test.
k = ['Trump','president']

search_from_keywords(k)
'''


# In[ ]:



