from Keyword_input import extract_keywords
from Articles_search import search_from_keywords_wiki, search_from_keywords_dbpedia
from Compare import compare_keywords, compare_keywords_dbpedia

while True: 
    inputfact = input("Enter a fact : ")
    
    # Take in inputfact as a string
    keywords = extract_keywords(inputfact)
    
    # keywords is a dicationary of lists
    # {relations : [], negations : [], dates : []}
    # relations is a list [(list subjects, list of objects, relation)]. 
    # List of subjects can be ['president','Trump'] or just ['member']
    # negations and dates can be empty. Else : date = [(datetime, original text)]
    
   
    # Takes in keywords and searches subj[-1] on Wikipedia
    #keywords = search_from_keywords_wiki(keywords)
    keywords = search_from_keywords_dbpedia(keywords)
    # keywords is a dicationary of lists
    # {relations : [], negations : [], dates : []}
    # relations is a list [(list subjects, list of objects, relation, good_phrases, phrases, #tot phrase)]. 
    # good_phrases has two or more key words in phrase

    # Takes in keywords
    #print(compare_keywords(keywords))
    print(compare_keywords_dbpedia(keywords))
    # Prints True or False
    # Donald Trump became president of the US in 2017
    # Lee Hsien Loong is the prime minister of Singapore
    # The UN president is Ban Ki Moon
    # Emmanuel Macron has become the president of France in 2017
    # Emmanuel Macron is running for the president of France in 2017
