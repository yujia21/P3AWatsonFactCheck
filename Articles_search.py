
# coding: utf-8

# In[4]:

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
        
        # search on wikipedia for the title that ressembles the subject the most
        page = wikipedia.page(wikipedia.search(subj)[0])
        # replace spaces with _
        title = page.title.replace(' ','_')
        
        # GENERAL SPARQL QUERY ON DBPEDIA
        # query string for dbpedia : extract abstract in english
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
        
        # get results as string
        abstract = ''
        if (len(results) != 0) : 
            if (len (results['results']['bindings']) != 0):
                abstract = results['results']['bindings'][0]['abstract']['value']
        
        # add True or False for whether each obj and date is in abstract
        values = [obj[0].lower() in abstract.lower() for obj in objs+[i[1] for i in dates]]
        # add True False list
        relation.append(values)
        # add abstract
        relation.append(abstract)
        
        # TYPE PRECISE SPARQL QUERY ON DBPEDIA
        precise = []
        for obj in objs : 
            # Countries / geopoliticalentities
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
            # jobs
            elif (obj[1] == "JobTitle") :
                query_string = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?office ?type
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
                else : 
                    query_string = """
                    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                    SELECT ?type
                    WHERE { <http://dbpedia.org/resource/Lee_Hsien_Loong> rdf:type ?type }
                    """
                    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
                    sparql.setReturnFormat(JSON)

                    sparql.setQuery(query_string % title)

                    results = sparql.query().convert()
                    if (len(results) != 0) : 
                        precise.append(False)
                        for i in range(len(results['results']['bindings'])):
                            office = results['results']['bindings'][i]['type']['value']
                            if (obj[0].lower().replace(" ", "") in office.lower()):
                                precise[-1] = True

        # add True False list for precise search
        relation.append(precise)
        # update relation with new elements
        new_relations.append(relation)
    # update relations
    keywords['relations'] = new_relations
    return keywords


# In[5]:

'''
# Comment if using from Interface, decomment to test.

k1 = {'relations': [['Lee Hsien Loong', [['prime minister', 'JobTitle'], ['Singapore', 'GeopoliticalEntity']], 'residesIn']], 'dates': [], 'negations': []}
k2 = {'relations': [['Ban Ki Moon', [['president', 'JobTitle'], ['UN', 'Organization']], 'employedBy']], 'dates': [], 'negations': []}
k3 = {'relations': [['Donald Trump', [['president', 'JobTitle'], ['US', 'GeopoliticalEntity']], 'residesIn']], 'dates': [('20170101T000000', '2017')], 'negations': []}

print(search_from_keywords_dbpedia(k1))
print(search_from_keywords_dbpedia(k2))
print(search_from_keywords_dbpedia(k3))
'''

