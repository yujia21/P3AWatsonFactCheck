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