
# coding: utf-8

# In[2]:

get_ipython().system('jupyter nbconvert --to script Keyword_input.ipynb')

from watson_developer_cloud import AlchemyLanguageV1
import json

from API_Key import *
alchemy_language = AlchemyLanguageV1(api_key = api_key_chosen)


# In[4]:

def extract_keywords(inputfact):
    subjects={} #dictionary of people/organization/country
    subjects['Person']=[]
    subjects['Country']=[]
    subjects['Organization']=[]
    subjects['Unsorted Subjects']=[]
        
    relations=[] #list of relations/verbs
    objects=[]
        
    import re
    n_list=[]
    #negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    #keywords
    response = alchemy_language.combined(text=inputfact,extract='entities,typed-rels',max_items=100)
    if response['status'] == 'OK' : 
        
        
        for entity in response['entities']:
            e_type=entity['type']
            if e_type in subjects : #either person, country or organization
                subjects[e_type].append(entity['text'])
            elif (e_type=='JobTitle'):
                relations.append('worksAs')
                objects.append(entity['text'])

        for relation in response['typedRelations']:
            for argument in relation['arguments']:
                if argument['part']=='second' :
                    for entity in argument['entities']:
                        subjects['Unsorted Subjects'].append(entity['text'])
                if argument['part']=='second' :
                    for entity in argument['entities']:
                        objects.append(entity['text'])
            relations.append(relation['type'])
        
        print('The subjects are: ')
        for key in subjects.keys() :
            if not (len(subjects[key]) == 0) :
                print(key+" : ")
                print(subjects[key])
        print("")
        
        print("The relations and verbs involved are: ")
        print(relations)
        print("")
        
        print("The objects of these relations are: ")
        print(objects)
        print("")
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    
    if (negation) : 
        print('')
        print('## Negations ##')
        if (len(n_list)==1) : 
            print("There is a negation : ", end='')
            print(n_list)
        else : 
            print("There are negations : ", end='')
            print(n_list)


    # Prepositions ? 

    # Semantic query expansion
    # dbpedia : Quepy
    # Scoping problem - Political issues. Sample queries
    print('')
    print('')
    
    output = {'subjects' : subjects, 
              'relations' : relations, 
              'objects' : objects, 
              'negations' : n_list}
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

