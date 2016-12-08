
# coding: utf-8

from alchemyapi import AlchemyAPI
import json
alchemyapi = AlchemyAPI()

from ipywidgets import widgets, interact
from IPython.display import display


def extract_keywords(inputfact):
    print("Your text is : "+inputfact)
    
    import re
    n_list=[]
    #negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    #keywords
    response = alchemyapi.combined("text", inputfact)
    if response['status'] == 'OK' : 
        print('## Keywords ##')
        for keyword in response['keywords']:
            print('text: ', keyword['text'].encode('utf-8'))
            print('relevance: ', keyword['relevance'])
        print('')
        
        print('## Entities ##')
        for entity in response['entities']:
            print('text: ', entity['text'].encode('utf-8'))
            print('type: ', entity['type'])
            print('relevance: ', entity['relevance'])
        print('')
        
        print('## Relations ##')
        response_relations = alchemyapi.relations("text", inputfact)
        for relation in response_relations['relations']:
            print('subject: ', relation['subject']['text'].encode('utf-8'))
            print('action: ', relation['action']['text'].encode('utf-8'))
            print('object: ', relation['subject']['text'].encode('utf-8'))
        
        if (negation) : 
            print('')
            print('## Negations ##')
            if (len(n_list)==1) : 
                print("There is a negation : ", end='')
                print(n_list)
            else : 
                print("There are negations : ", end='')
                print(n_list)
                
        # extract and return keywords, entities, relations and negation -> feed to webpage search
        
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    print('')
    print('')def extract_keywords(inputfact):
    print("Your text is : "+inputfact)
    
    import re
    n_list=[]
    #negation
    negation=False
    for n in ["no", "not", "never", "none", "noone"] : 
        if n in re.compile('\w+').findall(inputfact):
            negation=True
            n_list.append(n)

    
    #keywords
    response = alchemyapi.combined("text", inputfact)
    if response['status'] == 'OK' : 
        print('## Keywords ##')
        for keyword in response['keywords']:
            print('text: ', keyword['text'].encode('utf-8'))
            print('relevance: ', keyword['relevance'])
        print('')
        
        print('## Entities ##')
        for entity in response['entities']:
            print('text: ', entity['text'].encode('utf-8'))
            print('type: ', entity['type'])
            print('relevance: ', entity['relevance'])
        print('')
        
        print('## Relations ##')
        response_relations = alchemyapi.relations("text", inputfact)
        for relation in response_relations['relations']:
            print('subject: ', relation['subject']['text'].encode('utf-8'))
            print('action: ', relation['action']['text'].encode('utf-8'))
            print('object: ', relation['subject']['text'].encode('utf-8'))
        
        if (negation) : 
            print('')
            print('## Negations ##')
            if (len(n_list)==1) : 
                print("There is a negation : ", end='')
                print(n_list)
            else : 
                print("There are negations : ", end='')
                print(n_list)
                
        # extract and return keywords, entities, relations and negation -> feed to webpage search
        
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    print('')
    print('')



while (True) : 
    print ("Enter a fact:")
    inputfact = input()
    extract_keywords(inputfact)

