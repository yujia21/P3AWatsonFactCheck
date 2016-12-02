
# coding: utf-8

# In[47]:

from alchemyapi import AlchemyAPI
import json
alchemyapi = AlchemyAPI()

from ipywidgets import widgets, interact
from IPython.display import display


# In[63]:

def extract_keywords(inputfact):
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
        print('## Concepts ##')
        for concept in response['concepts']:
            print('text: ', concept['text'].encode('utf-8'))
            print('relevance: ', concept['relevance'])
    else:
        print('Error in keyword extaction call: ', response['statusInfo'])
    print('')
    print('')


# In[ ]:

#Else if python
while (True) : 
    print ("Enter a fact:")
    inputfact = input()
    extract_keywords(inputfact)

