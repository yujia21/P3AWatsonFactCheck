
# coding: utf-8

# In[2]:

get_ipython().system('jupyter nbconvert --to script Keyword_input.ipynb')

from watson_developer_cloud import AlchemyLanguageV1
import json

from API_Key import *
alchemy_language = AlchemyLanguageV1(api_key = api_key_chosen)


# In[4]:

def extract_keywords(inputfact):
    output=[]
        
    import re
    n_list=[]
    #negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    #keywords
    response = alchemy_language.combined(text=inputfact,extract='typed-rels',max_items=100)
    if response['status'] == 'OK' : 
        
        
        for relation in response['typedRelations']:
            for argument in relation['arguments']:
                if argument['part']=='first' : 
                    this_subject = argument['text']

                if argument['part']=='second' :
                    this_object = argument['text']
            output.append((this_subject,this_object, relation['type']))
        
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    
    # Prepositions ? 

    # Semantic query expansion
    # dbpedia : Quepy
    # Scoping problem - Political issues. Sample queries
    print(output)   
    return output


# In[7]:

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

'''

