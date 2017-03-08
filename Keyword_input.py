
# coding: utf-8

# In[9]:

get_ipython().system('jupyter nbconvert --to script Keyword_input.ipynb')

from watson_developer_cloud import AlchemyLanguageV1
import json

from API_Key import *
alchemy_language = AlchemyLanguageV1(api_key = api_key_chosen)


# In[5]:

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
            objs = []
            for argument in relation['arguments']:
                
                if argument['part']=='first' : 
                    subj = argument['text']
                    for entity in argument['entities'] : 
                        ssubj = entity['text']
                        if not (subj == ssubj):
                            objs.append([subj,''])
                            subj = ssubj
                            
                if argument['part']=='second' :
                    objs.append(argument['text'])
                    for entity in argument['entities'] : 
                        sobj = [entity['text'], entity['type']]
                        if not (sobj in objs):
                            objs.append(sobj)
            
            output.append([subj, objs, relation['type']])
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

    return final


# In[8]:

'''
k1 ='Lee Hsien Loong is the prime minister of Singapore'
k2 = 'The UN president is Ban Ki Moon'
k3 = 'Donald Trump became president of the US in 2017'

print(extract_keywords(k1))
print(extract_keywords(k2))
print(extract_keywords(k3))
'''

