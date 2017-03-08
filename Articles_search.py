
# coding: utf-8

# In[51]:

get_ipython().system('jupyter nbconvert --to script Articles_search.ipynb')


# In[49]:

def search_from_keywords_dbpedia(keywords) :
    from SPARQLWrapper import SPARQLWrapper, JSON
    import wikipedia
    
    relations = keywords['relations']
    dates = keywords['dates']
    new_relations = []
    
    for relation in relations : 
        subj = relation[0]
        objs = relation[1]
        rel = relation[2]
        
        page = wikipedia.page(wikipedia.search(subj)[0])
        title = page.title.replace(' ','_')
        
        #dict_terms = {'residesIn' : ['''dbo:country''']}

        query_string = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?abstract
            WHERE { <http://dbpedia.org/resource/%s> dbo:abstract ?abstract
            FILTER langMatches(lang(?abstract),'en')
            }
        """

        sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        sparql.setReturnFormat(JSON)

        sparql.setQuery(query_string % title)

        results = sparql.query().convert()
        if (len(results) != 0) : 
            abstract = results['results']['bindings'][0]['abstract']['value']
        else : 
            abstract = ''
        
        values = [obj[0].lower() in abstract.lower() for obj in objs+[i[1] for i in dates]]
        relation.append(values)
        relation.append(abstract)
        
        precise = []
        
        for obj in objs : 
            if (obj[1] == "GeopoliticalEntity") :
                query_string = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?country
                WHERE { <http://dbpedia.org/resource/%s> dbo:country ?country
                }
                """
                sparql = SPARQLWrapper("http://dbpedia.org/sparql")
                sparql.setReturnFormat(JSON)

                sparql.setQuery(query_string % title)

                results = sparql.query().convert()
                if (len(results) != 0) : 
                    precise.append(False)
                    for i in range(len(results['results']['bindings'])):
                        country = results['results']['bindings'][i]['country']['value']
                        if (obj[0].lower() in country.lower()):
                            precise[-1] = True

            elif (obj[0].lower() == "prime minister" or obj[0].lower() == "president") :
                query_string = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?office
                WHERE { <http://dbpedia.org/resource/%s> dbo:office ?office
                }
                """
                sparql = SPARQLWrapper("http://dbpedia.org/sparql")
                sparql.setReturnFormat(JSON)

                sparql.setQuery(query_string % title)

                results = sparql.query().convert()
                if (len(results) != 0) : 
                    precise.append(False)
                    for i in range(len(results['results']['bindings'])):
                        office = results['results']['bindings'][i]['office']['value']
                        if (obj[0].lower() in office.lower()):
                            precise[-1] = True

        relation.append(precise)
        new_relations.append(relation)

    keywords['relations'] = new_relations
    return keywords


# In[50]:

'''
# Comment if using from Interface, decomment to test.

k1 = {'relations': [['Lee Hsien Loong', [['prime minister', ''], 'Singapore', ['Singapore', 'GeopoliticalEntity']], 'residesIn']], 'dates': [], 'negations': []}
k2 = {'relations': [['Ban Ki Moon', [['president', ''], 'UN', ['UN', 'Organization']], 'employedBy']], 'dates': [], 'negations': []}
k3 = {'relations': [['Donald Trump', [['president', ''], 'US', ['US', 'GeopoliticalEntity']], 'residesIn']], 'dates': [('20170101T000000', '2017')], 'negations': []}


#search_from_keywords_wiki(k1)
#search_from_keywords_wiki(k2)
#search_from_keywords_wiki(k3)


print(search_from_keywords_dbpedia(k1))
print(search_from_keywords_dbpedia(k2))
print(search_from_keywords_dbpedia(k3))
'''


# In[27]:

def search_from_keywords_wiki(keywords):
    import wikipedia
    import re
    
    # keywords is a dicationary of lists
    # {relations : [], negations : [], dates : []}
    # relations is a list [[subj, list of objects, relation]]. 
    # negations and dates can be empty. Else : date = [(datetime, original text)]
    
    relations = keywords['relations']
    dates = keywords['dates']
    new_relations = []
    
    print("Wikipedia page(s) searched :")
    for relation in relations : 
        subj = relation[0]
        objs = relation[1]
        rel = relation[2]
        
        # Retrieve contents of last subject item
        page = wikipedia.page(wikipedia.search(subj)[0])
        txt = page.content
        print(page.title)
        print('')
        
        signs = ['=','\n']
        for sign in signs : 
            txt = txt.replace(sign,'.')
        phrases = []
        good_phrases = []
        text_list = txt.split('.')
        
        # For each object and dates
        for word in objs+[i[1] for i in dates] : 
            # Add sentences that contain word to phrases. A list for each word
            phrase1 = [s+ '.' for s in text_list if word.lower() in s.lower()]
            if len(phrase1) !=0 :
                phrases.append(phrase1)
                for other_word in objs+[i[1] for i in dates]  : 
                    phrase2 = [s for s in phrases[-1] if (other_word.lower() in s.lower()) and (word != other_word)]
                    if len(phrase2)!=0 : 
                        good_phrases.append(phrase2)
        
        # Reshaping good phrases to be list of phrases with no duplicates
        good_phrases = [phrase for sublist in good_phrases for phrase in sublist]
        good_phrases = list(set(good_phrases))
        
        # New list is [subj, obj, rel, good_phrases, phrases]
        # good_phrases has at least two object words, phrases has one
        relation.append(good_phrases)
        relation.append(phrases)
        relation.append(len(text_list))
        new_relations.append(relation)
    
    keywords['relations'] = new_relations
    return keywords


# In[38]:

'''
def search_from_keywords(keywords):
    from watson_developer_cloud import AlchemyDataNewsV1
    import json
    from API_Key import *
    from Keyword_input import extract_keywords
    alchemy_data_news = AlchemyDataNewsV1(api_key = api_key_chosen)
    
    # keywords is a dicationary of lists
    # {relations : [], negations : [], dates : []}
    # relations is a list [(list subjects, list of objects, relation)]. 
    # List of subjects can be ['president','Trump'] or just ['member']
    # negations and dates can be empty. Else : date = [(datetime, original text)]
    
    relations = keywords[0]
    negations = keywords[1]
    dates = keywords[2]
    
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
'''

