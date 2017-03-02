
# coding: utf-8

# In[4]:

get_ipython().system(u'jupyter nbconvert --to script Keyword_input.ipynb')

from watson_developer_cloud import AlchemyLanguageV1
import json

from API_Key import *
alchemy_language = AlchemyLanguageV1(api_key = api_key_chosen)


# In[7]:

def extract_keywords(inputfact):
    output = []
    dates = []
        
    import re
    n_list=[]
    #negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    #keywords
    response = alchemy_language.combined(text=inputfact,extract='typed-rels, dates',max_items=100)
    if response['status'] == 'OK' : 
        
        
        for relation in response['typedRelations']:
            for argument in relation['arguments']:
                if argument['part']=='first' : 
                    subjs = [argument['text']]
                    for entity in argument['entities'] : 
                        ssubj = entity['text']
                        if not (subjs[0] == ssubj):
                            subjs.append(ssubj)
                            
                if argument['part']=='second' :
                    objs = [argument['text']]
                    for entity in argument['entities'] : 
                        sobj = entity['text']
                        if not (objs[0] == sobj):
                            objs.append(sobj)
            
            output.append([subjs, objs, relation['type']])
        if not (len(response['dates'])==0) :
            for date in response['dates']:
                dates.append((date['date'], date['text']))
        
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    
    # Prepositions ? 
    
    # Semantic query expansion
    # dbpedia : Quepy
    # Scoping problem - Political issues. Sample queries
    final = {}
    final['relations'] = output
    final['negations'] = n_list
    final['dates'] = dates
    print(final)
    return final


# In[9]:

'''
# Comment if using from Interface, decomment to test.
while True: 
    print ("Enter a fact:")
    inputfact = input()
    keywords = extract_keywords(inputfact)
    
    # Lee Hsien Loong is the prime minister of Singapore
    # The UN president is Ban Ki Moon
    # The US is at war with Syria
    # Laos became a member of ASEAN in 2016

The UN president is Ban Ki Moon
{'relations': [[['president', 'Ban Ki Moon'], ['UN'], 'employedBy']], 'negations': [], 'dates': []}
Enter a fact:
The US is at war with Syria
{'relations': [[['US'], ['war'], 'agentOf'], [['Syria'], ['war'], 'affectedBy']], 'negations': [], 'dates': []}
Enter a fact:
Laos became a member of ASEAN in 2016
{'relations': [[['member'], ['ASEAN'], 'employedBy']], 'negations': [], 'dates': [('20160101T000000', '2016')]}
Enter a fact:
Lee Hsien Loong is the prime minister of Singapore
{'relations': [[['prime minister', 'Lee Hsien Loong'], ['Singapore'], 'residesIn']], 'negations': [], 'dates': []}
Enter a fact:
Donald Trump became president of the US in 2017
{'relations': [[['president', 'Donald Trump'], ['US'], 'residesIn']], 'negations': [], 'dates': [('20170101T000000', '2017')]}
'''

