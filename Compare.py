
# coding: utf-8

# In[11]:

get_ipython().system(u'jupyter nbconvert --to script Compare.ipynb')


# In[10]:

def compare_keywords(keywords):
    nb_phrases = 0
    nb_good_phrases = 0
    nb_gp_per_rel = []
    nb_p_per_rel = []
    
    for rel in keywords['relations']:
        print(rel)
        phrases = list(set([phrase for sublist in rel[4] for phrase in sublist]))
        nb_phrases += len(phrases)
        nb_good_phrases += len(rel[3])
        nb_p_per_rel.append(nb_phrases)
        nb_gp_per_rel.append(nb_good_phrases)
    
    p = 1/float(nb_phrases+nb_good_phrases)
    final_prob = 0
    
    for rel in keywords['relations']:
        for phrase in phrases:
            final_prob += 0.5 * p
        for gd_phrase in rel[3]:
            final_prob += p
            
    if final_prob >= 0.7:
        print('True')
    else : 
        print('False')
    print(final_prob)

