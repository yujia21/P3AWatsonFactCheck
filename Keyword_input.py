
# coding: utf-8

# In[43]:

from watson_developer_cloud import AlchemyLanguageV1
import json

from API_Key import *
alchemy_language = AlchemyLanguageV1(api_key = api_key_chosen)


# In[1]:

def extract_keywords(inputfact):
    output = []
    dates = []
        
    import re
    n_list=[]
    # negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    # keywords
    response = alchemy_language.combined(text=inputfact,extract='typed-rels, dates, entities',max_items=100)
    if response['status'] == 'OK' : 

        # if there are typed relations
        if ('typedRelations' in response.keys()):
            # for each relation
            for relation in response['typedRelations']:
                objs = []

                for argument in relation['arguments']:
                    if argument['part']=='first' : 
                        # add subject
                        subj = argument['text']
                        # make sure we add the most specific subj
                        for entity in argument['entities'] : 
                            ssubj = entity['text']
                            if not (subj == ssubj):
                                objs.append([subj, ''])
                                # if no type, add type using results from entities
                                for entity in response['entities'] :
                                    if (subj == entity['text']):
                                        objs[-1][1] = entity['type']
                                
                                subj = ssubj

                    if argument['part']=='second' :
                        # add object
                        obj = argument['text']
                        for entity in argument['entities'] : 
                            sobj = [entity['text'], entity['type']]
                            objs.append(sobj)
                        # make sure no repeat
                        if obj not in [item[0] for item in objs] :
                            objs.append([obj,''])
                            # add type from results of entities if type not available
                            for entity in response['entities'] :
                                if (obj == entity['text']):
                                    objs[-1][1] = entity['type'] 

                output.append([subj, objs, relation['type']])
            
            # add missing entities to first relation : for all entities that are not already in some relation
            if ('entities' in response.keys()):
                for entity in response['entities']:
                    if (entity['text'] not in [rel[0] for rel in output]) and (entity['text'] not in [rel[1][0] for rel in output]) : 
                        #add to first
                        output[0][1].append([entity['text'],entity['type']])
        # if no typed relation
        elif ('entities' in response.keys()):
            # subject is entity with higheset relevance
            subj = response['entities'][0]['text'] 
            objs = []
            # add all objects
            for entity in response['entities'][1:]:
                objs.append(entity['text'],entity['type'])
            # if no other object, add all other words other than subject
            if (len(objs) == 0) :
                objs = inputfact.split()
                for subj_part in subj.split() : 
                    objs.remove(subj_part)
            output.append([subj, objs, ''])

        # if dates, add dates
        if ('dates' in response.keys()) :
            for date in response['dates']:
                dates.append((date['date'], date['text']))
        
                
        
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    
    final = {}
    final['relations'] = output
    final['negations'] = n_list
    final['dates'] = dates

    return final


# In[49]:

'''
k0 = 'Saddam Hussein died in 2015'
k1 ='Lee Hsien Loong is the prime minister of Singapore'
k2 = 'The UN President is Ban Ki Moon'
k3 = 'Donald Trump became president of the US in 2017'

print(extract_keywords(k0))
print(extract_keywords(k1))
print(extract_keywords(k2))
print(extract_keywords(k3))
'''

