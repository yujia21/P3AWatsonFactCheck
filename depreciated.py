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


def compare_keywords(keywords):
    nb_phrases = 0
    nb_good_phrases = 0
    nb_gp_per_rel = []
    nb_p_per_rel = []
    page_phrases = 0
    
    for rel in keywords['relations']:
        phrases = list(set([phrase for sublist in rel[4] for phrase in sublist]))
        nb_phrases += len(phrases)
        nb_good_phrases += len(rel[3])
        nb_p_per_rel.append(len(phrases))
        nb_gp_per_rel.append(len(rel[3]))
        page_phrases += rel[5]
        print('Total sentences : '+str(rel[5]))
        print('Total sentences with 1 keyword : '+str(len(phrases)))
        print('Total sentences with 2 keywords: '+str(len(rel[3])))

    p = 1/float(nb_phrases+nb_good_phrases)
    final_prob = 0
    
    for rel in keywords['relations']:
        for phrase in phrases:
            final_prob += 0.5 * p
        for gd_phrase in rel[3]:
            final_prob += p
    
    if (final_prob >= 0.5) and (nb_phrases/page_phrases >=0.1) :
        print(final_prob)
        return True
    else : 
        print(final_prob)
        return False