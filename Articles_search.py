
# coding: utf-8

# In[1]:

get_ipython().system(u'jupyter nbconvert --to script Articles_search.ipynb')

from watson_developer_cloud import AlchemyDataNewsV1
import json


# In[37]:

from API_Key import *
from Keyword_input import extract_keywords
alchemy_data_news = AlchemyDataNewsV1(api_key = api_key_chosen)


# In[38]:

def search_from_keywords(keywords):
    
    # keywords is a dictionnary with 'subjects' (dictionnary with 'Person', 'Country', 'Organization', 'Unsorted Subjects'),
    # 'relations', 'objects', 'negations'
    
    interesting_keywords = []
    for intermediate_list in list(keywords['subjects'].values()):
        interesting_keywords += intermediate_list
    
    for word in keywords['objects']:
        if word not in interesting_keywords:
            interesting_keywords.append(word)
    
    tts='A['
    for keyword in interesting_keywords:
        tts += keyword+'^'
    tts = tts[:-1]+']'

    results = alchemy_data_news.get_news_documents(
                                                   start='now-1d',
                                                   end='now',
                                                   return_fields=['enriched.url.title',
                                                                  'enriched.url.url',
                                                                  'enriched.url.text',
                                                                  'enriched.url.author',
                                                                  'enriched.url.publicationDate'],
                                                   query_fields={'q.enriched.url.text': tts})
    
    #print(json.dumps(results, indent=2))
    
    text_list = [doc['source']['enriched']['url']['text'] for doc in results['result']['docs']]
    
    keywords_list = [extract_keywords(text) for text in text_list]
    
    return keywords_list


# In[39]:

'''
# Comment if using from Interface, decomment to test.
k = {'subjects': {'Person': ['Trump'], 'Unsorted Subjects': []}, 'objects': ['president']}

search_from_keywords(k)
'''


# In[ ]:



