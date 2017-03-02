
# coding: utf-8

# In[3]:

get_ipython().system(u'jupyter nbconvert --to script Compare.ipynb')


# In[2]:

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
        print('True')
    else : 
        print('False')
    print(final_prob)

